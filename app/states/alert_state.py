import reflex as rx
from sqlmodel import select, desc
from app.models import Alert, Sensor, Parcel
from app.states.auth_state import AuthState
from datetime import datetime


class AlertState(rx.State):
    alerts: list[dict] = []
    active_filter: bool = True
    severity_filter: str = "all"

    @rx.event
    async def load_alerts(self):
        user = await self.get_state(AuthState)
        if not user.user:
            return
        with rx.session() as session:
            user_parcels = session.exec(
                select(Parcel.id).where(Parcel.owner_id == user.user.id)
            ).all()
            if not user_parcels:
                self.alerts = []
                return
            user_sensors = session.exec(
                select(Sensor.id).where(Sensor.parcel_id.in_(user_parcels))
            ).all()
            if not user_sensors:
                self.alerts = []
                return
            query = (
                select(Alert, Sensor)
                .join(Sensor)
                .where(Alert.sensor_id.in_(user_sensors))
            )
            if self.active_filter:
                query = query.where(Alert.is_active == True)
            if self.severity_filter != "all":
                query = query.where(Alert.severity == self.severity_filter)
            query = query.order_by(desc(Alert.timestamp))
            results = session.exec(query).all()
            self.alerts = [
                {
                    "id": a.id,
                    "sensor_name": s.name,
                    "message": a.message,
                    "severity": a.severity,
                    "timestamp": a.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "is_active": a.is_active,
                    "acknowledged_at": a.acknowledged_at.strftime("%Y-%m-%d %H:%M:%S")
                    if a.acknowledged_at
                    else None,
                }
                for a, s in results
            ]

    @rx.event
    def set_active_filter(self, value: bool):
        self.active_filter = value
        return AlertState.load_alerts

    @rx.event
    def set_severity_filter(self, value: str):
        self.severity_filter = value
        return AlertState.load_alerts

    @rx.event
    def acknowledge_alert(self, alert_id: int):
        with rx.session() as session:
            alert = session.get(Alert, alert_id)
            if alert:
                alert.is_active = False
                alert.acknowledged_at = datetime.utcnow()
                session.add(alert)
                session.commit()
        return AlertState.load_alerts