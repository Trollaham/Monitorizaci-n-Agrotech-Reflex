import reflex as rx
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password_hash: str
    role: str = "farmer"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Parcel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    location: str
    area: float
    owner_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Sensor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    sensor_type: str
    parcel_id: int = Field(foreign_key="parcel.id")
    unique_id: str
    status: str = "active"
    threshold_min: Optional[float] = None
    threshold_max: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SensorData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sensor_id: int = Field(foreign_key="sensor.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    value: float
    unit: str


class Alert(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sensor_id: int = Field(foreign_key="sensor.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    severity: str
    message: str
    is_active: bool = True
    acknowledged_at: Optional[datetime] = None