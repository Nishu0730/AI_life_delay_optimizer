from services.behavior_tracker import calculate_delay


def analyze_patterns(tasks):

    task_type_delays = {}

    for task in tasks:

        if not task["actual_start"]:
            continue

        delay = calculate_delay(
            task["planned_time"],
            task["actual_start"]
        )

        task_type = task["task_type"]

        if task_type not in task_type_delays:
            task_type_delays[task_type] = []

        task_type_delays[task_type].append(delay)

    analysis = {}

    for task_type, delays in task_type_delays.items():

        average_delay = sum(delays) / len(delays)

        analysis[task_type] = {
            "average_delay_minutes": average_delay,
            "tasks_analyzed": len(delays)
        }

    return analysis