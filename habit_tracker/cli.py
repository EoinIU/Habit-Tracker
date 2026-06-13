import typer
from habit_tracker.analytics import list_all_habits, list_all_habits_with_given_periodicity, list_longest_streak_for_given_habit, list_longest_streak_for_given_habit, return_longest_streak_of_all_habits
from habit_tracker.habit import Habit
from habit_tracker.storage import add_completion, delete_habit, initialise_database, load_habits, save_habit

DATABASE_NAME = "habits.db" 


# The name of the database file where habits and their completions are stored.
app = typer.Typer()

@app.command()
def list_habits():
    """Lists all tracked habits."""
    initialise_database(DATABASE_NAME)
    habits = load_habits(DATABASE_NAME)
    habit_list = list_all_habits(habits)
    
    #Prints an empty line for formatting purposes
    typer.echo("")

    #If there are no habits tracked yet, a message is printed to the user.
    if len(habit_list) == 0:
        typer.echo("No habits tracked yet.")
        return

    #Prints title and empty line 
    typer.echo("Currently tracked habits:")
    typer.echo("")
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
    typer.echo("")
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
def complete_habit():
    """Allows the user to mark a habit as complete"""
    #Initialise the database
    initialise_database(DATABASE_NAME)
    #Sets the variable habits to the 
    habits = load_habits(DATABASE_NAME)

    #If there are no habits tracked yet then no habit can be completed and a message is printed to the user.
    if len(habits) == 0:
        typer.echo("")
        typer.echo("No habits tracked yet.")
        return

    #Prints the name and periodicity of each habit in the database, numbered in a list format.
    for index, habit in enumerate(habits, start=1):
        typer.echo(f"{index}. {habit.name} ({habit.periodicity})")

    #Asks the user to enter the number of the habit they wish to complete
    typer.echo("")
    entered_number = typer.prompt("Please enter the number of the habit you wish to complete, e.g., '1'")

    #Checks if the users input is an integer
    try:
        selected_number = int(entered_number)
    except ValueError:
        typer.echo("Please enter a valid number.")
        return

    #Checks that the users inputted number is within the given range of habits
    if selected_number < 1 or selected_number > len(habits):
        typer.echo("Invalid habit number.")
        return
    
    #Finds the ID of the habit the user wishes to complete
    selected_habit = habits[selected_number - 1]

    #Adds a completion
    add_completion(selected_habit.id, database_name=DATABASE_NAME)

    #Lets the user that the habit has been marked complete
    typer.echo(f"Marked complete: {selected_habit.name}")

@app.command()
def delete_a_habit():
    """Allows the user to delete a habit"""
    #Initialise the database
    initialise_database(DATABASE_NAME)
    #Sets the variable habits to the results of the load_habits function
    habits = load_habits(DATABASE_NAME)

    #If there are no habits tracked yet then no habit can be deleted and so a message is printed to the user.
    if len(habits) == 0:
        typer.echo("")
        typer.echo("No habits tracked yet.")
        return

    #Prints the name and periodicity of each habit in the database, numbered in a list format.
    for index, habit in enumerate(habits, start=1):
        typer.echo(f"{index}. {habit.name} ({habit.periodicity})")

    #Asks the user to enter the number of the habit they wish to delete
    typer.echo("")
    entered_number = typer.prompt("Please enter the number of the habit you wish to delete, e.g., '1'")

    #Checks if the users input is an integer
    try:
        selected_number = int(entered_number)
    except ValueError:
        typer.echo("")
        typer.echo("Please enter a valid number.")
        return

    #Checks that the users inputted number is within the given range of habits
    if selected_number < 1 or selected_number > len(habits):
        typer.echo("")
        typer.echo("Invalid habit number.")
        return
    
    #Finds the habit the user wishes to delete
    selected_habit = habits[selected_number - 1]

    #Asks the user if they are sure they want to delete the given habit, and assigns the user's input to the variable certainty
    certainty = typer.prompt(f"Are you sure you want to delete {selected_habit.name}? this cannot be undone. type: y/n").lower()

    #If loop which deals with the user's input
    if certainty == "y":
        delete_habit(selected_habit.id, DATABASE_NAME)
        typer.echo(f"{selected_habit.name} has been deleted")
    elif certainty == "n":
        typer.echo(f"{selected_habit.name} has not been deleted")
    else:
        typer.echo("Please enter a valid input")

    

