import reflex as rx
import bcrypt
import logging
from typing import Optional
from app.models import User, Parcel, Sensor, SensorData, Alert
from sqlmodel import select, SQLModel
from datetime import datetime


class AuthState(rx.State):
    user: Optional[User] = None
    username_input: str = ""
    password_input: str = ""
    email_input: str = ""
    role_input: str = "farmer"
    error_message: str = ""

    @rx.var
    def is_authenticated(self) -> bool:
        return self.user is not None

    @rx.event
    async def check_auth_index(self):
        """Check login for index page. No redirect on failure, but load data if success."""
        if self.is_authenticated:
            from app.states.dashboard_state import DashboardState

            yield DashboardState.start_auto_refresh

    @rx.event
    def check_auth_redirect(self):
        """Check login for protected pages. Redirect to / on failure."""
        if not self.is_authenticated:
            return rx.redirect("/")

    @rx.event
    def check_public_access(self):
        """Redirect logged-in users away from public pages."""
        if self.is_authenticated:
            return rx.redirect("/")

    @rx.event
    def logout(self):
        """Logout the current user."""
        self.user = None
        return rx.redirect("/")

    @rx.event
    def login(self):
        """Authenticate the user."""
        with rx.session() as session:
            user = session.exec(
                select(User).where(User.username == self.username_input)
            ).first()
            if user and bcrypt.checkpw(
                self.password_input.encode("utf-8"), user.password_hash.encode("utf-8")
            ):
                self.user = user
                self.error_message = ""
                return rx.redirect("/")
            else:
                self.error_message = "Invalid username or password"

    @rx.event
    def register(self):
        """Register a new user."""
        if not self.username_input or not self.password_input or (not self.email_input):
            self.error_message = "All fields are required"
            return
        with rx.session() as session:
            existing_user = session.exec(
                select(User).where(User.username == self.username_input)
            ).first()
            if existing_user:
                self.error_message = "Username already exists"
                return
            hashed_pw = bcrypt.hashpw(
                self.password_input.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            new_user = User(
                username=self.username_input,
                email=self.email_input,
                password_hash=hashed_pw,
                role=self.role_input,
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            self.user = new_user
            self.error_message = ""
            return rx.redirect("/")

    @rx.event
    def set_username(self, value: str):
        self.username_input = value

    @rx.event
    def set_password(self, value: str):
        self.password_input = value

    @rx.event
    def set_email(self, value: str):
        self.email_input = value

    @rx.event
    def set_role(self, value: str):
        self.role_input = value

    @rx.event
    def seed_database(self):
        """Seed the database with initial data."""
        with rx.session() as session:
            try:
                engine = session.get_bind()
                SQLModel.metadata.create_all(engine)
                logging.info("Database tables verified/created.")
            except Exception as e:
                logging.exception(f"Failed to verify/create tables: {e}")
        with rx.session() as session:
            try:
                technician = session.exec(
                    select(User).where(User.username == "tech_admin")
                ).first()
                if not technician:
                    tech_pw = bcrypt.hashpw(
                        "admin123".encode("utf-8"), bcrypt.gensalt()
                    ).decode("utf-8")
                    technician = User(
                        username="tech_admin",
                        email="admin@agrotech.com",
                        password_hash=tech_pw,
                        role="technician",
                    )
                    session.add(technician)
                    session.flush()
                    logging.info("Created tech_admin user.")
                farmer = session.exec(
                    select(User).where(User.username == "john_doe")
                ).first()
                if not farmer:
                    farmer_pw = bcrypt.hashpw(
                        "farmer123".encode("utf-8"), bcrypt.gensalt()
                    ).decode("utf-8")
                    farmer = User(
                        username="john_doe",
                        email="john@farm.com",
                        password_hash=farmer_pw,
                        role="farmer",
                    )
                    session.add(farmer)
                    session.flush()
                    logging.info("Created john_doe user.")
                if not farmer.id:
                    session.refresh(farmer)
                parcel1 = session.exec(
                    select(Parcel).where(
                        Parcel.name == "North Field", Parcel.owner_id == farmer.id
                    )
                ).first()
                if not parcel1:
                    parcel1 = Parcel(
                        name="North Field",
                        location="Sector A",
                        area=15.5,
                        owner_id=farmer.id,
                    )
                    session.add(parcel1)
                    session.flush()
                parcel2 = session.exec(
                    select(Parcel).where(
                        Parcel.name == "Green Valley", Parcel.owner_id == farmer.id
                    )
                ).first()
                if not parcel2:
                    parcel2 = Parcel(
                        name="Green Valley",
                        location="Sector B",
                        area=22.0,
                        owner_id=farmer.id,
                    )
                    session.add(parcel2)
                    session.flush()
                if not parcel1.id:
                    session.refresh(parcel1)
                if not parcel2.id:
                    session.refresh(parcel2)
                sensors_config = [
                    {
                        "uid": "SENS-001",
                        "name": "Soil Sensor A1",
                        "type": "soil_moisture",
                        "pid": parcel1.id,
                        "unit": "%",
                        "val": 45.2,
                    },
                    {
                        "uid": "SENS-002",
                        "name": "Temp Sensor A1",
                        "type": "temperature",
                        "pid": parcel1.id,
                        "unit": "C",
                        "val": 23.5,
                    },
                    {
                        "uid": "SENS-003",
                        "name": "Light Sensor B1",
                        "type": "light",
                        "pid": parcel2.id,
                        "unit": "lx",
                        "val": 500.0,
                    },
                    {
                        "uid": "SENS-004",
                        "name": "Humidity Sensor A1",
                        "type": "humidity",
                        "pid": parcel1.id,
                        "unit": "%",
                        "val": 55.0,
                    },
                    {
                        "uid": "SENS-005",
                        "name": "CO2 Sensor A1",
                        "type": "co2",
                        "pid": parcel1.id,
                        "unit": "ppm",
                        "val": 410.0,
                    },
                    {
                        "uid": "SENS-006",
                        "name": "VOC Sensor B1",
                        "type": "voc",
                        "pid": parcel2.id,
                        "unit": "ppb",
                        "val": 120.0,
                    },
                    {
                        "uid": "SENS-007",
                        "name": "NOx Sensor B1",
                        "type": "nox",
                        "pid": parcel2.id,
                        "unit": "ppb",
                        "val": 45.0,
                    },
                ]
                for conf in sensors_config:
                    sensor = session.exec(
                        select(Sensor).where(Sensor.unique_id == conf["uid"])
                    ).first()
                    if not sensor:
                        sensor = Sensor(
                            name=conf["name"],
                            sensor_type=conf["type"],
                            parcel_id=conf["pid"],
                            unique_id=conf["uid"],
                        )
                        session.add(sensor)
                        session.flush()
                        data = SensorData(
                            sensor_id=sensor.id, value=conf["val"], unit=conf["unit"]
                        )
                        session.add(data)
                        if conf["uid"] == "SENS-001":
                            alert = Alert(
                                sensor_id=sensor.id,
                                severity="warning",
                                message="Soil moisture low",
                                is_active=True,
                            )
                            session.add(alert)
                    elif sensor.sensor_type != conf["type"]:
                        sensor.sensor_type = conf["type"]
                        session.add(sensor)
                session.commit()
                logging.info("Database seeding completed successfully.")
            except Exception as e:
                logging.exception(f"Error seeding database: {e}")
                session.rollback()