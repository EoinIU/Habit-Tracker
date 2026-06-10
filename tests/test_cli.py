from datetime import datetime
from typer.testing import CliRunner
from habit_tracker.cli import app
import habit_tracker.cli as cli
from habit_tracker.habit import Habit
from habit_tracker.storage import initialise_database, load_habits, save_habit

# The CliRunner from the Typer librarywill be used to invoke the CLI commands in the tests and check their output.
runner = CliRunner()

def test_list_habits_shows_no_habits_message(tmp_path):
    """Tests whether the correct message is shown when there are no habits tracked yet."""
    #Sets the database name to a temporary file path to ensure that the tests do not interfere with the actual database used by the application.
    database_path = tmp_path / "test_habits.db"
    cli.DATABASE_NAME = database_path

    #Initialises the database at the specified path.
    result = runner.invoke(app, ["list-habits"])

    #Checks that the command exits with a status code of 0 (indicating success) and that the output contains the message 
    #"No habits tracked yet.", which is the expected output when there are no habits in the database.
    assert result.exit_code == 0
    assert "No habits tracked yet." in result.output

def test_list_habits_with_given_periodicity(tmp_path):
    """Tests whether the function to list habits with a given periodicity correctly filters habits based on their periodicity."""
    #Sets the database name to a temporary file path to ensure that the tests do not interfere with the actual database used by the application.
    database_path = tmp_path / "test_habits.db"
    cli.DATABASE_NAME = database_path

    #Initialises the database at the specified path, which creates the necessary tables for storing habits and their completions.
    initialise_database(database_path)

    #Creates two habits, one with daily periodicity and another with weekly periodicity, and saves them to the database.
    save_habit(Habit("Drink water", "daily"), database_path)
    save_habit(Habit("Gym", "weekly"), database_path)

    #Invokes the CLI command to list habits with daily periodicity and checks that the output contains 
    # the expected habit with daily periodicity and does not contain the habit with weekly periodicity.
    result = runner.invoke(app, ["list-habits-with-given-periodicity", "daily"])

    #Checks that the command exits with a status code of 0 (indicating success) and that the output contains 
    #"Drink water (daily)" and does not contain "Gym (weekly)", which is the expected output when filtering for daily habits.
    assert result.exit_code == 0
    assert "Drink water (daily)" in result.output
    assert "Gym (weekly)" not in result.output

def test_longest_streak_command(tmp_path):
    """Tests whether the CLI command to list the longest streak across all tracked habits correctly identifies and displays the longest streak."""
    #Sets the database name to a temporary file path to ensure that the tests do not interfere with the actual database used by the application.
    database_path = tmp_path / "test_habits.db"
    cli.DATABASE_NAME = database_path

    #Initialises the database at the specified path.
    initialise_database(database_path)

    #Creates a habit with daily periodicity and completes it for three consecutive days.
    habit = Habit("Drink water", "daily")
    habit.complete(datetime(2025, 1, 1))
    habit.complete(datetime(2025, 1, 2))
    habit.complete(datetime(2025, 1, 3))

    #Saves the habit to the database.
    save_habit(habit, database_path)

    #Invokes the CLI command to list the longest streak across all tracked habits and checks that the output contains the expected longest streak information for the habit that was completed for three consecutive days.
    result = runner.invoke(app, ["longest-streak"])

    #Checks that the command exits with a status code of 0 (indicating success) and that the output contains "Longest streak: 3 days for Drink water".
    assert result.exit_code == 0
    assert "Longest streak: 3 days for Drink water" in result.output

def test_longest_streak_for_habit_command(tmp_path):
    """Tests whether the CLI command to list the longest streak for a given habit correctly identifies and displays the longest streak for that habit."""
    #Sets the database name to a temporary file path to ensure that the tests do not interfere with the actual database used by the application.
    database_path = tmp_path / "test_habits.db"
    cli.DATABASE_NAME = database_path

    #Initialises the database at the specified path.
    initialise_database(database_path)

    #Creates a habit with daily periodicity and completes it for three consecutive days.
    habit = Habit("Drink water", "daily")
    habit.complete(datetime(2025, 1, 1))
    habit.complete(datetime(2025, 1, 2))
    habit.complete(datetime(2025, 1, 3))

    #Saves the habit to the database.
    save_habit(habit, database_path)

    #Invokes the CLI command to list the longest streak for the habit named "Drink water".
    result = runner.invoke(app, ["longest-streak-for-habit", "Drink water"])

    #Checks that the command exits with a status code of 0 (indicating success) and that the output contains "Longest streak for Drink water: 3 days".
    assert result.exit_code == 0
    assert "Longest streak for Drink water: 3 days" in result.output

def test_longest_streak_for_unknown_habit_command(tmp_path):
    """Tests whether the CLI command to list the longest streak for a given habit correctly handles the case when the specified habit is not found in the database."""
    #Sets the database name to a temporary file path to ensure that the tests do not interfere with the actual database used by the application.
    database_path = tmp_path / "test_habits.db"
    cli.DATABASE_NAME = database_path

    #Initialises the database at the specified paths.
    initialise_database(database_path)

    #Invokes the CLI command to list the longest streak for a habit named "Unknown habit", which does not exist in the database.
    result = runner.invoke(app, ["longest-streak-for-habit", "Unknown habit"])

    #Checks that the command exits with a status code of 0 (indicating success) and that the output contains "Habit 'Unknown habit' not found.".
    assert result.exit_code == 0
    assert "Habit 'Unknown habit' not found." in result.output

def test_add_habit_menu_option_adds_new_habit(tmp_path):
    """Test that the add-habit CLI command saves a new habit."""
    #Creates a temporary test database and point the CLI to it.
    database_path = tmp_path / "test_habits.db"
    cli.DATABASE_NAME = database_path

    #Simulates the user entering a habit name and periodicity.
    result = runner.invoke(
        app,
        ["add-habit"],
        input="Drink water\ndaily\n"
    )

    #Checks that the command ran successfully and showed confirmation.
    assert result.exit_code == 0
    assert "Habit added: Drink water (daily)" in result.output

    #Loads habits from the test database and check the new habit was saved.
    habits = load_habits(database_path)
    assert len(habits) == 1
    assert habits[0].name == "Drink water"
    assert habits[0].periodicity == "daily"