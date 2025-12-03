import reflex as rx
from app.components.sidebar import sidebar
from app.components.navbar import navbar
from app.states.parcel_state import ParcelState
from app.models import Parcel


def form_field(
    label: str,
    placeholder: str,
    value_var: rx.Var,
    on_change_handler: rx.event.EventType,
    type_: str = "text",
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.input(
            type=type_,
            placeholder=placeholder,
            default_value=value_var,
            on_change=on_change_handler,
            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent",
        ),
        class_name="mb-4",
    )


def parcel_dialog(
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
                    ParcelState.error_message != "",
                    rx.el.div(
                        ParcelState.error_message,
                        class_name="mb-4 p-3 bg-red-50 text-red-600 text-sm rounded-lg border border-red-100",
                    ),
                ),
                rx.el.div(
                    form_field(
                        "Parcel Name",
                        "e.g., North Field",
                        ParcelState.name,
                        ParcelState.set_name,
                    ),
                    form_field(
                        "Location",
                        "e.g., Sector A, Zone 1",
                        ParcelState.location,
                        ParcelState.set_location,
                    ),
                    form_field(
                        "Area (hectares)",
                        "e.g., 15.5",
                        ParcelState.area.to_string(),
                        ParcelState.set_area,
                        "number",
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
                        "Save Parcel",
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
                    "Delete Parcel", class_name="text-xl font-bold text-gray-900 mb-2"
                ),
                rx.radix.primitives.dialog.description(
                    "Are you sure you want to delete this parcel? This action cannot be undone and will remove all associated sensors.",
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
                        on_click=ParcelState.delete_parcel,
                        class_name="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-medium transition-colors shadow-sm",
                    ),
                    class_name="flex justify-end gap-3",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-2xl p-6 w-full max-w-sm z-50",
            ),
        ),
        open=ParcelState.is_delete_open,
        on_open_change=lambda open: rx.cond(
            open, rx.noop(), ParcelState.close_delete_dialog()
        ),
    )


def parcel_card(parcel: Parcel) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "map-pin",
                    class_name="w-10 h-10 text-green-600 bg-green-50 p-2 rounded-lg mb-3",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("pencil", class_name="w-4 h-4"),
                        on_click=ParcelState.open_edit_dialog(parcel),
                        class_name="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors",
                    ),
                    rx.el.button(
                        rx.icon("trash-2", class_name="w-4 h-4"),
                        on_click=ParcelState.open_delete_dialog(parcel.id),
                        class_name="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors",
                    ),
                    class_name="flex gap-1 absolute top-4 right-4",
                ),
                class_name="relative",
            ),
            rx.el.h3(parcel.name, class_name="text-lg font-bold text-gray-800 mb-1"),
            rx.el.p(
                parcel.location,
                class_name="text-sm text-gray-500 mb-4 flex items-center gap-1",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Area",
                        class_name="text-xs text-gray-500 uppercase font-semibold",
                    ),
                    rx.el.p(
                        f"{parcel.area} ha", class_name="font-medium text-gray-800"
                    ),
                    class_name="flex flex-col",
                ),
                rx.el.div(
                    rx.el.span(
                        "Sensors",
                        class_name="text-xs text-gray-500 uppercase font-semibold",
                    ),
                    rx.el.p(
                        ParcelState.sensor_counts[parcel.id],
                        class_name="font-medium text-gray-800",
                    ),
                    class_name="flex flex-col items-end",
                ),
                class_name="flex justify-between items-center pt-4 border-t border-gray-100",
            ),
            class_name="p-6",
        ),
        class_name="bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200",
    )


def parcels_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            navbar(),
            rx.el.main(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h2(
                                "My Parcels",
                                class_name="text-2xl font-bold text-gray-800",
                            ),
                            rx.el.p(
                                "Manage your land and agricultural zones",
                                class_name="text-gray-500 mt-1",
                            ),
                            class_name="flex-1",
                        ),
                        rx.el.button(
                            rx.icon("plus", class_name="w-5 h-5 mr-2"),
                            "Add Parcel",
                            on_click=ParcelState.open_add_dialog,
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
                                placeholder="Search parcels...",
                                on_change=ParcelState.set_search,
                                class_name="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent",
                            ),
                            class_name="relative max-w-md",
                        ),
                        class_name="mb-8",
                    ),
                    rx.cond(
                        ParcelState.parcels.length() > 0,
                        rx.el.div(
                            rx.foreach(ParcelState.parcels, parcel_card),
                            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                        ),
                        rx.el.div(
                            rx.icon("map", class_name="w-16 h-16 text-gray-300 mb-4"),
                            rx.el.h3(
                                "No parcels found",
                                class_name="text-lg font-medium text-gray-900",
                            ),
                            rx.el.p(
                                "Get started by adding your first parcel",
                                class_name="text-gray-500 mt-2",
                            ),
                            class_name="flex flex-col items-center justify-center py-20 bg-gray-50 rounded-2xl border border-dashed border-gray-300",
                        ),
                    ),
                    parcel_dialog(
                        ParcelState.is_add_open,
                        "Add New Parcel",
                        lambda open: rx.cond(
                            open, rx.noop(), ParcelState.close_add_dialog()
                        ),
                        ParcelState.add_parcel,
                    ),
                    parcel_dialog(
                        ParcelState.is_edit_open,
                        "Edit Parcel",
                        lambda open: rx.cond(
                            open, rx.noop(), ParcelState.close_edit_dialog()
                        ),
                        ParcelState.update_parcel,
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