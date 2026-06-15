def generate_insights(tasks):

    insights = []

    delays = {}
    counts = {}

    for task in tasks:

        if task["status"] != "completed":
            continue

        if not task["actual_start"]:
            continue

        planned = task["planned_time"]
        actual = task["actual_start"]

        ph, pm = map(int, planned.split(":"))
        ah, am = map(int, actual.split(":"))

        planned_min = ph * 60 + pm
        actual_min = ah * 60 + am

        delay = max(0, actual_min - planned_min)

        task_type = task["task_type"]

        delays[task_type] = (
            delays.get(task_type, 0) + delay
        )

        counts[task_type] = (
            counts.get(task_type, 0) + 1
        )

    # No completed tasks
    if not delays:
        return [
            "Not enough data to generate insights."
        ]

    # Average delays
    avg_delay = {}

    for task_type in delays:

        avg_delay[task_type] = (
            delays[task_type] /
            counts[task_type]
        )

    # 🔥 Highest delay
    worst_task = max(
        avg_delay,
        key=avg_delay.get
    )

    worst_delay = round(
        avg_delay[worst_task]
    )

    insights.append(
        f"You delay {worst_task} tasks the most "
        f"(average {worst_delay} mins)."
    )

    # 🔥 Lowest delay
    best_task = min(
        avg_delay,
        key=avg_delay.get
    )

    best_delay = round(
        avg_delay[best_task]
    )

    insights.append(
        f"You are most consistent in "
        f"{best_task} tasks "
        f"(average delay {best_delay} mins)."
    )

    # 🔥 Overall delay
    overall = (
        sum(avg_delay.values()) /
        len(avg_delay)
    )

    if overall > 120:

        insights.append(
            "Your delay pattern is high. "
            "Try breaking large tasks into "
            "smaller steps."
        )

    elif overall > 60:

        insights.append(
            "Your delays are moderate. "
            "Starting tasks a little earlier "
            "can improve productivity."
        )

    else:

        insights.append(
            "Your delays are well managed. "
            "You are maintaining a good routine."
        )

    # 🔥 Personalized insight
    if worst_task == "Meeting":

        insights.append(
            "You frequently postpone meetings. "
            "Set reminders 15 minutes earlier."
        )

    elif worst_task == "Exercise":

        insights.append(
            "Exercise is your most delayed activity. "
            "Try scheduling it during your most "
            "productive hours."
        )

    elif worst_task == "Deep Work":

        insights.append(
            "Deep Work sessions are often delayed. "
            "Reduce distractions before starting."
        )

    elif worst_task == "Reading":

        insights.append(
            "Reading tasks are frequently postponed. "
            "Consider shorter reading sessions."
        )

    # 🔥 Positive reinforcement
    if best_delay <= 15:

        insights.append(
            f"Excellent consistency in "
            f"{best_task}. "
            f"Use similar habits for other tasks."
        )

    return insights