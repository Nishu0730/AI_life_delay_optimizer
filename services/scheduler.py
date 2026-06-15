def suggest_best_time(tasks):

    delays = {}

    for task in tasks:

        # only consider completed tasks
        if task.get("status") != "completed":
            continue

        if not task.get("actual_start") or not task.get("planned_time"):
            continue

        try:
            # extract hour
            hour = int(task["planned_time"].split(":")[0])

            ph, pm = map(int, task["planned_time"].split(":"))
            ah, am = map(int, task["actual_start"].split(":"))

            planned_min = ph * 60 + pm
            actual_min = ah * 60 + am

            delay = max(0, actual_min - planned_min)

            if hour not in delays:
                delays[hour] = []

            delays[hour].append(delay)

        except:
            continue  # skip bad data safely

    # 🔥 CASE 1: NO DATA

    if not delays:
        return "Not enough data yet. Complete more tasks to get smart scheduling insights."

    # 🔥 CALCULATE AVERAGE DELAYS

    avg_delays = {}

    for hour, d_list in delays.items():
        avg_delays[hour] = sum(d_list) / len(d_list)

    # 🔥 FIND BEST HOUR (least delay)

    best_hour = min(avg_delays, key=avg_delays.get)

    # 🔥 CONVERT TO HUMAN FRIENDLY TIME

    if 5 <= best_hour < 12:
        period = "morning"
    elif 12 <= best_hour < 17:
        period = "afternoon"
    elif 17 <= best_hour < 21:
        period = "evening"
    else:
        period = "night"

    # 🔥 FINAL MESSAGE

    return (
        f"You are most productive around {best_hour}:00 "
        f"({period}). Schedule important tasks then."
    )