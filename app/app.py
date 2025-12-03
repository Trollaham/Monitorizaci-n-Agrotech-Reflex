import reflex as rx
from fastapi import APIRouter
from app.states.auth_state import AuthState
from app.states.parcel_state import ParcelState
from app.states.sensor_state import SensorState
from app.pages.auth_pages import register_page
from app.pages.index import index
from app.pages.profile import profile_page
from app.pages.parcels import parcels_page
from app.pages.sensors import sensors_page
from app.pages.alerts import alerts_page
from app.pages.history import history_page
from app.states.dashboard_state import DashboardState
from app.states.alert_state import AlertState
from app.states.history_state import HistoryState
from app.api import (
    ingest_sensor_data,
    get_sensor_history,
    get_dashboard_summary,
    list_parcels,
    get_parcel_sensors,
)


def api_routes(app):
    router = APIRouter()
    router.add_api_route(
        "/api/sensors/{unique_id}/data", ingest_sensor_data, methods=["POST"]
    )
    router.add_api_route(
        "/api/sensors/{unique_id}/data", get_sensor_history, methods=["GET"]
    )
    router.add_api_route("/api/dashboard", get_dashboard_summary, methods=["GET"])
    router.add_api_route("/api/parcels", list_parcels, methods=["GET"])
    router.add_api_route(
        "/api/parcels/{parcel_id}/sensors", get_parcel_sensors, methods=["GET"]
    )
    app.include_router(router)
    return app


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
    api_transformer=api_routes,
)
app.add_page(
    index, route="/", on_load=[AuthState.seed_database, AuthState.check_auth_index]
)
app.add_page(profile_page, route="/profile", on_load=AuthState.check_auth_redirect)
app.add_page(
    parcels_page,
    route="/parcels",
    on_load=[AuthState.check_auth_redirect, ParcelState.load_parcels],
)
app.add_page(
    sensors_page,
    route="/sensors",
    on_load=[AuthState.check_auth_redirect, SensorState.load_data],
)
app.add_page(
    alerts_page,
    route="/alerts",
    on_load=[AuthState.check_auth_redirect, AlertState.load_alerts],
)
app.add_page(
    history_page,
    route="/history",
    on_load=[AuthState.check_auth_redirect, HistoryState.load_history],
)
app.add_page(register_page, route="/register", on_load=AuthState.check_public_access)