from flask import (
    request,
    render_template,
    redirect,
    session,
    url_for
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from database.db import (
    add_user,
    get_user_by_email
)


def register_auth_routes(app):

    app.secret_key = "your_secret_key"

    # ---------------- SIGNUP PAGE ----------------

    @app.route("/signup")
    def signup_page():

        return render_template(
            "signup.html"
        )

    # ---------------- LOGIN PAGE ----------------

    @app.route("/login")
    def login_page():

        return render_template(
            "login.html"
        )

    # ---------------- SIGNUP ----------------

    @app.route(
        "/register",
        methods=["POST"]
    )
    def register():

        name = request.form.get(
            "name"
        )

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )

        # 🔐 Hash password
        hashed_password = (
            generate_password_hash(
                password
            )
        )

        success = add_user(
            name,
            email,
            hashed_password
        )

        if not success:

            return {
                "message":
                    "Email already exists"
            }

        return redirect(
            url_for("login_page")
        )

    # ---------------- LOGIN ----------------

    @app.route(
        "/authenticate",
        methods=["POST"]
    )
    def authenticate():

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )

        user = get_user_by_email(
            email
        )

        if (
            not user
            or
            not check_password_hash(
                user["password"],
                password
            )
        ):

            return {
                "message":
                    "Invalid credentials"
            }

        session["user_id"] = user[
            "id"
        ]

        session["user_name"] = user[
            "name"
        ]

        return redirect(
            "/dashboard"
        )

    # ---------------- LOGOUT ----------------

    @app.route("/logout")
    def logout():

        session.clear()

        return redirect(
            "/login"
        )