@app.command()
def list_habits_with_given_periodicity():
    """Lists all tracked habits with a given periodicity."""
    #Initialise the database
    initialise_database(DATABASE_NAME)
    habits = load_habits(DATABASE_NAME)
    #Sets the variable choice equal to the lower case version of the users unput
    typer.echo("")
    choice = typer.prompt("Please type your chosen periodicity (daily/weekly)").lower()

    #Checks whether the user's input is either 'daily' or 'weekly'
    if choice not in ["daily", "weekly"]:
        typer.echo("Please enter either daily or weekly.")
        return

    #Assigns the variable matching_habits to the result of the return_all_habits_with_given_periodicity function from the analytics module
    matching_habits = list_all_habits_with_given_periodicity(habits, choice)

    #Checks if matching_habits is empty and lets the user know
    if len(matching_habits) == 0:
        typer.echo(f"No {choice} habits tracked yet.")
        return

    #Prints a title and empty lines for formatting
    typer.echo("")
    typer.echo(f"Habits with {choice} periodicity:")
    typer.echo("")

    #A for loop which lists each item in matching_habits for the user
    for index, habit in enumerate(matching_habits, start=1):
        typer.echo(f"{index}. {habit.name} ({habit.periodicity})")




@app.command()
def longest_streak():
    """Lists the longest streak of all tracked habits."""
    initialise_database(DATABASE_NAME)
    habits = load_habits(DATABASE_NAME)

    #If there are no habits tracked yet, a message is printed to the user.
    if len(habits) == 0:
        typer.echo("No habits tracked yet.")
        return

    #Assigns the longest streak, unit, and habit name across all tracked habits to the variables streak, unit, and habit_name respectively.
    streak, unit, habit_name = return_longest_streak_of_all_habits(habits)
    
    # 
    typer.echo(f"Longest streak: {streak} {unit} for {habit_name}")

@app.command()
def longest_streak_for_habit(habit_name: str):
    """Lists the longest streak for a given habit."""
    initialise_database(DATABASE_NAME)
    habits = load_habits(DATABASE_NAME)

    habit = next((h for h in habits if h.name == habit_name), None)

    #If the habit with the given name is not found in the database, a message is printed to the user.
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
        typer.echo("Habit Tracker Menu")
        typer.echo("----------------------------------")
        typer.echo("1. List all habits")
        typer.echo("2. Add habit")
        typer.echo("3. Complete habit")
        typer.echo("4. Delete habit")
        typer.echo("5. Analytics")
        typer.echo("6. Exit")
        typer.echo("----------------------------------")
        typer.echo("")
        typer.echo("")
        choice = typer.prompt("Please choose an option: (e.g., type '1' to list all habits)")
        if choice == "1":
            list_habits()
        elif choice == "2":
            add_habit()
        elif choice == "3":
            complete_habit()
        elif choice == "4":
            delete_a_habit() 
        elif choice == "5":
            analytics_menu()
        elif choice == "6":
            typer.echo("Goodbye!")
            break
        else:
            typer.echo("Invalid option. Please try again.")

@app.command()
def analytics_menu():
    """Displays the analytics sub-menu"""
    while True:
        typer.echo("")
        typer.echo("")
        typer.echo(" Habit Tracker Analytics")
        typer.echo("----------------------------------")
        typer.echo("1. List all habits")
        typer.echo("2. List all habits with a given periodicity")
        typer.echo("3. List longest streak for a given habit")
        typer.echo("4. List longest streak of all habits")
        typer.echo("5. Exit to main menu")
        typer.echo("----------------------------------")
        typer.echo("")
        typer.echo("")
        choice = typer.prompt("Please choose an option: (e.g., type '1' to list all habits)")

        if choice == "1":
            list_habits() 
        elif choice == "2":
            list_habits_with_given_periodicity()
        elif choice == "3":
            random_assignment = 1 
        elif choice == "4":
            random_assignment = 1 
        elif choice == "5":
            main_menu()
        else:
            typer.echo("Invalid option. Please try again.")
#Runs the CLI application when the script is executed directly.
if __name__ == "__main__":

    app()
