import reflex as rx
from app.states.auth_state import AuthState
from app.states.dashboard_state import DashboardState


def navbar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.h2(
                "Dashboard Overview", class_name="text-xl font-semibold text-gray-800"
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        rx.cond(AuthState.user, AuthState.user.username, "Guest"),
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    rx.el.span(
                        rx.cond(AuthState.user, AuthState.user.role, ""),
                        class_name="text-xs text-gray-500 uppercase tracking-wider",
                    ),
                    class_name="flex flex-col items-end mr-3",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon("bell", class_name="w-5 h-5 text-gray-600"),
                        rx.cond(
                            DashboardState.active_alerts > 0,
                            rx.el.span(
                                DashboardState.active_alerts,
                                class_name="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full h-4 w-4 flex items-center justify-center",
                            ),
                        ),
                        class_name="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center relative mr-4 cursor-pointer hover:bg-gray-200 transition-colors",
                        on_click=rx.redirect("/alerts"),
                    ),
                    rx.icon("user", class_name="w-5 h-5 text-gray-600"),
                    class_name="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center",
                ),
                rx.el.button(
                    rx.icon("log-out", class_name="w-5 h-5"),
                    on_click=AuthState.logout,
                    class_name="ml-4 p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors",
                ),
                class_name="flex items-center",
            ),
            class_name="flex justify-between items-center px-8 py-4 bg-white border-b border-gray-200",
        )
    )