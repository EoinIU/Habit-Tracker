import typer
from habit_tracker.analytics import list_all_habits, list_all_habits_with_given_periodicity, list_longest_streak_for_given_habit, list_longest_streak_for_given_habit, return_longest_streak_of_all_habits
from habit_tracker.habit import Habit
from habit_tracker.storage import initialise_database, load_habits, save_habit

DATABASE_NAME = "habits.db" 


# The name of the database file where habits and their completions are stored.
app = typer.Typer()

@app.command()
def list_habits():
    """Lists all tracked habits."""
    initialise_database(DATABASE_NAME)
    habits = load_habits(DATABASE_NAME)
    habit_list = list_all_habits(habits)

    #If there are no habits tracked yet, a message is printed to the user.
    if len(habit_list) == 0:
        typer.echo("No habits tracked yet.")
        return

    #Prints the name and periodicity of each habit in the database, numbered in a list format.
    for index, habit in enumerate(habit_list, start=1):
        name, periodicity = habit
        typer.echo(f"{index}. {name} ({periodicity})")

@app.command()
def add_habit():
    """Adds a new habit to be tracked."""
    #Initialises the database
    initialise_database(DATABASE_NAME)

    #Asks the user for the name of the habit and the periodicity
    habit_name = typer.prompt("Please enter the name of the habit:")
    habit_periodicity = typer.prompt("Please enter the periodicity of the habit (daily/weekly):")

    #Loads the currently tracked habits from the database
    habits = load_habits(DATABASE_NAME)

    #This for loop iterates through each of the habits loaded from the database and checks if the habit name provided by the customer already exists
    for habit in habits:
        if habit.name == habit_name:
            typer.echo(f"Habit already exists: {habit_name}")
            return
        
    #Tries creating a habit object with the name and periodicity provided byt the user
    try:
        habit_to_save = Habit(habit_name, habit_periodicity)
    except ValueError as error:
        typer.echo(error)
        return

    #Saves the habit to the database
    save_habit(habit_to_save, DATABASE_NAME)

    #Shows confirmation message to the user
    typer.echo(f"Habit added: {habit_name} ({habit_periodicity})")
    

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

    #Assigns the longest streak for the given habit to the variable streak and uses the is_daily method to determine whether the unit should be days or weeks, which is assigned to the variable unit.
    streak = list_longest_streak_for_given_habit(habit)
    unit = "days" if habit.is_daily() else "weeks"

    #Prints the longest streak for the given habit, including the habit name, streak, and unit.
    typer.echo(f"Longest streak for {habit.name}: {streak} {unit}")

@app.command()
def main_menu():
    """Displays the main menu of the habit tracker application."""
    while True:
        typer.echo("")
        typer.echo("")
        typer.echo("")
        typer.echo("Welcome to the Habit Tracker!")
        typer.echo("----------------------------------")
        typer.echo("1. List all habits")
        typer.echo("2. Add habit")
        typer.echo("3. Complete habit")
        typer.echo("4. Delete habit")
        typer.echo("5. Analytics")
        typer.echo("6. Exit")
        typer.echo("----------------------------------")
        choice = typer.prompt("Please choose an option: (e.g., type '1' to list all habits)")
        typer.echo("")
        typer.echo("")
        typer.echo("")
        if choice == "1":
            list_habits()
        elif choice == "2":
            random_assignment = 1 
        elif choice == "3":
            random_assignment = 1 
        elif choice == "4":
            random_assignment = 1 
        elif choice == "5":
            random_assignment = 1 
        elif choice == "6":
            typer.echo("Goodbye!")
            break
        else:
            typer.echo("Invalid option. Please try again.")


# Runs the CLI application when the script is executed directly.
if __name__ == "__main__":

    app()
