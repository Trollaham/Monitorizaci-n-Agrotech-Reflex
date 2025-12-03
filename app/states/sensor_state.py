import reflex as rx
import logging
from typing import Optional
from sqlmodel import select
from app.models import Sensor, Parcel, User
from app.states.auth_state import AuthState


class SensorState(rx.State):
    sensors: list[Sensor] = []
    parcels: list[Parcel] = []
    search_value: str = ""
    filter_type: str = "all"
    filter_status: str = "all"
    is_add_open: bool = False
    is_edit_open: bool = False
    is_delete_open: bool = False
    current_sensor_id: int = 0
    name: str = ""
    sensor_type: str = "temperature"
    unique_id: str = ""
    status: str = "active"
    parcel_id: int = 0
    threshold_min: str = ""
    threshold_max: str = ""
    error_message: str = ""

    @rx.event
    async def load_data(self):
        """Load sensors and parcels for the current user."""
        user = await self.get_state(AuthState)
        if not user.user:
            return
        user_data = user.user
        user_id = user_data["id"] if isinstance(user_data, dict) else user_data.id
        with rx.session() as session:
            p_query = select(Parcel).where(Parcel.owner_id == user_id)
            self.parcels = session.exec(p_query).all()
            if not self.parcels:
                self.sensors = []
                return
            parcel_ids = [p.id for p in self.parcels]
            query = select(Sensor).where(Sensor.parcel_id.in_(parcel_ids))
            if self.search_value:
                query = query.where(
                    Sensor.name.contains(self.search_value)
                    | Sensor.unique_id.contains(self.search_value)
                )
            if self.filter_type != "all":
                query = query.where(Sensor.sensor_type == self.filter_type)
            if self.filter_status != "all":
                query = query.where(Sensor.status == self.filter_status)
            self.sensors = session.exec(query).all()

    @rx.event
    def set_search(self, value: str):
        self.search_value = value
        return SensorState.load_data

    @rx.event
    def set_filter_type(self, value: str):
        self.filter_type = value
        return SensorState.load_data

    @rx.event
    def set_filter_status(self, value: str):
        self.filter_status = value
        return SensorState.load_data

    @rx.event
    def open_add_dialog(self):
        self.name = ""
        self.sensor_type = "temperature"
        self.unique_id = ""
        self.status = "active"
        self.threshold_min = ""
        self.threshold_max = ""
        if self.parcels:
            self.parcel_id = self.parcels[0].id
        self.error_message = ""
        self.is_add_open = True

    @rx.event
    def close_add_dialog(self):
        self.is_add_open = False

    @rx.event
    def open_edit_dialog(self, sensor: Sensor):
        self.current_sensor_id = sensor.id
        self.name = sensor.name
        self.sensor_type = sensor.sensor_type
        self.unique_id = sensor.unique_id
        self.status = sensor.status
        self.parcel_id = sensor.parcel_id
        self.threshold_min = (
            str(sensor.threshold_min) if sensor.threshold_min is not None else ""
        )
        self.threshold_max = (
            str(sensor.threshold_max) if sensor.threshold_max is not None else ""
        )
        self.error_message = ""
        self.is_edit_open = True

    @rx.event
    def close_edit_dialog(self):
        self.is_edit_open = False

    @rx.event
    def open_delete_dialog(self, sensor_id: int):
        self.current_sensor_id = sensor_id
        self.is_delete_open = True

    @rx.event
    def close_delete_dialog(self):
        self.is_delete_open = False

    @rx.event
    def set_name(self, value: str):
        self.name = value

    @rx.event
    def set_sensor_type(self, value: str):
        self.sensor_type = value

    @rx.event
    def set_unique_id(self, value: str):
        self.unique_id = value

    @rx.event
    def set_status(self, value: str):
        self.status = value

    @rx.event
    def set_parcel_id(self, value: str):
        try:
            self.parcel_id = int(value)
        except ValueError as e:
            logging.exception(f"Error setting parcel_id: {e}")

    @rx.event
    def set_threshold_min(self, value: str):
        self.threshold_min = value

    @rx.event
    def set_threshold_max(self, value: str):
        self.threshold_max = value

    @rx.event
    def add_sensor(self):
        if not self.name or not self.unique_id or (not self.parcel_id):
            self.error_message = "Name, Unique ID and Parcel are required"
            return
        t_min = float(self.threshold_min) if self.threshold_min else None
        t_max = float(self.threshold_max) if self.threshold_max else None
        with rx.session() as session:
            new_sensor = Sensor(
                name=self.name,
                sensor_type=self.sensor_type,
                unique_id=self.unique_id,
                status=self.status,
                parcel_id=self.parcel_id,
                threshold_min=t_min,
                threshold_max=t_max,
            )
            session.add(new_sensor)
            session.commit()
        self.is_add_open = False
        return SensorState.load_data

    @rx.event
    def update_sensor(self):
        if not self.name or not self.unique_id:
            self.error_message = "Name and Unique ID are required"
            return
        t_min = float(self.threshold_min) if self.threshold_min else None
        t_max = float(self.threshold_max) if self.threshold_max else None
        with rx.session() as session:
            sensor = session.get(Sensor, self.current_sensor_id)
            if sensor:
                sensor.name = self.name
                sensor.sensor_type = self.sensor_type
                sensor.unique_id = self.unique_id
                sensor.status = self.status
                sensor.parcel_id = self.parcel_id
                sensor.threshold_min = t_min
                sensor.threshold_max = t_max
                session.add(sensor)
                session.commit()
        self.is_edit_open = False
        return SensorState.load_data

    @rx.event
    def delete_sensor(self):
        with rx.session() as session:
            sensor = session.get(Sensor, self.current_sensor_id)
            if sensor:
                session.delete(sensor)
                session.commit()
        self.is_delete_open = False
        return SensorState.load_data