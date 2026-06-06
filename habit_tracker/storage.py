import sqlite3
from datetime import datetime
from habit_tracker import habit
from habit_tracker.habit import Habit


def initialise_database(database_name="habits.db"):
    """Creates the database tables if they do not already exist."""
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            periodicity TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    """Creates the habits table if it does not already exist."""

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completed_at TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits (id)
        )
    """)
    """Creates the completions table if it does not already exist."""

    connection.commit()
    connection.close()

def save_habit(habit, database_name="habits.db"):
    """Save a habit to the database."""
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO habits (name, periodicity, created_at) VALUES (?, ?, ?)
    """, (habit.name, habit.periodicity, habit.created_at.isoformat()))
    """Saves the habit's name, periodicity and created_at attributes to the habits table."""

    habit_id = cursor.lastrowid

    for completion in habit.completions:
        """Saves each completion of the habit to the completions table, linking it to the habit via the habit_id foreign key."""
        cursor.execute("""
            INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)
        """, (habit_id, completion.isoformat()))

    connection.commit()
    connection.close()
    return habit_id

def load_habits(database_name="habits.db"):
    """Load all habits and their completions from the database."""
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, periodicity, created_at FROM habits")
    habit_rows = cursor.fetchall()

    habits = []

    for habit_id, name, periodicity, created_at in habit_rows:
        """Creates a Habit object for each habit in the database and populates its completions list with the corresponding completions from the completions table."""
        habit = Habit(name, periodicity)
        habit.created_at = datetime.fromisoformat(created_at)

        cursor.execute(
            "SELECT completed_at FROM completions WHERE habit_id = ?",
             (habit_id,)
        )

        completion_rows = cursor.fetchall()

        for completion_row in completion_rows:
            completed_at = completion_row[0]
            habit.completions.append(datetime.fromisoformat(completed_at))

        habits.append(habit)

    connection.close()
    return habits

def add_completion(habit_id, completed_at=None, database_name="habits.db"):
    """Add a completion for a habit in the database. If no datetime value is provided, the current time and date will be used."""
    if completed_at is None:
        completed_at = datetime.now()

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    

    cursor.execute("""
        INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)
    """, (habit_id, completed_at.isoformat()))

    completion_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return completion_id

def delete_habit(habit_id, database_name="habits.db"):
    """Delete a habit and its completions from the database."""
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
    """Deletes all completions linked to the habit via the habit_id foreign key."""

    cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    """Deletes the habit from the habits table."""

    connection.commit()
    connection.close()