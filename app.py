import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

from flask import (
    Flask,
    render_template,
    session,
    redirect
)

from routes.task_routes import (
    register_routes
)

from routes.auth_routes import (
    register_auth_routes
)

from database.db import (
    create_table,
    create_users_table,
    get_tasks_by_user
)

# ---------------- DATABASE ----------------

create_table()
create_users_table()

# ---------------- APP ----------------

app = Flask(__name__)

# Secret key for sessions
app.secret_key = "ai_life_delay_optimizer_secret"

# ---------------- REGISTER ROUTES ----------------

register_routes(app)
register_auth_routes(app)

# ---------------- HOME ROUTE ----------------

@app.route("/")
def home():

    # User already logged in
    if "user_id" in session:
        return redirect(
            "/dashboard"
        )

    # User not logged in
    return redirect(
            "/login"
        )

# ---------------- DASHBOARD ROUTE ----------------

@app.route("/dashboard")
def dashboard():

    # Protect dashboard
    if "user_id" not in session:
        return redirect(
            "/login"
        )

    return render_template(
        "index.html"
    )

# ---------------- PROFILE ROUTE ----------------

@app.route("/profile")
def profile():

    # Protect profile page
    if "user_id" not in session:
        return redirect(
            "/login"
        )

    user_id = session["user_id"]
    user_name = session["user_name"]

    tasks = get_tasks_by_user(
        user_id
    )

    total_tasks = len(tasks)

    completed_tasks = len([
        task
        for task in tasks
        if task["status"] == "completed"
    ])

    if total_tasks > 0:

        completion_rate = round(
            (
                completed_tasks
                / total_tasks
            ) * 100,
            1
        )

    else:

        completion_rate = 0

    productivity_score = completion_rate

    return render_template(
        "profile.html",
        user_name=user_name,
        user_id=user_id,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        completion_rate=completion_rate,
        productivity_score=productivity_score
    )

# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )