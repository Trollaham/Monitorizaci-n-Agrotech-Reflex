import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("leaf", class_name="w-12 h-12 text-green-600 mb-4 mx-auto"),
                rx.el.h1(
                    "Welcome Back",
                    class_name="text-2xl font-bold text-center text-gray-900 mb-2",
                ),
                rx.el.p(
                    "Sign in to monitor your crops",
                    class_name="text-center text-gray-600 mb-8",
                ),
                rx.el.div(
                    rx.el.label(
                        "Username",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        placeholder="Enter your username",
                        on_change=AuthState.set_username,
                        class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition-all",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Password",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="password",
                        placeholder="Enter your password",
                        on_change=AuthState.set_password,
                        class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition-all",
                    ),
                    class_name="mb-6",
                ),
                rx.cond(
                    AuthState.error_message != "",
                    rx.el.div(
                        AuthState.error_message,
                        class_name="p-3 mb-4 text-sm text-red-600 bg-red-50 rounded-lg",
                    ),
                ),
                rx.el.button(
                    "Sign In",
                    on_click=AuthState.login,
                    class_name="w-full py-2.5 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 transition-colors shadow-sm hover:shadow-md",
                ),
                rx.el.div(
                    "Don't have an account? ",
                    rx.el.a(
                        "Register here",
                        href="/register",
                        class_name="text-green-600 font-medium hover:underline",
                    ),
                    class_name="mt-6 text-center text-sm text-gray-600",
                ),
                class_name="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md border border-gray-100",
            ),
            class_name="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-emerald-100 p-4",
        )
    )


def register_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("leaf", class_name="w-12 h-12 text-green-600 mb-4 mx-auto"),
                rx.el.h1(
                    "Create Account",
                    class_name="text-2xl font-bold text-center text-gray-900 mb-2",
                ),
                rx.el.p(
                    "Join Agrotech today", class_name="text-center text-gray-600 mb-8"
                ),
                rx.el.div(
                    rx.el.label(
                        "Username",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        placeholder="Choose a username",
                        on_change=AuthState.set_username,
                        class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition-all",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Email",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="email",
                        placeholder="your@email.com",
                        on_change=AuthState.set_email,
                        class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition-all",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Role",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.select(
                        rx.el.option("Farmer", value="farmer"),
                        rx.el.option("Technician", value="technician"),
                        on_change=AuthState.set_role,
                        class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition-all bg-white",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Password",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="password",
                        placeholder="Choose a strong password",
                        on_change=AuthState.set_password,
                        class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition-all",
                    ),
                    class_name="mb-6",
                ),
                rx.cond(
                    AuthState.error_message != "",
                    rx.el.div(
                        AuthState.error_message,
                        class_name="p-3 mb-4 text-sm text-red-600 bg-red-50 rounded-lg",
                    ),
                ),
                rx.el.button(
                    "Create Account",
                    on_click=AuthState.register,
                    class_name="w-full py-2.5 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 transition-colors shadow-sm hover:shadow-md",
                ),
                rx.el.div(
                    "Already have an account? ",
                    rx.el.a(
                        "Sign in here",
                        href="/",
                        class_name="text-green-600 font-medium hover:underline",
                    ),
                    class_name="mt-6 text-center text-sm text-gray-600",
                ),
                class_name="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md border border-gray-100",
            ),
            class_name="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-emerald-100 p-4",
        )
    )