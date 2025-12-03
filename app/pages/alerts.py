import reflex as rx
from app.components.sidebar import sidebar
from app.components.navbar import navbar
from app.states.alert_state import AlertState


def alert_row(alert: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.cond(
                    alert["severity"] == "critical",
                    rx.icon("badge_alert", class_name="w-5 h-5 text-red-500"),
                    rx.icon(
                        "flag_triangle_right", class_name="w-5 h-5 text-yellow-500"
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        alert["sensor_name"], class_name="font-medium text-gray-900"
                    ),
                    class_name="ml-3",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(alert["message"], class_name="text-sm text-gray-700"),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.span(alert["timestamp"], class_name="text-sm text-gray-500"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.cond(
                alert["is_active"],
                rx.el.span(
                    "Active",
                    class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800",
                ),
                rx.el.div(
                    rx.el.span(
                        "Resolved",
                        class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800",
                    ),
                    rx.el.p(
                        alert["acknowledged_at"],
                        class_name="text-xs text-gray-400 mt-1",
                    ),
                    class_name="flex flex-col",
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.cond(
                alert["is_active"],
                rx.el.button(
                    rx.icon("check", class_name="w-4 h-4 mr-1"),
                    "Acknowledge",
                    on_click=AlertState.acknowledge_alert(alert["id"]),
                    class_name="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-green-700 bg-green-100 hover:bg-green-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500",
                ),
                rx.el.span("-", class_name="text-gray-400"),
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right",
        ),
        class_name="hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-0",
    )


def alerts_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            navbar(),
            rx.el.main(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "System Alerts",
                            class_name="text-2xl font-bold text-gray-800",
                        ),
                        rx.el.p(
                            "Monitor system warnings and critical events",
                            class_name="text-gray-500 mt-1",
                        ),
                        class_name="mb-8",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                rx.el.input(
                                    type="checkbox",
                                    default_checked=AlertState.active_filter,
                                    on_change=AlertState.set_active_filter,
                                    class_name="w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500 mr-2",
                                ),
                                "Show Active Only",
                                class_name="flex items-center text-sm font-medium text-gray-700",
                            ),
                            class_name="flex items-center bg-white p-2 rounded-lg border border-gray-200",
                        ),
                        rx.el.select(
                            rx.el.option("All Severities", value="all"),
                            rx.el.option("Critical", value="critical"),
                            rx.el.option("Warning", value="warning"),
                            on_change=AlertState.set_severity_filter,
                            class_name="px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 bg-white",
                        ),
                        class_name="flex gap-4 mb-6",
                    ),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Sensor",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Message",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Time",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Status",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Actions",
                                        class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    class_name="bg-gray-50 border-b border-gray-200",
                                )
                            ),
                            rx.el.tbody(
                                rx.cond(
                                    AlertState.alerts.length() > 0,
                                    rx.foreach(AlertState.alerts, alert_row),
                                    rx.el.tr(
                                        rx.el.td(
                                            "No alerts found matching criteria",
                                            col_span=5,
                                            class_name="px-6 py-8 text-center text-gray-500 italic",
                                        )
                                    ),
                                ),
                                class_name="bg-white divide-y divide-gray-200",
                            ),
                            class_name="min-w-full table-auto",
                        ),
                        class_name="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm",
                    ),
                    class_name="p-6 md:p-8 max-w-7xl mx-auto",
                ),
                class_name="flex-1 bg-gray-50 overflow-y-auto",
            ),
            class_name="flex flex-col flex-1 h-screen overflow-hidden",
        ),
        class_name="flex h-screen w-full font-['Inter']",
    )