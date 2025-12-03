import reflex as rx
from fastapi import HTTPException, Query
from typing import Optional
from datetime import datetime
from sqlmodel import select, desc, func
from pydantic import BaseModel
from app.models import Parcel, Sensor, SensorData, Alert


class SensorDataPayload(BaseModel):
    value: float
    unit: str
    timestamp: Optional[datetime] = None
    sensor_id: Optional[str] = None
    type: Optional[str] = None


class SensorDataOut(BaseModel):
    timestamp: datetime
    value: float
    unit: str


class DashboardSummary(BaseModel):
    total_sensors: int
    active_sensors: int
    active_alerts: int
    total_parcels: int
    recent_activity: list[str]


class SensorOut(BaseModel):
    id: int
    unique_id: str
    name: str
    sensor_type: str
    status: str
    last_value: Optional[float] = None
    last_unit: Optional[str] = None


class ParcelOut(BaseModel):
    id: int
    name: str
    location: str
    area: float
    owner_id: int
    sensors: list[SensorOut]


async def ingest_sensor_data(unique_id: str, payload: SensorDataPayload):
    """
    Ingest data for a specific sensor identified by its unique_id.
    POST /api/sensors/{unique_id}/data
    """
    with rx.session() as session:
        sensor = session.exec(
            select(Sensor).where(Sensor.unique_id == unique_id)
        ).first()
        if not sensor:
            raise HTTPException(
                status_code=404, detail=f"Sensor with ID {unique_id} not found"
            )
        ts = payload.timestamp if payload.timestamp else datetime.utcnow()
        new_data = SensorData(
            sensor_id=sensor.id, value=payload.value, unit=payload.unit, timestamp=ts
        )
        session.add(new_data)
        if sensor.threshold_min is not None and payload.value < sensor.threshold_min:
            alert = Alert(
                sensor_id=sensor.id,
                timestamp=ts,
                severity="warning",
                message=f"Value {payload.value} {payload.unit} is below minimum threshold {sensor.threshold_min}",
                is_active=True,
            )
            session.add(alert)
        if sensor.threshold_max is not None and payload.value > sensor.threshold_max:
            alert = Alert(
                sensor_id=sensor.id,
                timestamp=ts,
                severity="warning",
                message=f"Value {payload.value} {payload.unit} is above maximum threshold {sensor.threshold_max}",
                is_active=True,
            )
            session.add(alert)
        session.commit()
        session.refresh(new_data)
        return {
            "status": "success",
            "data_id": new_data.id,
            "message": "Data ingested successfully",
        }


async def get_sensor_history(
    unique_id: str,
    from_date: Optional[datetime] = Query(None, alias="from"),
    to_date: Optional[datetime] = Query(None, alias="to"),
    limit: int = 100,
) -> list[SensorDataOut]:
    """
    Get historical data for a sensor.
    GET /api/sensors/{unique_id}/data
    Query params: from (ISO8601), to (ISO8601), limit (default 100)
    """
    with rx.session() as session:
        sensor = session.exec(
            select(Sensor).where(Sensor.unique_id == unique_id)
        ).first()
        if not sensor:
            raise HTTPException(
                status_code=404, detail=f"Sensor with ID {unique_id} not found"
            )
        query = select(SensorData).where(SensorData.sensor_id == sensor.id)
        if isinstance(from_date, datetime):
            query = query.where(SensorData.timestamp >= from_date)
        if isinstance(to_date, datetime):
            query = query.where(SensorData.timestamp <= to_date)
        query = query.order_by(desc(SensorData.timestamp)).limit(limit)
        results = session.exec(query).all()
        return [
            SensorDataOut(timestamp=row.timestamp, value=row.value, unit=row.unit)
            for row in results
        ]


async def get_dashboard_summary() -> DashboardSummary:
    """
    Get high-level stats for the dashboard.
    GET /api/dashboard
    """
    with rx.session() as session:
        total_sensors = session.exec(select(func.count(Sensor.id))).one()
        active_sensors = session.exec(
            select(func.count(Sensor.id)).where(Sensor.status == "active")
        ).one()
        total_parcels = session.exec(select(func.count(Parcel.id))).one()
        active_alerts = session.exec(
            select(func.count(Alert.id)).where(Alert.is_active == True)
        ).one()
        recent_logs = session.exec(
            select(SensorData).order_by(desc(SensorData.timestamp)).limit(5)
        ).all()
        activity = []
        for log in recent_logs:
            s = session.get(Sensor, log.sensor_id)
            name = s.name if s else "Unknown"
            activity.append(
                f"[{log.timestamp.strftime('%H:%M')}] {name}: {log.value} {log.unit}"
            )
        return DashboardSummary(
            total_sensors=total_sensors,
            active_sensors=active_sensors,
            active_alerts=active_alerts,
            total_parcels=total_parcels,
            recent_activity=activity,
        )


async def list_parcels() -> list[ParcelOut]:
    """
    List all parcels with their sensors and latest reading.
    GET /api/parcels
    """
    with rx.session() as session:
        parcels = session.exec(select(Parcel)).all()
        result = []
        for p in parcels:
            sensors = session.exec(select(Sensor).where(Sensor.parcel_id == p.id)).all()
            sensor_outs = []
            for s in sensors:
                last_data = session.exec(
                    select(SensorData)
                    .where(SensorData.sensor_id == s.id)
                    .order_by(desc(SensorData.timestamp))
                    .limit(1)
                ).first()
                sensor_outs.append(
                    SensorOut(
                        id=s.id,
                        unique_id=s.unique_id,
                        name=s.name,
                        sensor_type=s.sensor_type,
                        status=s.status,
                        last_value=last_data.value if last_data else None,
                        last_unit=last_data.unit if last_data else None,
                    )
                )
            result.append(
                ParcelOut(
                    id=p.id,
                    name=p.name,
                    location=p.location,
                    area=p.area,
                    owner_id=p.owner_id,
                    sensors=sensor_outs,
                )
            )
        return result


async def get_parcel_sensors(parcel_id: int) -> list[SensorOut]:
    """
    Get all sensors for a specific parcel ID.
    GET /api/parcels/{parcel_id}/sensors
    """
    with rx.session() as session:
        parcel = session.get(Parcel, parcel_id)
        if not parcel:
            raise HTTPException(status_code=404, detail=f"Parcel {parcel_id} not found")
        sensors = session.exec(
            select(Sensor).where(Sensor.parcel_id == parcel_id)
        ).all()
        output = []
        for s in sensors:
            last_data = session.exec(
                select(SensorData)
                .where(SensorData.sensor_id == s.id)
                .order_by(desc(SensorData.timestamp))
                .limit(1)
            ).first()
            output.append(
                SensorOut(
                    id=s.id,
                    unique_id=s.unique_id,
                    name=s.name,
                    sensor_type=s.sensor_type,
                    status=s.status,
                    last_value=last_data.value if last_data else None,
                    last_unit=last_data.unit if last_data else None,
                )
            )
        return output