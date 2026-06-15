from flask import (
    request,
    session
)

from database.db import (
    add_task_to_db,
    get_all_tasks,
    get_tasks_by_user,
    complete_task_in_db,
    update_task_in_db,
    delete_task_from_db,
    save_user_location,
    get_user_locations,
    get_location
)

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)

from services.behavior_tracker import calculate_delay
from services.pattern_analyzer import analyze_patterns
from services.recommendation_engine import generate_recommendations
from services.productivity_scorer import calculate_productivity_score
from services.delay_predictor import (
    predict_delay,
    get_delay_probability,
    generate_delay_message
)
from services.context_engine import generate_travel_advice
from services.insights_engine import generate_insights
from services.trend_analyzer import get_weekly_trend
from services.scheduler import suggest_best_time


# 🔥 TASK TYPE CLEANER (IMPORTANT)
def normalize_task_type(task_type):

    if not task_type:
        return "General"

    t = task_type.lower()

    if "meeting" in t:
        return "Meeting"
    elif "exercise" in t or "gym" in t:
        return "Exercise"
    elif "sleep" in t:
        return "Sleep"
    elif "work" in t:
        return "Deep Work"
    elif "entertainment" in t:
        return "Entertainment"
    elif "read" in t:
        return "Reading"
    else:
        return task_type.capitalize()


def register_routes(app):

    # ---------------- ADD TASK ----------------

    @app.route("/add_task", methods=["POST"])
    @app.route("/add_task", methods=["POST"])
    def add_task():

        data = request.json

        # 🔥 CLEAN TASK TYPE HERE
        task_type = normalize_task_type(
            data.get("task_type")
        )

        task = {
            "user_id":
                session["user_id"],

            "task_name":
                data.get("task_name"),

            "task_type":
                task_type,

            "priority":
                data.get("priority"),

            "difficulty":
                data.get("difficulty"),

            "location":
                data.get("location"),

            "travel_time":
                data.get(
                    "travel_time",
                    20
                ),

            "traffic_level":
                data.get(
                    "traffic_level",
                    "medium"
                ),

            "planned_time":
                data.get(
                    "planned_time"
                ),

            "planned_duration":
                data.get(
                    "planned_duration"
                ),

            "status":
                "pending"
        }

        add_task_to_db(task)

        return {
            "message":
                "Task added successfully",
            "task":
                task
        }
    # ---------------- GET TASKS ----------------

    @app.route("/tasks", methods=["GET"])
    def get_tasks():

        if "user_id" not in session:
            return {
                "tasks": []
            }

        tasks = get_tasks_by_user(
            session["user_id"]
        )

        return {
            "tasks": tasks
        }

    # ---------------- COMPLETE TASK ----------------

    @app.route("/complete_task/<int:task_id>", methods=["PUT"])
    def complete_task(task_id):

        data = request.json

        complete_task_in_db(
            task_id,
            data.get("actual_start"),
            data.get("actual_end"),
            data.get("actual_duration")
        )

        return {
            "message": "Task completed successfully",
            "task_id": task_id
        }

    @app.route(
        "/update_task/<int:task_id>",
        methods=["PUT"]
    )
    def update_task(task_id):

        data = request.json

        task_type = normalize_task_type(
            data.get("task_type")
        )

        update_task_in_db(
            task_id,
            data.get("task_name"),
            task_type,
            data.get("location"),
            data.get("planned_time")
        )

        return {
            "message":
                "Task updated successfully"
        }

    @app.route(
        "/delete_task/<int:task_id>",
        methods=["DELETE"]
    )
    def delete_task(task_id):

        delete_task_from_db(
            task_id
        )

        return {
            "message":
                "Task deleted successfully"
        }

    # ---------------- ANALYTICS ----------------

    @app.route("/analytics_data", methods=["GET"])
    def analytics_data():

        tasks = get_all_tasks()

        analytics = {}

        for task in tasks:

            if task.get("actual_start") and task.get("planned_time"):

                delay = calculate_delay(
                    task["planned_time"],
                    task["actual_start"]
                )

                # 🔥 NORMALIZE AGAIN (IMPORTANT)
                task_type = normalize_task_type(task.get("task_type"))

                if task_type not in analytics:
                    analytics[task_type] = []

                analytics[task_type].append(delay)

        final_data = {}

        for task_type, delays in analytics.items():

            if len(delays) > 0:
                avg_delay = sum(delays) / len(delays)
                final_data[task_type] = round(avg_delay, 2)

        return {
            "analytics": final_data
        }

    # ---------------- TRAVEL ----------------

    @app.route("/travel_advice/<int:task_id>", methods=["POST"])
    def travel_advice(task_id):

        data = request.json or {}

        user_lat = data.get("user_lat")
        user_lon = data.get("user_lon")

        tasks = get_all_tasks()

        task = next((t for t in tasks if t["id"] == task_id), None)

        if not task:
            return {"message": "Task not found"}, 404

        if not task.get("location") or task.get("travel_time", 0) == 0:
            return {"travel_advice": ""}

        advice = generate_travel_advice(task, user_lat, user_lon)

        return {"travel_advice": advice}

    @app.route("/save_location", methods=["POST"])
    def save_location():

        data = request.json

        save_user_location(
            data.get("location_type"),
            data.get("place_name"),
            data.get("latitude"),
            data.get("longitude")
        )

        return {
            "message":
                "Location saved successfully"
        }

    @app.route("/user_locations", methods=["GET"])
    def user_locations():

        return {
            "locations":
                get_user_locations()
        }

    @app.route("/delay_prediction", methods=["POST"])
    def delay_prediction():

        data = request.json

        task_type = normalize_task_type(
            data.get("task_type")
        )

        expected_delay = int(
            data.get(
                "expected_delay"
            ) or 0
        )

        prediction = predict_delay(
            task_type,
            expected_delay
        )

        probability = get_delay_probability(
            task_type,
            expected_delay
        )

        message = generate_delay_message(
            task_type,
            expected_delay
        )

        return {
            "prediction":
                prediction,
            "probability":
                probability,
            "message":
                message
        }

    # ---------------- OTHER ROUTES ----------------

    @app.route("/recommendations", methods=["GET"])
    def recommendations():

        tasks = get_all_tasks()
        analysis = analyze_patterns(tasks)

        return {
            "recommendations": generate_recommendations(analysis)
        }

    @app.route("/productivity_score", methods=["GET"])
    def productivity_score():

        tasks = get_all_tasks()

        return {
            "productivity": calculate_productivity_score(tasks)
        }

    @app.route("/insights", methods=["GET"])
    def insights():

        tasks = get_all_tasks()

        return {
            "insights": generate_insights(tasks)
        }

    @app.route("/weekly_trend", methods=["GET"])
    def weekly_trend():

        tasks = get_all_tasks()

        return {
            "trend": get_weekly_trend(tasks)
        }

    @app.route("/smart_schedule", methods=["GET"])
    def smart_schedule():

        tasks = get_all_tasks()

        return {
            "suggestion": suggest_best_time(tasks)
        }