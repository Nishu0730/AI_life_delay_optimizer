from datetime import datetime


def calculate_delay(planned_time, actual_start):

    try:
        # 🔥 Handle empty values
        if not planned_time or not actual_start:
            return 0

        # 🔥 Remove extra spaces
        planned_time = str(planned_time).strip()
        actual_start = str(actual_start).strip()

        # 🔥 Handle both formats
        # "18:30" and "18:30:00"

        if len(planned_time) >= 8:
            planned = datetime.strptime(
                planned_time[:8],
                "%H:%M:%S"
            )
        else:
            planned = datetime.strptime(
                planned_time,
                "%H:%M"
            )

        if len(actual_start) >= 8:
            actual = datetime.strptime(
                actual_start[:8],
                "%H:%M:%S"
            )
        else:
            actual = datetime.strptime(
                actual_start,
                "%H:%M"
            )

        delay = actual - planned

        delay_minutes = max(
            0,
            delay.total_seconds() / 60
        )

        return delay_minutes

    except Exception as e:
        print(
            "❌ Time parsing error:",
            repr(planned_time),
            repr(actual_start),
            e
        )
        return 0