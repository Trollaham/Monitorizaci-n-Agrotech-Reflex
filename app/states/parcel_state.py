import reflex as rx
import logging
from typing import Optional
from sqlmodel import select, func, delete
from app.models import Parcel, Sensor
from app.states.auth_state import AuthState


class ParcelState(rx.State):
    parcels: list[Parcel] = []
    sensor_counts: dict[int, int] = {}
    search_value: str = ""
    is_add_open: bool = False
    is_edit_open: bool = False
    is_delete_open: bool = False
    current_parcel_id: int = 0
    name: str = ""
    location: str = ""
    area: float = 0.0
    error_message: str = ""

    @rx.event
    async def load_parcels(self):
        """Load parcels for the current user."""
        user = await self.get_state(AuthState)
        if not user.user:
            return
        with rx.session() as session:
            query = select(Parcel).where(Parcel.owner_id == user.user.id)
            if self.search_value:
                query = query.where(
                    Parcel.name.contains(self.search_value)
                    | Parcel.location.contains(self.search_value)
                )
            self.parcels = session.exec(query).all()
            counts = session.exec(
                select(Sensor.parcel_id, func.count(Sensor.id)).group_by(
                    Sensor.parcel_id
                )
            ).all()
            self.sensor_counts = {p_id: count for p_id, count in counts}

    @rx.event
    def set_search(self, value: str):
        self.search_value = value
        return ParcelState.load_parcels

    @rx.event
    def open_add_dialog(self):
        self.name = ""
        self.location = ""
        self.area = 0.0
        self.error_message = ""
        self.is_add_open = True

    @rx.event
    def close_add_dialog(self):
        self.is_add_open = False

    @rx.event
    def open_edit_dialog(self, parcel: Parcel):
        self.current_parcel_id = parcel.id
        self.name = parcel.name
        self.location = parcel.location
        self.area = parcel.area
        self.error_message = ""
        self.is_edit_open = True

    @rx.event
    def close_edit_dialog(self):
        self.is_edit_open = False

    @rx.event
    def open_delete_dialog(self, parcel_id: int):
        self.current_parcel_id = parcel_id
        self.is_delete_open = True

    @rx.event
    def close_delete_dialog(self):
        self.is_delete_open = False

    @rx.event
    def set_name(self, value: str):
        self.name = value

    @rx.event
    def set_location(self, value: str):
        self.location = value

    @rx.event
    def set_area(self, value: str):
        try:
            self.area = float(value)
        except ValueError as e:
            logging.exception(f"Error setting area: {e}")

    @rx.event
    async def add_parcel(self):
        if not self.name or not self.location:
            self.error_message = "Name and Location are required"
            return
        user = await self.get_state(AuthState)
        if not user.user:
            return
        with rx.session() as session:
            new_parcel = Parcel(
                name=self.name,
                location=self.location,
                area=self.area,
                owner_id=user.user.id,
            )
            session.add(new_parcel)
            session.commit()
            session.refresh(new_parcel)
        self.is_add_open = False
        return ParcelState.load_parcels

    @rx.event
    def update_parcel(self):
        if not self.name or not self.location:
            self.error_message = "Name and Location are required"
            return
        with rx.session() as session:
            parcel = session.get(Parcel, self.current_parcel_id)
            if parcel:
                parcel.name = self.name
                parcel.location = self.location
                parcel.area = self.area
                session.add(parcel)
                session.commit()
        self.is_edit_open = False
        return ParcelState.load_parcels

    @rx.event
    def delete_parcel(self):
        with rx.session() as session:
            parcel = session.get(Parcel, self.current_parcel_id)
            if parcel:
                statement = delete(Sensor).where(
                    Sensor.parcel_id == self.current_parcel_id
                )
                session.exec(statement)
                session.delete(parcel)
                session.commit()
        self.is_delete_open = False
        return ParcelState.load_parcels