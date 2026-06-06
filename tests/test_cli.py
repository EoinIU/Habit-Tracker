from datetime import datetime

from typer.testing import CliRunner

from habit_tracker.cli import app
import habit_tracker.cli as cli
from habit_tracker.habit import Habit
from habit_tracker.storage import initialise_database, save_habit

runner = CliRunner()

def test_list_habits_shows_no_habits_message(tmp_path):
    """Tests whether the correct message is shown when there are no habits tracked yet."""
    database_path = tmp_path / "test_habits.db"
    cli.DATABASE_NAME = database_path

    result = runner.invoke(app, ["list-habits"])

    assert result.exit_code == 0
    assert "No habits tracked yet." in result.output

def test_list_habits_with_given_periodicity(tmp_path):
    """Tests whether the function to list habits with a given periodicity correctly filters habits based on their periodicity."""
    database_path = tmp_path / "test_habits.db"
    cli.DATABASE_NAME = database_path

    initialise_database(database_path)
    save_habit(Habit("Drink water", "daily"), database_path)
    save_habit(Habit("Gym", "weekly"), database_path)

    result = runner.invoke(app, ["list-habits-with-given-periodicity", "daily"])

    assert result.exit_code == 0
    assert "Drink water (daily)" in result.output
    assert "Gym (weekly)" not in result.output

def test_longest_streak_command(tmp_path):
    database_path = tmp_path / "test_habits.db"
    cli.DATABASE_NAME = database_path

    initialise_database(database_path)

    habit = Habit("Drink water", "daily")
    habit.complete(datetime(2025, 1, 1))
    habit.complete(datetime(2025, 1, 2))
    habit.complete(datetime(2025, 1, 3))

    save_habit(habit, database_path)

    result = runner.invoke(app, ["longest-streak"])

    assert result.exit_code == 0
    assert "Longest streak: 3 days for Drink water" in result.output