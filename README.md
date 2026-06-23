#  Habit Tracker
This is a command-line habit tracking application built using python.

It allows users to create and manage habits, track completion, and analyse progress.

##  Installation

N.B. `python` is used for the main commands in this guide, however some macOS/Linux installations require `python3`.

1) Clone the repository and enter the project folder

    `git clone https://github.com/EoinIU/Habit-Tracker`
   
    `cd Habit-Tracker-main`

2) Create a virtual environment

    `python -m venv .venv`

3) Activate the virtual environment

    Windows (Command Prompt)
   
    `.venv\Scripts\activate`
   
    Windows (PowerShell)
   
    `.venv\Scripts\Activate.ps1`
   
    macOS / Linux
   
    `source .venv/bin/activate`
   
4)  Install the required packages:
   
    `pip install typer pytest`

##  Load example data

The seed script creates five predefined habits with four weeks of example completion data.

Run:

`python -m habit_tracker.seed`

If the database already contains habits, the seed script will stop to prevent duplicate data.

If at any time you wish to reload the example data again run:

`rm habits.db` first, then:

`python -m habit_tracker.seed`

##  Run the application

Start the main menu:

`python -m habit_tracker.cli main-menu`

###  Main menu

Follow the on screen commands. Type the number for the command you wish to execute and hit enter.

1) List all currently tracked habits
2) Add a new habit
3) Mark a habit as complete
4) Delete a habit
5) Enter the Analytics menu
6) Exit the app

###  Analytics menu

Follow the on screen commands. Type the humber for the command you wish to execute and hit enter.

1) List all currently tracked habits
2) List all habits with a given periodicity
3) List longest streak for a given habit
4) List longest streak for all habits
5) Return to main menu

##  Run the tests

To execute suite of tests, from the project root run `pytest`

##  Database

The application uses SQLite to store its data in a file called **habits.db**

The database contains two tables:

  1)  **Habits**, which stores the habit name, the periodicity, and the creation date.
  2)  **Completions**, which stored dates when each habit was completed.

The database file is excluded from Git so that each user can create and manage their own local data. The application will automatically create a new database either when the user seeds the example data, or when they add a habit for the first time.
