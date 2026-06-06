import typer

from habit_tracker.analytics import list_all_habits_with_given_periodicity, list_longest_streak_for_given_habit, list_longest_streak_for_given_habit, return_longest_streak_of_all_habits
from habit_tracker.storage import initialise_database, load_habits

DATABASE_NAME = "habits.db" 

app = typer.Typer()

@app.command()
def list_habits():
    """Lists all tracked habits."""
    initialise_database(DATABASE_NAME)
    habits = load_habits(DATABASE_NAME)

    if len(habits) == 0:
            """returns a message if there are no habits tracked yet."""
            typer.echo("No habits tracked yet.")

    for habit in habits:
        """Prints the name and periodicity of each habit in the database."""
        typer.echo(f"{habit.name} ({habit.periodicity})")

@app.command()
def list_habits_with_given_periodicity(periodicity: str):
    """Lists all tracked habits with a given periodicity."""
    initialise_database(DATABASE_NAME)
    habits = load_habits(DATABASE_NAME)

    filtered_habits = list_all_habits_with_given_periodicity(habits, periodicity)

    if len(filtered_habits) == 0:
        """returns a message if there are no habits with the given periodicity."""
        typer.echo(f"No {periodicity} habits tracked yet.")
        return

    for habit in filtered_habits:
        """Prints the name and periodicity of each habit in the database with the given periodicity."""
        typer.echo(f"{habit.name} ({habit.periodicity})")

@app.command()
def longest_streak():
    """Lists the longest streak of all tracked habits."""
    initialise_database(DATABASE_NAME)
    habits = load_habits(DATABASE_NAME)

    if len(habits) == 0:
        typer.echo("No habits tracked yet.")
        return

    streak, unit, habit_name = return_longest_streak_of_all_habits(habits)
    
    typer.echo(f"Longest streak: {streak} {unit} for {habit_name}")

@app.command()
def longest_streak_for_habit(habit_name: str):
    """Lists the longest streak for a given habit."""
    initialise_database(DATABASE_NAME)
    habits = load_habits(DATABASE_NAME)

    habit = next((h for h in habits if h.name == habit_name), None)

    if habit is None:
        typer.echo(f"Habit '{habit_name}' not found.")
        return

    streak = list_longest_streak_for_given_habit(habit)
    unit = "days" if habit.is_daily() else "weeks"

    typer.echo(f"Longest streak for {habit.name}: {streak} {unit}")

if __name__ == "__main__":
    """Runs the CLI application."""
    app()