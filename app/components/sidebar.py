import reflex as rx
from app.states.auth_state import AuthState


def sidebar_item(text: str, icon: str, url: str) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(icon, class_name="w-5 h-5"),
            rx.el.span(text, class_name="font-medium"),
            class_name="flex items-center gap-3 px-4 py-3 text-gray-700 rounded-lg hover:bg-green-50 hover:text-green-700 transition-colors",
        ),
        href=url,
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("leaf", class_name="w-8 h-8 text-green-600"),
                rx.el.h1("AgroTech", class_name="text-xl font-bold text-gray-800"),
                class_name="flex items-center gap-3 px-6 py-6 border-b border-gray-100",
            ),
            rx.el.nav(
                sidebar_item("Dashboard", "layout-dashboard", "/"),
                sidebar_item("Parcels", "map", "/parcels"),
                sidebar_item("Sensors", "activity", "/sensors"),
                sidebar_item("Alerts", "bell", "/alerts"),
                sidebar_item("History", "bar-chart-2", "/history"),
                sidebar_item("Profile", "user", "/profile"),
                class_name="flex flex-col gap-1 p-4",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="w-64 bg-white border-r border-gray-200 h-screen sticky top-0 hidden md:block shrink-0",
    )