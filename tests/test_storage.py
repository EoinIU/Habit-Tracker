from datetime import datetime
from habit_tracker.habit import Habit
from habit_tracker.storage import add_completion, delete_habit, initialise_database, save_habit, load_habits
import sqlite3


def test_initialize_database_creates_database_tables(tmp_path):
    """Tests whether the function to initialize the database correctly creates the necessary tables for storing habits and their completions."""
    #Sets the database name to a temporary file path.
    database_path = tmp_path / "test_habits.db"

    #Initializes the database at the specified path.
    initialise_database(database_path)

    #Checks that the database file has been created at the specified path and that the habits and completions tables exist in the database.
    assert database_path.exists()

    #Connects to the SQLite database and retrieves the names of all tables in the database.
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    connection.close()

    #Checks that the habits and completions tables are present in the database by verifying that their names are included in the list of tables 
    #retrieved from the database.
    assert ("habits",) in tables
    assert ("completions",) in tables

def test_save_habit_stores_habit_in_database(tmp_path):
    """Tests whether a habit can be saved to the database and that the habit's name and periodicity are correctly stored."""
    #Sets the database name to a temporary file path and initializes the database at that path.
    database_path = tmp_path / "test_habits.db"
    initialise_database(database_path)

    #Creates a habit with the name "Drink water" and periodicity "daily".
    habit = Habit("Drink water", "daily")

    #Saves the habit to the database.
    save_habit(habit, database_path)

    #Connects to the SQLite database
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    #Retrieves the name and periodicity of the habit from the habits table in the database.
    cursor.execute("SELECT name, periodicity FROM habits")
    result = cursor.fetchone()

    #Closes the connection to the database.
    connection.close()

    #Checks that the retrieved name and periodicity match the expected values for the habit that was saved to the database.
    assert result == ("Drink water", "daily")

def test_load_habits_returns_saved_habit(tmp_path):
    """Tests whether a habit that has been saved to the database can be loaded back"""
    #Sets the database name to a temporary file path and initializes the database at that path.
    database_path = tmp_path / "test_habits.db"
    initialise_database(database_path)

    #Creates a habit with the name "Drink water" and periodicity "daily".
    original_habit = Habit("Drink water", "daily")
    #Saves the habit to the database.
    save_habit(original_habit, database_path)

    #Loads all habits from the database and assigns the result to the variable loaded_habits.
    loaded_habits = load_habits(database_path)

    #Checks that the loaded habit has the same name and periodicity as the original habit that was saved to the database.
    assert len(loaded_habits) == 1
    assert loaded_habits[0].name == "Drink water"
    assert loaded_habits[0].periodicity == "daily"

def test_load_habits_includes_completions(tmp_path):
    """Tests whether the completions of a habit are correctly loaded back when the habit is loaded."""
    #Sets the database name to a temporary file path and initializes the database at that path.
    database_path = tmp_path / "test_habits.db"
    initialise_database(database_path)

    #Creates a habit with the name "Drink water" and periodicity "daily".
    original_habit = Habit("Drink water", "daily")
    original_habit.complete(datetime(2025, 1, 1, 9, 0))

    #Saves the habit with its completion to the database.
    save_habit(original_habit, database_path)

    #Loads all habits from the database and assigns the result to the variable loaded_habits.
    loaded_habits = load_habits(database_path)

    #Checks that the loaded habit has one completion and that the datetime of that completion matches the expected value for the 
    #completion that was saved to the database.
    assert len(loaded_habits[0].completions) == 1
    assert loaded_habits[0].completions[0] == datetime(2025, 1, 1, 9, 0)

def test_add_completion_adds_completion_to_database(tmp_path):
    """Tests whether a completion can be added to a habit in the database and that the completion's datetime is correctly stored."""
    #Sets the database name to a temporary file path and initializes the database at that path.
    database_path = tmp_path / "test_habits.db"
    initialise_database(database_path)

    #Creates a habit with the name "Drink water" and periodicity "daily" and saves it to the database, retrieving the habit_id of the saved habit.
    habit = Habit("Drink water", "daily")
    habit_id = save_habit(habit, database_path)

    #Adds a completion for this habit to the database with a specific datetime value.
    add_completion(habit_id, datetime(2025, 1, 1, 9, 0), database_path)

    #Connects to the SQLite database 
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    #Retrieves the completed_at datetime of the completion that was added for this habit.
    cursor.execute("SELECT completed_at FROM completions WHERE habit_id = ?", (habit_id,))
    result = cursor.fetchone()

    #Closes the connection to the database.
    connection.close()

    #Checks that the retrieved completed_at datetime matches the expected value for the completion that was added to the database.
    assert result == ("2025-01-01T09:00:00",)

def test_delete_removes_habit_and_completions(tmp_path):
    """Tests whether a habit and its completions are correctly deleted from the database."""
    #Sets the database name to a temporary file path and initializes the database at that path.
    database_path = tmp_path / "test_habits.db"
    initialise_database(database_path)

    #Creates a habit with the name "Drink water" and periodicity "daily", completes it, and saves it to the database,
    #retrieving the habit_id of the saved habit.
    habit = Habit("Drink water", "daily")
    habit.complete(datetime(2025, 1, 1, 9, 0))
    habit_id = save_habit(habit, database_path)

    #Deletes the habit and its completions from the database using the habit_id.
    delete_habit(habit_id, database_path)

    #Connects to the SQLite database and retrieves all rows from the habits and completions tables.
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    #Retrieves all rows from the habits table
    cursor.execute("SELECT * FROM habits")
    habits_result = cursor.fetchall()

    #Retrieves all rows from the completions table
    cursor.execute("SELECT * FROM completions")
    completions_result = cursor.fetchall()

    #Closes the connection to the database.
    connection.close()

    #Checks that there are no rows in either the habits or completions tables, indicating that the habit and its completions were successfully deleted from the database.
    assert habits_result == []
    assert completions_result == []