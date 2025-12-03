import reflex as rx
from app.components.sidebar import sidebar
from app.components.navbar import navbar
from app.states.sensor_state import SensorState
from app.models import Sensor


def form_field(label: str, content: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        content,
        class_name="mb-4",
    )


def sensor_dialog(
    is_open: rx.Var,
    title: str,
    on_open_change: rx.event.EventType,
    on_submit: rx.event.EventType,
) -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 animate-overlay-show"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    title, class_name="text-xl font-bold text-gray-900 mb-4"
                ),
                rx.cond(
                    SensorState.error_message != "",
                    rx.el.div(
                        SensorState.error_message,
                        class_name="mb-4 p-3 bg-red-50 text-red-600 text-sm rounded-lg border border-red-100",
                    ),
                ),
                rx.el.div(
                    form_field(
                        "Sensor Name",
                        rx.el.input(
                            placeholder="e.g., Soil Sensor A1",
                            default_value=SensorState.name,
                            on_change=SensorState.set_name,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500",
                        ),
                    ),
                    form_field(
                        "Unique ID",
                        rx.el.input(
                            placeholder="e.g., SENS-001",
                            default_value=SensorState.unique_id,
                            on_change=SensorState.set_unique_id,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500",
                        ),
                    ),
                    rx.el.div(
                        form_field(
                            "Type",
                            rx.el.select(
                                rx.el.option("Temperature", value="temperature"),
                                rx.el.option("Humidity", value="humidity"),
                                rx.el.option("Light", value="light"),
                                rx.el.option("Soil Moisture", value="soil_moisture"),
                                rx.el.option("CO2", value="co2"),
                                rx.el.option("VOC", value="voc"),
                                rx.el.option("NOx", value="nox"),
                                value=SensorState.sensor_type,
                                on_change=SensorState.set_sensor_type,
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 bg-white",
                            ),
                        ),
                        form_field(
                            "Parcel",
                            rx.el.select(
                                rx.foreach(
                                    SensorState.parcels,
                                    lambda p: rx.el.option(p.name, value=p.id),
                                ),
                                value=SensorState.parcel_id.to_string(),
                                on_change=SensorState.set_parcel_id,
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 bg-white",
                            ),
                        ),
                        class_name="grid grid-cols-2 gap-4",
                    ),
                    form_field(
                        "Status",
                        rx.el.select(
                            rx.el.option("Active", value="active"),
                            rx.el.option("Inactive", value="inactive"),
                            rx.el.option("Maintenance", value="maintenance"),
                            value=SensorState.status,
                            on_change=SensorState.set_status,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 bg-white",
                        ),
                    ),
                    rx.el.div(
                        form_field(
                            "Min Threshold",
                            rx.el.input(
                                type="number",
                                step="0.1",
                                placeholder="Min value",
                                default_value=SensorState.threshold_min,
                                on_change=SensorState.set_threshold_min,
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500",
                            ),
                        ),
                        form_field(
                            "Max Threshold",
                            rx.el.input(
                                type="number",
                                step="0.1",
                                placeholder="Max value",
                                default_value=SensorState.threshold_max,
                                on_change=SensorState.set_threshold_max,
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500",
                            ),
                        ),
                        class_name="grid grid-cols-2 gap-4",
                    ),
                    class_name="flex flex-col",
                ),
                rx.el.div(
                    rx.radix.primitives.dialog.close(
                        rx.el.button(
                            "Cancel",
                            class_name="px-4 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 font-medium transition-colors",
                        )
                    ),
                    rx.el.button(
                        "Save Sensor",
                        on_click=on_submit,
                        class_name="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium transition-colors shadow-sm",
                    ),
                    class_name="flex justify-end gap-3 mt-6",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-2xl p-6 w-full max-w-md z-50 animate-content-show",
            ),
        ),
        open=is_open,
        on_open_change=on_open_change,
    )


def delete_confirmation_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    "Delete Sensor", class_name="text-xl font-bold text-gray-900 mb-2"
                ),
                rx.radix.primitives.dialog.description(
                    "Are you sure you want to delete this sensor? This action cannot be undone and will delete all collected data.",
                    class_name="text-gray-500 mb-6",
                ),
                rx.el.div(
                    rx.radix.primitives.dialog.close(
                        rx.el.button(
                            "Cancel",
                            class_name="px-4 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 font-medium transition-colors",
                        )
                    ),
                    rx.el.button(
                        "Delete",
                        on_click=SensorState.delete_sensor,
                        class_name="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-medium transition-colors shadow-sm",
                    ),
                    class_name="flex justify-end gap-3",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-2xl p-6 w-full max-w-sm z-50",
            ),
        ),
        open=SensorState.is_delete_open,
        on_open_change=lambda open: rx.cond(
            open, rx.noop(), SensorState.close_delete_dialog()
        ),
    )


