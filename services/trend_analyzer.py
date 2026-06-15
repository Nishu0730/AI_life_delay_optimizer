def get_weekly_trend(tasks):

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    trend = {day: 0 for day in days}
    counts = {day: 0 for day in days}

    for task in tasks:

        if task.get("status") != "completed":
            continue

        if not task.get("actual_start") or not task.get("planned_time"):
            continue

        try:
            # distribute tasks across days (simulation)
            day_index = task["id"] % 7
            day = days[day_index]

            ph, pm = map(int, task["planned_time"].split(":"))
            ah, am = map(int, task["actual_start"].split(":"))

            planned_min = ph * 60 + pm
            actual_min = ah * 60 + am

            delay = max(0, actual_min - planned_min)

            trend[day] += delay
            counts[day] += 1

        except:
            continue  # skip bad data safely

    # 🔥 CALCULATE AVERAGE

    for day in days:
        if counts[day] > 0:
            trend[day] = round(trend[day] / counts[day], 2)

    # 🔥 HANDLE LOW DATA (SMOOTHING)

    non_zero_days = [trend[d] for d in days if trend[d] > 0]

    if len(non_zero_days) == 0:
        # no completed tasks
        return {day: 0 for day in days}

    avg = sum(non_zero_days) / len(non_zero_days)

    for day in days:
        if trend[day] == 0:
            # fill missing days with average
            trend[day] = round(avg, 2)

    return trend