import reflex as rx
import asyncio
from sqlmodel import select, func, desc
from datetime import datetime
from app.models import Sensor, Parcel, Alert, SensorData
from app.states.auth_state import AuthState


class DashboardState(rx.State):
    total_sensors: int = 0
    active_sensors: int = 0
    active_alerts: int = 0
    total_parcels: int = 0
    recent_activity: list[dict] = []
    chart_data: dict[str, list[dict]] = {
        "temperature": [],
        "humidity": [],
        "light": [],
        "soil_moisture": [],
    }
    type_stats: dict[str, dict] = {
        "temperature": {"avg": 0, "unit": "C", "active": 0, "total": 0},
        "humidity": {"avg": 0, "unit": "%", "active": 0, "total": 0},
        "light": {"avg": 0, "unit": "lx", "active": 0, "total": 0},
        "soil_moisture": {"avg": 0, "unit": "%", "active": 0, "total": 0},
    }
    _is_running: bool = False

    @rx.event(background=True)
    async def start_auto_refresh(self):
        if self._is_running:
            return
        async with self:
            self._is_running = True
        yield DashboardState.load_data
        while True:
            await asyncio.sleep(30)
            async with self:
                if not self._is_running:
                    break
            yield DashboardState.load_data

    @rx.event
    def stop_auto_refresh(self):
        self._is_running = False

    @rx.event
    async def load_data(self):
        auth_state = await self.get_state(AuthState)
        user = auth_state.user
        if not user:
            return
        with rx.session() as session:
            user_parcels = session.exec(
                select(Parcel.id).where(Parcel.owner_id == user.id)
            ).all()
            if not user_parcels:
                self.total_sensors = 0
                self.active_sensors = 0
                self.active_alerts = 0
                self.total_parcels = 0
                self.recent_activity = []
                return
            self.total_parcels = len(user_parcels)
            sensors = session.exec(
                select(Sensor).where(Sensor.parcel_id.in_(user_parcels))
            ).all()
            sensor_ids = [s.id for s in sensors]
            self.total_sensors = len(sensors)
            self.active_sensors = sum((1 for s in sensors if s.status == "active"))
            self.active_alerts = session.exec(
                select(func.count(Alert.id))
                .where(Alert.sensor_id.in_(sensor_ids))
                .where(Alert.is_active == True)
            ).one()
            recent_data = session.exec(
                select(SensorData, Sensor)
                .join(Sensor)
                .where(SensorData.sensor_id.in_(sensor_ids))
                .order_by(desc(SensorData.timestamp))
                .limit(10)
            ).all()
            self.recent_activity = [
                {
                    "time": d.timestamp.strftime("%H:%M"),
                    "sensor": s.name,
                    "value": round(d.value, 1),
                    "unit": d.unit,
                    "type": s.sensor_type,
                }
                for d, s in recent_data
            ]
            types = ["temperature", "humidity", "light", "soil_moisture"]
            new_chart_data = {}
            new_type_stats = {}
            for t in types:
                type_sensors = [s for s in sensors if s.sensor_type == t]
                type_ids = [s.id for s in type_sensors]
                active_count = len([s for s in type_sensors if s.status == "active"])
                total_count = len(type_sensors)
                current_sum = 0
                count = 0
                for sid in type_ids:
                    last = session.exec(
                        select(SensorData)
                        .where(SensorData.sensor_id == sid)
                        .order_by(desc(SensorData.timestamp))
                        .limit(1)
                    ).first()
                    if last:
                        current_sum += last.value
                        count += 1
                avg = round(current_sum / count, 1) if count > 0 else 0
                unit = "C"
                if t == "humidity":
                    unit = "%"
                elif t == "light":
                    unit = "lx"
                elif t == "soil_moisture":
                    unit = "%"
                new_type_stats[t] = {
                    "avg": avg,
                    "unit": unit,
                    "active": active_count,
                    "total": total_count,
                }
                if type_ids:
                    readings = session.exec(
                        select(SensorData)
                        .where(SensorData.sensor_id.in_(type_ids))
                        .order_by(desc(SensorData.timestamp))
                        .limit(20)
                    ).all()
                    readings.sort(key=lambda x: x.timestamp)
                    new_chart_data[t] = [
                        {"timestamp": r.timestamp.strftime("%H:%M"), "value": r.value}
                        for r in readings
                    ]
                else:
                    new_chart_data[t] = []
            self.chart_data = new_chart_data
            self.type_stats = new_type_stats