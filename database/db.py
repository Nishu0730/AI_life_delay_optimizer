import sqlite3

DB_NAME = "database/tasks.db"


def create_connection():

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    return conn


def create_table():

    conn = create_connection()
    cursor = conn.cursor()

    # ---------------- TASKS TABLE ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        
        user_id INTEGER,

        task_name TEXT NOT NULL,
        task_type TEXT,

        priority TEXT,
        difficulty INTEGER,

        location TEXT,
        travel_time INTEGER,
        traffic_level TEXT,

        planned_time TEXT,
        planned_duration INTEGER,

        actual_start TEXT,
        actual_end TEXT,
        actual_duration INTEGER,

        status TEXT
    )
    """)

    # ---------------- USER LOCATIONS TABLE ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_locations (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        location_type TEXT UNIQUE,
        place_name TEXT,

        latitude REAL,
        longitude REAL
    )
    """)

    conn.commit()
    conn.close()


def create_users_table():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def add_user(
        name,
        email,
        password
):

    conn = create_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO users (
            name,
            email,
            password
        )
        VALUES (?, ?, ?)
        """, (
            name,
            email,
            password
        ))

        conn.commit()
        return True

    except:

        return False

    finally:

        conn.close()


def get_user_by_email(email):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM users
    WHERE email = ?
    """, (email,))

    user = cursor.fetchone()

    conn.close()

    if user:
        return dict(user)

    return None

def add_task_to_db(task):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tasks (
    
        user_id,
        
        task_name,
        task_type,

        priority,
        difficulty,

        location,
        travel_time,
        traffic_level,

        planned_time,
        planned_duration,

        actual_start,
        actual_end,
        actual_duration,

        status
    )

    VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        task["user_id"],
        task["task_name"],
        task["task_type"],

        task["priority"],
        task["difficulty"],

        task["location"],
        task["travel_time"],
        task["traffic_level"],

        task["planned_time"],
        task["planned_duration"],

        None,
        None,
        None,

        task["status"]
    ))

    conn.commit()
    conn.close()


def get_all_tasks():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks"
    )

    rows = cursor.fetchall()

    tasks = [
        dict(row)
        for row in rows
    ]

    conn.close()

    return tasks

def get_tasks_by_user(user_id):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM tasks
    WHERE user_id = ?
    """, (
        user_id,
    ))

    rows = cursor.fetchall()

    tasks = [
        dict(row)
        for row in rows
    ]

    conn.close()

    return tasks


def complete_task_in_db(
        task_id,
        actual_start,
        actual_end,
        actual_duration
):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE tasks
    SET
        actual_start = ?,
        actual_end = ?,
        actual_duration = ?,
        status = ?
    WHERE id = ?
    """, (
        actual_start,
        actual_end,
        actual_duration,
        "completed",
        task_id
    ))

    conn.commit()
    conn.close()

def update_task_in_db(
        task_id,
        task_name,
        task_type,
        location,
        planned_time
):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE tasks
    SET
        task_name = ?,
        task_type = ?,
        location = ?,
        planned_time = ?
    WHERE id = ?
    """, (
        task_name,
        task_type,
        location,
        planned_time,
        task_id
    ))

    conn.commit()
    conn.close()

def delete_task_from_db(task_id):
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM tasks
        WHERE id = ?
        """, (
            task_id,
        ))

        conn.commit()
        conn.close()
# ---------------- USER LOCATION FUNCTIONS ----------------

def save_user_location(
        location_type,
        place_name,
        latitude,
        longitude
):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO user_locations
    (
        location_type,
        place_name,
        latitude,
        longitude
    )
    VALUES (?, ?, ?, ?)
    """, (
        location_type,
        place_name,
        latitude,
        longitude
    ))

    conn.commit()
    conn.close()


def get_user_locations():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM user_locations
    """)

    rows = cursor.fetchall()

    locations = [
        dict(row)
        for row in rows
    ]

    conn.close()

    return locations


def get_location(location_type):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM user_locations
    WHERE location_type = ?
    """, (
        location_type,
    ))

    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)

    return None