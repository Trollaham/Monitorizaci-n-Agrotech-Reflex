import reflex as rx
from app.states.auth_state import AuthState
from app.pages.dashboard import dashboard_page
from app.pages.auth_pages import login_page


def index() -> rx.Component:
    return rx.cond(AuthState.is_authenticated, dashboard_page(), login_page())