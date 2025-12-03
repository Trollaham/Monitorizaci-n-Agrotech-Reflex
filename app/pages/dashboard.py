import reflex as rx
from app.components.sidebar import sidebar
from app.components.navbar import navbar
from app.states.dashboard_state import DashboardState


def stat_card(title: str, value: str, icon: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(title, class_name="text-sm text-gray-500 font-medium"),
            rx.el.div(value, class_name=f"text-3xl font-bold text-{color}-600 mt-2"),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.icon(icon, class_name=f"w-8 h-8 text-{color}-600"),
            class_name=f"p-3 bg-{color}-50 rounded-full flex items-center justify-center",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm flex items-center justify-between hover:shadow-md transition-shadow",
    )


def type_stat_card(title: str, type_key: str, icon: str, color: str) -> rx.Component:
    stats = DashboardState.type_stats[type_key]
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"w-5 h-5 text-{color}-600 mb-2"),
            rx.el.h4(title, class_name="font-semibold text-gray-700"),
            class_name="flex items-center gap-2 mb-3",
        ),
        rx.el.div(
            rx.el.span(stats["avg"], class_name="text-2xl font-bold text-gray-900"),
            rx.el.span(
                stats["unit"], class_name="text-sm text-gray-500 ml-1 font-medium"
            ),
            class_name="flex items-baseline",
        ),
        rx.el.div(
            rx.el.span(
                f"{stats['active']}/{stats['total']} Active",
                class_name=f"text-xs font-medium text-{color}-600 bg-{color}-50 px-2 py-1 rounded-full",
            ),
            class_name="mt-3",
        ),
        class_name="bg-white p-5 rounded-xl border border-gray-200",
    )


def chart_section(title: str, data_key: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name="text-lg font-semibold text-gray-800 mb-4"),
        rx.el.div(
            rx.recharts.area_chart(
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3", vertical=False, stroke="#E5E7EB"
                ),
                rx.recharts.area(
                    data_key="value",
                    stroke=color,
                    fill=color,
                    fill_opacity=0.1,
                    stroke_width=2,
                ),
                rx.recharts.x_axis(
                    data_key="timestamp",
                    tick_line=False,
                    axis_line=False,
                    tick={"fontSize": 12, "fill": "#9CA3AF"},
                ),
                rx.recharts.y_axis(
                    tick_line=False,
                    axis_line=False,
                    tick={"fontSize": 12, "fill": "#9CA3AF"},
                ),
                data=DashboardState.chart_data[data_key],
                height=300,
                width="100%",
            ),
            class_name="h-[300px] w-full",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm",
    )


def activity_item(item: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                class_name="w-2 h-2 rounded-full bg-green-500 mt-1.5 flex-shrink-0"
            ),
            rx.el.div(
                rx.el.p(
                    f"{item['sensor']}", class_name="text-sm font-medium text-gray-900"
                ),
                rx.el.p(
                    f"{item['value']} {item['unit']}",
                    class_name="text-xs text-gray-500",
                ),
                class_name="ml-3 flex-1",
            ),
            rx.el.div(item["time"], class_name="text-xs text-gray-400 font-medium"),
            class_name="flex items-start",
        ),
        class_name="py-3 border-b border-gray-50 last:border-0",
    )


def dashboard_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            navbar(),
            rx.el.main(
                rx.el.div(
                    rx.el.h2(
                        "Dashboard Overview",
                        class_name="text-2xl font-bold text-gray-800 mb-6",
                    ),
                    rx.el.div(
                        stat_card(
                            "Active Sensors",
                            DashboardState.active_sensors.to_string(),
                            "activity",
                            "green",
                        ),
                        stat_card(
                            "Total Parcels",
                            DashboardState.total_parcels.to_string(),
                            "map",
                            "blue",
                        ),
                        stat_card(
                            "Active Alerts",
                            DashboardState.active_alerts.to_string(),
                            "bell",
                            "red",
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                type_stat_card(
                                    "Temperature",
                                    "temperature",
                                    "thermometer",
                                    "orange",
                                ),
                                type_stat_card(
                                    "Humidity", "humidity", "droplets", "blue"
                                ),
                                type_stat_card("Light", "light", "sun", "yellow"),
                                type_stat_card(
                                    "Soil Moisture", "soil_moisture", "sprout", "green"
                                ),
                                class_name="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8",
                            ),
                            rx.tabs.root(
                                rx.tabs.list(
                                    rx.tabs.trigger(
                                        "Temperature",
                                        value="temp",
                                        class_name="px-4 py-2 text-sm font-medium text-gray-600 hover:text-green-600 data-[state=active]:text-green-600 data-[state=active]:border-b-2 data-[state=active]:border-green-600 transition-colors outline-none",
                                    ),
                                    rx.tabs.trigger(
                                        "Humidity",
                                        value="hum",
                                        class_name="px-4 py-2 text-sm font-medium text-gray-600 hover:text-green-600 data-[state=active]:text-green-600 data-[state=active]:border-b-2 data-[state=active]:border-green-600 transition-colors outline-none",
                                    ),
                                    rx.tabs.trigger(
                                        "Light",
                                        value="light",
                                        class_name="px-4 py-2 text-sm font-medium text-gray-600 hover:text-green-600 data-[state=active]:text-green-600 data-[state=active]:border-b-2 data-[state=active]:border-green-600 transition-colors outline-none",
                                    ),
                                    class_name="flex border-b border-gray-200 mb-6",
                                ),
                                rx.tabs.content(
                                    chart_section(
                                        "Temperature Trends", "temperature", "#F97316"
                                    ),
                                    value="temp",
                                ),
                                rx.tabs.content(
                                    chart_section(
                                        "Humidity Trends", "humidity", "#3B82F6"
                                    ),
                                    value="hum",
                                ),
                                rx.tabs.content(
                                    chart_section(
                                        "Light Intensity", "light", "#EAB308"
                                    ),
                                    value="light",
                                ),
                                default_value="temp",
                            ),
                            class_name="flex flex-col",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.h3(
                                    "Recent Activity",
                                    class_name="text-lg font-semibold text-gray-800 mb-4",
                                ),
                                rx.el.div(
                                    rx.cond(
                                        DashboardState.recent_activity.length() > 0,
                                        rx.foreach(
                                            DashboardState.recent_activity,
                                            activity_item,
                                        ),
                                        rx.el.p(
                                            "No recent activity",
                                            class_name="text-sm text-gray-500 py-4 text-center",
                                        ),
                                    ),
                                    class_name="flex flex-col",
                                ),
                                class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm h-fit sticky top-6",
                            ),
                            class_name="w-full md:w-80 shrink-0",
                        ),
                        class_name="flex flex-col md:flex-row gap-8",
                    ),
                    class_name="p-6 md:p-8 max-w-7xl mx-auto",
                ),
                class_name="flex-1 bg-gray-50 overflow-y-auto",
            ),
            class_name="flex flex-col flex-1 h-screen overflow-hidden",
        ),
        class_name="flex h-screen w-full font-['Inter']",
    )