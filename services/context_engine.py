from datetime import datetime, timedelta
import os
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# OpenRouteService API Key
ORS_API_KEY = os.getenv(
    "ORS_API_KEY"
)

# Predefined destination coordinates
LOCATION_COORDS = {
    "Home": (12.9716, 77.5946),
    "Office": (12.9352, 77.6245),
    "Gym": (12.9279, 77.6271),
    "College": (12.9141, 77.6446),
    "Tech Park": (12.9177, 77.6228)
}


def estimate_travel_time(
        user_lat,
        user_lon,
        destination
):

    if not user_lat or not user_lon:
        return None

    if destination not in LOCATION_COORDS:
        return None

    dest_lat, dest_lon = (
        LOCATION_COORDS[destination]
    )

    try:

        headers = {
            "Authorization": ORS_API_KEY,
            "Content-Type": "application/json"
        }

        body = {
            "coordinates": [
                [user_lon, user_lat],
                [dest_lon, dest_lat]
            ]
        }

        response = requests.post(
            "https://api.openrouteservice.org/v2/directions/driving-car",
            headers=headers,
            json=body,
            timeout=10
        )

        data = response.json()

        print("ORS Response:", data)

        if "routes" not in data:
            return None

        summary = data["routes"][0]["summary"]

        distance_km = (
            summary["distance"] / 1000
        )

        duration_min = (
            summary["duration"] / 60
        )

        return {
            "distance":
                round(distance_km, 1),
            "duration":
                round(duration_min)
        }

    except Exception as e:

        print(
            "ORS Error:",
            e
        )

        return None


def generate_travel_advice(
        task,
        user_lat=None,
        user_lon=None
):

    # 🔥 No location → No travel advice
    location = task.get(
        "location",
        ""
    ).strip()

    if location == "":
        return ""

    # 🔥 Planned time
    planned_time = datetime.strptime(
        task["planned_time"].strip(),
        "%H:%M"
    )

    # 🔥 Default values
    travel_time = task.get(
        "travel_time",
        20
    )

    traffic = task.get(
        "traffic_level",
        "medium"
    )

    distance = None

    # 🔥 Use GPS if available
    if user_lat and user_lon:

        print(
            "📍 User Location:",
            user_lat,
            user_lon
        )

        travel_data = estimate_travel_time(
            user_lat,
            user_lon,
            location
        )

        if travel_data:

            travel_time = travel_data[
                "duration"
            ]

            distance = travel_data[
                "distance"
            ]

            if travel_time > 45:
                traffic = "high"

            elif travel_time > 25:
                traffic = "medium"

            else:
                traffic = "low"

    # 🔥 Calculate leave time
    leave_time = (
        planned_time -
        timedelta(
            minutes=travel_time
        )
    )

    # 🔥 HIGH TRAFFIC
    if traffic.lower() == "high":

        advice = (
            f"🚗 Heavy traffic expected near "
            f"{location}. "
        )

    # 🔥 MEDIUM TRAFFIC
    elif traffic.lower() == "medium":

        advice = (
            f"🚗 Moderate traffic expected towards "
            f"{location}. "
        )

    # 🔥 LOW TRAFFIC
    else:

        advice = (
            f"🚗 Traffic is light towards "
            f"{location}. "
        )

    # 🔥 Add distance if available
    if distance:

        advice += (
            f"Distance: "
            f"{distance:.1f} km. "
        )

    advice += (
        f"Estimated travel time: "
        f"{travel_time} mins. "
        f"Leave by "
        f"{leave_time.strftime('%H:%M')} "
        f"to reach on time."
    )

    # 🔥 GPS detected
    if user_lat and user_lon:

        advice += (
            " Current location detected."
        )

    return advice