def sensor_row(sensor: Sensor) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.match(
                    sensor.sensor_type,
                    (
                        "temperature",
                        rx.icon("thermometer", class_name="w-5 h-5 text-orange-500"),
                    ),
                    (
                        "humidity",
                        rx.icon("droplets", class_name="w-5 h-5 text-blue-500"),
                    ),
                    ("light", rx.icon("sun", class_name="w-5 h-5 text-yellow-500")),
                    (
                        "soil_moisture",
                        rx.icon("sprout", class_name="w-5 h-5 text-green-500"),
                    ),
                    ("co2", rx.icon("wind", class_name="w-5 h-5 text-slate-500")),
                    ("voc", rx.icon("cloud", class_name="w-5 h-5 text-gray-500")),
                    ("nox", rx.icon("flame", class_name="w-5 h-5 text-red-500")),
                    rx.icon("activity", class_name="w-5 h-5 text-gray-400"),
                ),
                rx.el.div(
                    rx.el.p(sensor.name, class_name="font-medium text-gray-900"),
                    rx.el.p(sensor.unique_id, class_name="text-xs text-gray-500"),
                    class_name="ml-3",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                sensor.sensor_type,
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 capitalize",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.cond(
                sensor.status == "active",
                rx.el.span(
                    "Active",
                    class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800",
                ),
                rx.cond(
                    sensor.status == "inactive",
                    rx.el.span(
                        "Inactive",
                        class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800",
                    ),
                    rx.el.span(
                        "Maintenance",
                        class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800",
                    ),
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td("--", class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500"),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("pencil", class_name="w-4 h-4"),
                    on_click=SensorState.open_edit_dialog(sensor),
                    class_name="p-1.5 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-md transition-colors mr-1",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="w-4 h-4"),
                    on_click=SensorState.open_delete_dialog(sensor.id),
                    class_name="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors",
                ),
                class_name="flex justify-end",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name="hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-0",
    )


def sensors_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            navbar(),
            rx.el.main(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h2(
                                "Device Management",
                                class_name="text-2xl font-bold text-gray-800",
                            ),
                            rx.el.p(
                                "Monitor and configure your field sensors",
                                class_name="text-gray-500 mt-1",
                            ),
                            class_name="flex-1",
                        ),
                        rx.el.button(
                            rx.icon("plus", class_name="w-5 h-5 mr-2"),
                            "Add Sensor",
                            on_click=SensorState.open_add_dialog,
                            class_name="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium transition-colors shadow-sm",
                        ),
                        class_name="flex justify-between items-start mb-8",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "search",
                                class_name="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                            ),
                            rx.el.input(
                                placeholder="Search sensors...",
                                on_change=SensorState.set_search,
                                class_name="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500",
                            ),
                            class_name="relative flex-1 max-w-xs",
                        ),
                        rx.el.select(
                            rx.el.option("All Types", value="all"),
                            rx.el.option("Temperature", value="temperature"),
                            rx.el.option("Humidity", value="humidity"),
                            rx.el.option("Light", value="light"),
                            rx.el.option("Soil Moisture", value="soil_moisture"),
                            rx.el.option("CO2", value="co2"),
                            rx.el.option("VOC", value="voc"),
                            rx.el.option("NOx", value="nox"),
                            on_change=SensorState.set_filter_type,
                            class_name="px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 bg-white",
                        ),
                        rx.el.select(
                            rx.el.option("All Status", value="all"),
                            rx.el.option("Active", value="active"),
                            rx.el.option("Inactive", value="inactive"),
                            on_change=SensorState.set_filter_status,
                            class_name="px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 bg-white",
                        ),
                        class_name="flex gap-4 mb-6 flex-wrap",
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
                                        "Type",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Status",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Last Reading",
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
                                rx.foreach(SensorState.sensors, sensor_row),
                                class_name="bg-white divide-y divide-gray-200",
                            ),
                            class_name="min-w-full table-auto",
                        ),
                        class_name="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm",
                    ),
                    sensor_dialog(
                        SensorState.is_add_open,
                        "Add New Sensor",
                        lambda open: rx.cond(
                            open, rx.noop(), SensorState.close_add_dialog()
                        ),
                        SensorState.add_sensor,
                    ),
                    sensor_dialog(
                        SensorState.is_edit_open,
                        "Edit Sensor",
                        lambda open: rx.cond(
                            open, rx.noop(), SensorState.close_edit_dialog()
                        ),
                        SensorState.update_sensor,
                    ),
                    delete_confirmation_dialog(),
                    class_name="p-6 md:p-8 max-w-7xl mx-auto",
                ),
                class_name="flex-1 bg-gray-50 overflow-y-auto",
            ),
            class_name="flex flex-col flex-1 h-screen overflow-hidden",
        ),
        class_name="flex h-screen w-full font-['Inter']",
    )