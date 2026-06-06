from datetime import datetime

from habit_tracker.habit import Habit
from habit_tracker.storage import add_completion, delete_habit, initialise_database, save_habit, load_habits
import sqlite3


def test_initialize_database_creates_database_tables(tmp_path):
    database_path = tmp_path / "test_habits.db"

    initialise_database(database_path)

    assert database_path.exists()

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    connection.close()

    assert ("habits",) in tables
    assert ("completions",) in tables

def test_save_habit_stores_habit_in_database(tmp_path):
    """Tests whether a habit can be saved to the database and that the habit's name and periodicity are correctly stored."""
    database_path = tmp_path / "test_habits.db"
    initialise_database(database_path)

    habit = Habit("Drink water", "daily")

    save_habit(habit, database_path)

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("SELECT name, periodicity FROM habits")
    result = cursor.fetchone()

    connection.close()

    assert result == ("Drink water", "daily")

def test_load_habits_returns_saved_habit(tmp_path):
    """Tests whether a habit that has been saved to the database can be loaded back"""
    database_path = tmp_path / "test_habits.db"
    initialise_database(database_path)

    original_habit = Habit("Drink water", "daily")
    save_habit(original_habit, database_path)

    loaded_habits = load_habits(database_path)

    assert len(loaded_habits) == 1
    assert loaded_habits[0].name == "Drink water"
    assert loaded_habits[0].periodicity == "daily"

def test_load_habits_includes_completions(tmp_path):
    """Tests whether the completions of a habit are correctly loaded back when the habit is loaded."""
    database_path = tmp_path / "test_habits.db"
    initialise_database(database_path)

    original_habit = Habit("Drink water", "daily")
    original_habit.complete(datetime(2025, 1, 1, 9, 0))

    save_habit(original_habit, database_path)

    loaded_habits = load_habits(database_path)

    assert len(loaded_habits[0].completions) == 1
    assert loaded_habits[0].completions[0] == datetime(2025, 1, 1, 9, 0)

def test_add_completion_adds_completion_to_database(tmp_path):
    """Tests whether a completion can be added to a habit in the database and that the completion's datetime is correctly stored."""
    database_path = tmp_path / "test_habits.db"
    initialise_database(database_path)

    habit = Habit("Drink water", "daily")
    habit_id = save_habit(habit, database_path)

    add_completion(habit_id, datetime(2025, 1, 1, 9, 0), database_path)

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("SELECT completed_at FROM completions WHERE habit_id = ?", (habit_id,))
    result = cursor.fetchone()

    connection.close()

    assert result == ("2025-01-01T09:00:00",)

def test_delete_removes_habit_and_completions(tmp_path):
    """Tests whether a habit and its completions are correctly deleted from the database."""
    database_path = tmp_path / "test_habits.db"
    initialise_database(database_path)

    habit = Habit("Drink water", "daily")
    habit.complete(datetime(2025, 1, 1, 9, 0))
    habit_id = save_habit(habit, database_path)

    delete_habit(habit_id, database_path)

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM habits")
    habits_result = cursor.fetchall()

    cursor.execute("SELECT * FROM completions")
    completions_result = cursor.fetchall()

    connection.close()

    assert habits_result == []
    assert completions_result == []