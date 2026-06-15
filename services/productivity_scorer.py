from services.behavior_tracker import calculate_delay


def calculate_productivity_score(tasks):

    total_tasks = len(tasks)

    if total_tasks == 0:
        return {
            "score": 0,
            "completion_rate": 0,
            "average_delay": 0
        }

    completed_tasks = 0
    total_delay = 0

    for task in tasks:

        if task["status"] == "completed":

            completed_tasks += 1

            delay = calculate_delay(
                task["planned_time"],
                task["actual_start"]
            )

            total_delay += delay

    completion_rate = (completed_tasks / total_tasks) * 100

    average_delay = (
        total_delay / completed_tasks
        if completed_tasks > 0 else 0
    )

    score = completion_rate - (average_delay / 5)

    score = max(0, min(100, score))

    return {
        "score": round(score, 2),
        "completion_rate": round(completion_rate, 2),
        "average_delay": round(average_delay, 2)
    }