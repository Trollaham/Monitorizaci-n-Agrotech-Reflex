import reflex as rx
from app.components.sidebar import sidebar
from app.components.navbar import navbar
from app.states.auth_state import AuthState


def profile_info_row(label: str, value: str) -> rx.Component:
    return rx.el.div(
        rx.el.dt(label, class_name="text-sm font-medium text-gray-500"),
        rx.el.dd(
            value,
            class_name="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2 font-medium",
        ),
        class_name="py-4 sm:grid sm:grid-cols-3 sm:gap-4 border-b border-gray-100 last:border-0",
    )


def profile_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            navbar(),
            rx.el.main(
                rx.el.div(
                    rx.el.h2(
                        "User Profile",
                        class_name="text-2xl font-bold text-gray-800 mb-6",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "user", class_name="w-12 h-12 text-gray-400"
                                    ),
                                    class_name="h-24 w-24 rounded-full bg-gray-100 flex items-center justify-center mb-4 mx-auto",
                                ),
                                rx.el.h3(
                                    rx.cond(
                                        AuthState.user, AuthState.user.username, ""
                                    ),
                                    class_name="text-xl font-bold text-center text-gray-900",
                                ),
                                rx.el.p(
                                    rx.cond(AuthState.user, AuthState.user.role, ""),
                                    class_name="text-sm text-center text-gray-500 uppercase tracking-wide mt-1",
                                ),
                                class_name="p-6 border-b border-gray-100 bg-gray-50/50",
                            ),
                            rx.el.dl(
                                profile_info_row(
                                    "Full Name",
                                    rx.cond(
                                        AuthState.user, AuthState.user.username, ""
                                    ),
                                ),
                                profile_info_row(
                                    "Email Address",
                                    rx.cond(AuthState.user, AuthState.user.email, ""),
                                ),
                                profile_info_row(
                                    "Role",
                                    rx.cond(AuthState.user, AuthState.user.role, ""),
                                ),
                                profile_info_row(
                                    "Account Created",
                                    rx.cond(
                                        AuthState.user,
                                        AuthState.user.created_at.to_string(),
                                        "",
                                    ),
                                ),
                                class_name="px-6 py-2",
                            ),
                            class_name="bg-white shadow-sm rounded-xl border border-gray-200 overflow-hidden",
                        ),
                        class_name="max-w-2xl",
                    ),
                    class_name="p-6 md:p-8",
                ),
                class_name="flex-1 bg-gray-50 overflow-y-auto",
            ),
            class_name="flex flex-col flex-1 h-screen overflow-hidden",
        ),
        class_name="flex h-screen w-full font-['Inter']",
    )