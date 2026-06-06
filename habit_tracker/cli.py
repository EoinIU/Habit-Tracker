import typer
from habit_tracker.analytics import list_all_habits_with_given_periodicity, list_longest_streak_for_given_habit, list_longest_streak_for_given_habit, return_longest_streak_of_all_habits
from habit_tracker.storage import initialise_database, load_habits

DATABASE_NAME = "habits.db" 

# The name of the database file where habits and their completions are stored.
app = typer.Typer()

@app.command()
def list_habits():
    """Lists all tracked habits."""
    initialise_database(DATABASE_NAME)
    habits = load_habits(DATABASE_NAME)

    # If there are no habits tracked yet, a message is printed to the user.
    if len(habits) == 0:
            typer.echo("No habits tracked yet.")

    # Prints the name and periodicity of each habit in the database.
    for habit in habits:
        typer.echo(f"{habit.name} ({habit.periodicity})")

@app.command()
def list_habits_with_given_periodicity(periodicity: str):
    """Lists all tracked habits with a given periodicity."""
    initialise_database(DATABASE_NAME)
    habits = load_habits(DATABASE_NAME)

    filtered_habits = list_all_habits_with_given_periodicity(habits, periodicity)

    # If there are no habits with the given periodicity, a message is printed to the user.
    if len(filtered_habits) == 0:
        typer.echo(f"No {periodicity} habits tracked yet.")
        return

    for habit in filtered_habits:
        #Prints the name and periodicity of each habit in the database with the given periodicity.
        typer.echo(f"{habit.name} ({habit.periodicity})")

@app.command()
def longest_streak():
    """Lists the longest streak of all tracked habits."""
    initialise_database(DATABASE_NAME)
    habits = load_habits(DATABASE_NAME)

    # If there are no habits tracked yet, a message is printed to the user.
    if len(habits) == 0:
        typer.echo("No habits tracked yet.")
        return

    # Assigns the longest streak, unit, and habit name across all tracked habits to the variables streak, unit, and habit_name respectively.
    streak, unit, habit_name = return_longest_streak_of_all_habits(habits)
    
    # 
    typer.echo(f"Longest streak: {streak} {unit} for {habit_name}")

@app.command()
def longest_streak_for_habit(habit_name: str):
    """Lists the longest streak for a given habit."""
    initialise_database(DATABASE_NAME)
    habits = load_habits(DATABASE_NAME)

    habit = next((h for h in habits if h.name == habit_name), None)

    # If the habit with the given name is not found in the database, a message is printed to the user.
    if habit is None:
        typer.echo(f"Habit '{habit_name}' not found.")
        return

    # assigns the longest streak for the given habit to the variable streak and uses the is_daily method to determine whether the unit should be days or weeks, which is assigned to the variable unit.
    streak = list_longest_streak_for_given_habit(habit)
    unit = "days" if habit.is_daily() else "weeks"

    #Prints the longest streak for the given habit, including the habit name, streak, and unit.
    typer.echo(f"Longest streak for {habit.name}: {streak} {unit}")

# Runs the CLI application when the script is executed directly.
if __name__ == "__main__":
    """Runs the CLI application."""
    app()