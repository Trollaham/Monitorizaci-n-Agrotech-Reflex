import reflex as rx
from sqlmodel import select, desc
from app.models import SensorData, Sensor, Parcel
from app.states.auth_state import AuthState
from datetime import datetime, timedelta
import csv
import io


class HistoryState(rx.State):
    chart_data: list[dict] = []
    sensor_type: str = "temperature"
    days_range: str = "7"

    @rx.event
    async def load_history(self):
        user = await self.get_state(AuthState)
        if not user.user:
            return
        user_data = user.user
        user_id = user_data["id"] if isinstance(user_data, dict) else user_data.id
        with rx.session() as session:
            user_parcels = session.exec(
                select(Parcel.id).where(Parcel.owner_id == user_id)
            ).all()
            if not user_parcels:
                self.chart_data = []
                return
            sensors = session.exec(
                select(Sensor)
                .where(Sensor.parcel_id.in_(user_parcels))
                .where(Sensor.sensor_type == self.sensor_type)
            ).all()
            if not sensors:
                self.chart_data = []
                return
            sensor_ids = [s.id for s in sensors]
            sensor_map = {s.id: s.name for s in sensors}
            days = int(self.days_range)
            cutoff = datetime.utcnow() - timedelta(days=days)
            data = session.exec(
                select(SensorData)
                .where(SensorData.sensor_id.in_(sensor_ids))
                .where(SensorData.timestamp >= cutoff)
                .order_by(SensorData.timestamp)
            ).all()
            formatted_data = []
            for d in data:
                formatted_data.append(
                    {
                        "timestamp": d.timestamp.strftime("%Y-%m-%d %H:%M"),
                        "value": d.value,
                        "sensor": sensor_map.get(d.sensor_id, "Unknown"),
                        "unit": d.unit,
                    }
                )
            self.chart_data = formatted_data

    @rx.event
    def set_sensor_type(self, value: str):
        self.sensor_type = value
        return HistoryState.load_history

    @rx.event
    def set_days_range(self, value: str):
        self.days_range = value
        return HistoryState.load_history

    @rx.event
    async def export_csv(self):
        user = await self.get_state(AuthState)
        if not user.user:
            return
        user_data = user.user
        user_id = user_data["id"] if isinstance(user_data, dict) else user_data.id
        with rx.session() as session:
            user_parcels = session.exec(
                select(Parcel.id).where(Parcel.owner_id == user_id)
            ).all()
            if not user_parcels:
                return
            sensors = session.exec(
                select(Sensor)
                .where(Sensor.parcel_id.in_(user_parcels))
                .where(Sensor.sensor_type == self.sensor_type)
            ).all()
            sensor_ids = [s.id for s in sensors]
            sensor_map = {s.id: s.name for s in sensors}
            days = int(self.days_range)
            cutoff = datetime.utcnow() - timedelta(days=days)
            data = session.exec(
                select(SensorData)
                .where(SensorData.sensor_id.in_(sensor_ids))
                .where(SensorData.timestamp >= cutoff)
                .order_by(SensorData.timestamp)
            ).all()
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Timestamp", "Sensor Name", "Type", "Value", "Unit"])
            for row in data:
                writer.writerow(
                    [
                        row.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        sensor_map.get(row.sensor_id, "Unknown"),
                        self.sensor_type,
                        row.value,
                        row.unit,
                    ]
                )
            csv_content = output.getvalue()
            return rx.download(
                data=csv_content, filename=f"sensor_history_{self.sensor_type}.csv"
            )