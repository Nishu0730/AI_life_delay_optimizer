from sklearn.tree import DecisionTreeClassifier
import pandas as pd


def train_model():

    # Sample training data
    data = {
        "task_type": [
            1, 1, 1,
            2, 2, 2,
            3, 3,
            4, 4
        ],
        "delay": [
            120, 90, 60,
            10, 20, 30,
            45, 70,
            15, 120
        ],
        "label": [
            1, 1, 1,
            0, 0, 0,
            1, 1,
            0, 1
        ]
    }

    df = pd.DataFrame(data)

    X = df[[
        "task_type",
        "delay"
    ]]

    y = df["label"]

    model = DecisionTreeClassifier(
        random_state=42
    )

    model.fit(X, y)

    return model


def get_task_type_id(task_type):

    mapping = {
        "Meeting": 1,
        "Exercise": 2,
        "Deep Work": 3,
        "Reading": 4,
        "Sleep": 5,
        "Entertainment": 6
    }

    return mapping.get(
        task_type,
        0
    )


def predict_delay(
        task_type,
        expected_delay
):

    model = train_model()

    task_id = get_task_type_id(
        task_type
    )

    prediction = model.predict([
        [
            task_id,
            expected_delay
        ]
    ])

    return int(
        prediction[0]
    )


def get_delay_probability(
        task_type,
        expected_delay
):

    model = train_model()

    task_id = get_task_type_id(
        task_type
    )

    probability = model.predict_proba([
        [
            task_id,
            expected_delay
        ]
    ])

    late_probability = round(
        probability[0][1] * 100
    )

    return late_probability


def generate_delay_message(
        task_type,
        expected_delay
):

    probability = get_delay_probability(
        task_type,
        expected_delay
    )

    if probability >= 80:

        return (
            f"⚠️ High risk of delay "
            f"({probability}%). "
            f"You are likely to be late "
            f"for {task_type}. "
            f"Start preparing now."
        )

    elif probability >= 50:

        return (
            f"⏰ Moderate delay risk "
            f"({probability}%). "
            f"Consider starting "
            f"{task_type} earlier."
        )

    else:

        return (
            f"✅ Low delay risk "
            f"({probability}%). "
            f"You are likely to stay on schedule."
        )