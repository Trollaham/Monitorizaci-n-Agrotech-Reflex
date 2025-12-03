import reflex as rx
import bcrypt
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
        """Seed the database with initial data if it's empty."""
        with rx.session() as session:
            engine = session.get_bind()
            SQLModel.metadata.create_all(engine)
            user_check = session.exec(select(User)).first()
            if user_check:
                return
            tech_pw = bcrypt.hashpw(
                "admin123".encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            technician = User(
                username="tech_admin",
                email="admin@agrotech.com",
                password_hash=tech_pw,
                role="technician",
            )
            farmer_pw = bcrypt.hashpw(
                "farmer123".encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            farmer = User(
                username="john_doe",
                email="john@farm.com",
                password_hash=farmer_pw,
                role="farmer",
            )
            session.add(technician)
            session.add(farmer)
            session.commit()
            session.refresh(farmer)
            parcel1 = Parcel(
                name="North Field", location="Sector A", area=15.5, owner_id=farmer.id
            )
            parcel2 = Parcel(
                name="Green Valley", location="Sector B", area=22.0, owner_id=farmer.id
            )
            session.add(parcel1)
            session.add(parcel2)
            session.commit()
            session.refresh(parcel1)
            session.refresh(parcel2)
            s1 = Sensor(
                name="Soil Sensor A1",
                sensor_type="soil_moisture",
                parcel_id=parcel1.id,
                unique_id="SENS-001",
            )
            s2 = Sensor(
                name="Temp Sensor A1",
                sensor_type="temperature",
                parcel_id=parcel1.id,
                unique_id="SENS-002",
            )
            s3 = Sensor(
                name="Light Sensor B1",
                sensor_type="light",
                parcel_id=parcel2.id,
                unique_id="SENS-003",
            )
            s4 = Sensor(
                name="Humidity Sensor A1",
                sensor_type="humidity",
                parcel_id=parcel1.id,
                unique_id="SENS-004",
            )
            s5 = Sensor(
                name="CO2 Sensor A1",
                sensor_type="co2",
                parcel_id=parcel1.id,
                unique_id="SENS-005",
            )
            s6 = Sensor(
                name="VOC Sensor B1",
                sensor_type="voc",
                parcel_id=parcel2.id,
                unique_id="SENS-006",
            )
            s7 = Sensor(
                name="NOx Sensor B1",
                sensor_type="nox",
                parcel_id=parcel2.id,
                unique_id="SENS-007",
            )
            session.add(s1)
            session.add(s2)
            session.add(s3)
            session.add(s4)
            session.add(s5)
            session.add(s6)
            session.add(s7)
            session.commit()
            session.refresh(s1)
            session.refresh(s5)
            session.refresh(s6)
            session.refresh(s7)
            d1 = SensorData(sensor_id=s1.id, value=45.2, unit="%")
            d2 = SensorData(sensor_id=s1.id, value=44.8, unit="%")
            d3 = SensorData(sensor_id=s2.id, value=23.5, unit="C")
            d4 = SensorData(sensor_id=s4.id, value=55.0, unit="%")
            d5 = SensorData(sensor_id=s5.id, value=410.0, unit="ppm")
            d6 = SensorData(sensor_id=s6.id, value=120.0, unit="ppb")
            d7 = SensorData(sensor_id=s7.id, value=45.0, unit="ppb")
            session.add(d1)
            session.add(d2)
            session.add(d3)
            session.add(d4)
            session.add(d5)
            session.add(d6)
            session.add(d7)
            a1 = Alert(
                sensor_id=s1.id,
                severity="warning",
                message="Soil moisture low",
                is_active=True,
            )
            session.add(a1)
            session.commit()