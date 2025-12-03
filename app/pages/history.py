import reflex as rx
from app.components.sidebar import sidebar
from app.components.navbar import navbar
from app.states.history_state import HistoryState


def history_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            navbar(),
            rx.el.main(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Data History",
                            class_name="text-2xl font-bold text-gray-800",
                        ),
                        rx.el.p(
                            "Analyze historical sensor trends",
                            class_name="text-gray-500 mt-1",
                        ),
                        class_name="mb-8",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.select(
                                rx.el.option("Temperature", value="temperature"),
                                rx.el.option("Humidity", value="humidity"),
                                rx.el.option("Light", value="light"),
                                rx.el.option("Soil Moisture", value="soil_moisture"),
                                value=HistoryState.sensor_type,
                                on_change=HistoryState.set_sensor_type,
                                class_name="px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 bg-white",
                            ),
                            rx.el.select(
                                rx.el.option("Last 24 Hours", value="1"),
                                rx.el.option("Last 7 Days", value="7"),
                                rx.el.option("Last 30 Days", value="30"),
                                value=HistoryState.days_range,
                                on_change=HistoryState.set_days_range,
                                class_name="px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 bg-white",
                            ),
                            class_name="flex gap-4",
                        ),
                        rx.el.button(
                            rx.icon("download", class_name="w-4 h-4 mr-2"),
                            "Export CSV",
                            on_click=HistoryState.export_csv,
                            class_name="flex items-center px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-medium transition-colors shadow-sm",
                        ),
                        class_name="flex justify-between items-center mb-8",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Trend Analysis",
                            class_name="text-lg font-semibold text-gray-800 mb-4",
                        ),
                        rx.el.div(
                            rx.recharts.scatter_chart(
                                rx.recharts.cartesian_grid(
                                    stroke_dasharray="3 3",
                                    vertical=False,
                                    stroke="#E5E7EB",
                                ),
                                rx.recharts.x_axis(
                                    data_key="timestamp",
                                    type_="category",
                                    tick={"fontSize": 12, "fill": "#9CA3AF"},
                                    allow_dupes=True,
                                ),
                                rx.recharts.y_axis(
                                    data_key="value",
                                    tick={"fontSize": 12, "fill": "#9CA3AF"},
                                ),
                                rx.recharts.tooltip(
                                    cursor={"strokeDasharray": "3 3"},
                                    content_style={
                                        "backgroundColor": "white",
                                        "borderRadius": "8px",
                                        "border": "1px solid #E5E7EB",
                                        "boxShadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                                    },
                                ),
                                rx.recharts.scatter(
                                    name="Reading",
                                    data=HistoryState.chart_data,
                                    fill="#10B981",
                                ),
                                height=400,
                                width="100%",
                            ),
                            class_name="h-[400px] w-full",
                        ),
                        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm mb-8",
                    ),
                    class_name="p-6 md:p-8 max-w-7xl mx-auto",
                ),
                class_name="flex-1 bg-gray-50 overflow-y-auto",
            ),
            class_name="flex flex-col flex-1 h-screen overflow-hidden",
        ),
        class_name="flex h-screen w-full font-['Inter']",
    )