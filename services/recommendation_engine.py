def generate_recommendations(pattern_analysis):

    recommendations = []

    if not pattern_analysis:
        return [
            "Not enough data to generate recommendations."
        ]

    for task_type, data in pattern_analysis.items():

        average_delay = data.get(
            "average_delay_minutes",
            0
        )

        frequency = data.get(
            "frequency",
            0
        )

        # 🔥 HIGH DELAY
        if average_delay > 120:

            recommendation = (
                f"⚠️ You frequently delay "
                f"{task_type} tasks by about "
                f"{average_delay:.0f} minutes. "
                f"Break them into smaller steps "
                f"and start earlier."
            )

        # 🔥 MODERATE DELAY
        elif average_delay > 60:

            recommendation = (
                f"⏰ You usually delay "
                f"{task_type} tasks by around "
                f"{average_delay:.0f} minutes. "
                f"Set reminders 15 minutes earlier "
                f"and avoid distractions."
            )

        # 🔥 LOW DELAY
        elif average_delay > 15:

            recommendation = (
                f"👍 You manage "
                f"{task_type} tasks fairly well. "
                f"Starting slightly earlier can "
                f"further improve consistency."
            )

        # 🔥 VERY GOOD
        else:

            recommendation = (
                f"✅ Excellent consistency in "
                f"{task_type} tasks. "
                f"Maintain your current routine."
            )

        recommendations.append(
            recommendation
        )

        # 🔥 ADDITIONAL PERSONALIZED SUGGESTIONS

        if task_type == "Meeting" and average_delay > 30:

            recommendations.append(
                "📅 Schedule meeting preparation "
                "15 minutes earlier."
            )

        elif task_type == "Exercise" and average_delay > 30:

            recommendations.append(
                "💪 Exercise is often postponed. "
                "Try scheduling it during your "
                "most productive hours."
            )

        elif task_type == "Deep Work" and average_delay > 30:

            recommendations.append(
                "🧠 Reduce distractions before "
                "starting Deep Work sessions."
            )

        elif task_type == "Reading" and average_delay > 30:

            recommendations.append(
                "📚 Consider shorter reading "
                "sessions to improve consistency."
            )

        # 🔥 REPETITIVE TASK ALERT
        if frequency >= 5:

            recommendations.append(
                f"🔄 {task_type} is a frequent "
                f"activity. Optimizing its schedule "
                f"can significantly improve "
                f"your productivity."
            )

    return recommendations