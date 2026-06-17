from datetime import datetime
from pathlib import Path

from habit_tracker.habit import Habit
from habit_tracker.storage import initialise_database, load_habits, save_habit


DATABASE_NAME = Path(__file__).resolve().parent.parent / "habits.db"

def seed_database():
    """Populates the database with predefined habits and example completion data."""

    #Initialises the database
    initialise_database(DATABASE_NAME)

    #Sets the variable existing_habits to the result of the load_habits function
    existing_habits = load_habits(DATABASE_NAME)

    #If loop to check if the databse already contains data
    if len(existing_habits) > 0:
        print("Database already contains habits. Seed cancelled.")
        return
    
    #Data for habit1, drink water daily
    habit1 = Habit("Drink water", "daily")

    habit1.complete(datetime(2026, 1, 1, 9, 0))
    habit1.complete(datetime(2026, 1, 2, 9, 0))
    habit1.complete(datetime(2026, 1, 3, 9, 0))
    habit1.complete(datetime(2026, 1, 4, 9, 0))
    habit1.complete(datetime(2026, 1, 5, 9, 0))
    habit1.complete(datetime(2026, 1, 6, 9, 0))
    habit1.complete(datetime(2026, 1, 8, 9, 0))
    habit1.complete(datetime(2026, 1, 9, 9, 0))
    habit1.complete(datetime(2026, 1, 10, 9, 0))
    habit1.complete(datetime(2026, 1, 11, 9, 0))
    habit1.complete(datetime(2026, 1, 12, 9, 0))
    habit1.complete(datetime(2026, 1, 13, 9, 0))
    habit1.complete(datetime(2026, 1, 14, 9, 0))
    habit1.complete(datetime(2026, 1, 15, 9, 0))
    habit1.complete(datetime(2026, 1, 16, 9, 0))
    habit1.complete(datetime(2026, 1, 17, 9, 0))
    habit1.complete(datetime(2026, 1, 18, 9, 0))
    habit1.complete(datetime(2026, 1, 20, 9, 0))
    habit1.complete(datetime(2026, 1, 21, 9, 0))
    habit1.complete(datetime(2026, 1, 22, 9, 0))
    habit1.complete(datetime(2026, 1, 23, 9, 0))
    habit1.complete(datetime(2026, 1, 24, 9, 0))
    habit1.complete(datetime(2026, 1, 25, 9, 0))
    habit1.complete(datetime(2026, 1, 26, 9, 0))
    habit1.complete(datetime(2026, 1, 28, 9, 0))

    #Data for habit2, go to the gym weekly
    habit2 = Habit("Go to the gym", "weekly")

    habit2.complete(datetime(2026, 1, 1, 9, 0))
    habit2.complete(datetime(2026, 1, 8, 9, 0))
    habit2.complete(datetime(2026, 1, 15, 9, 0))
    habit2.complete(datetime(2026, 1, 22, 9, 0))

    #Data for habit3, read a book weekly
    habit3 = Habit("Read a book", "weekly")

    habit3.complete(datetime(2026, 1, 1, 9, 0))
    habit3.complete(datetime(2026, 1, 8, 9, 0))
    habit3.complete(datetime(2026, 1, 15, 9, 0))
    habit3.complete(datetime(2026, 1, 29, 9, 0))

    #Data for habit4, Run 10km weekly
    habit4 = Habit("Run 10km", "weekly")

    habit4.complete(datetime(2026, 1, 1, 9, 0))
    habit4.complete(datetime(2026, 1, 8, 9, 0))
    habit4.complete(datetime(2026, 1, 22, 9, 0))
    habit4.complete(datetime(2026, 1, 29, 9, 0))

    #Data for habit5, walk 10,000 steps, daily
    habit5 = Habit("Walk 10,000 steps", "daily")

    habit5.complete(datetime(2026, 1, 1, 9, 0))
    habit5.complete(datetime(2026, 1, 3, 9, 0))
    habit5.complete(datetime(2026, 1, 4, 9, 0))
    habit5.complete(datetime(2026, 1, 5, 9, 0))
    habit5.complete(datetime(2026, 1, 6, 9, 0))
    habit5.complete(datetime(2026, 1, 8, 9, 0))
    habit5.complete(datetime(2026, 1, 9, 9, 0))
    habit5.complete(datetime(2026, 1, 10, 9, 0))
    habit5.complete(datetime(2026, 1, 11, 9, 0))
    habit5.complete(datetime(2026, 1, 12, 9, 0))
    habit5.complete(datetime(2026, 1, 13, 9, 0))
    habit5.complete(datetime(2026, 1, 14, 9, 0))
    habit5.complete(datetime(2026, 1, 15, 9, 0))
    habit5.complete(datetime(2026, 1, 16, 9, 0))
    habit5.complete(datetime(2026, 1, 17, 9, 0))
    habit5.complete(datetime(2026, 1, 20, 9, 0))
    habit5.complete(datetime(2026, 1, 21, 9, 0))
    habit5.complete(datetime(2026, 1, 22, 9, 0))
    habit5.complete(datetime(2026, 1, 23, 9, 0))
    habit5.complete(datetime(2026, 1, 24, 9, 0))
    habit5.complete(datetime(2026, 1, 25, 9, 0))
    habit5.complete(datetime(2026, 1, 26, 9, 0))
    habit5.complete(datetime(2026, 1, 28, 9, 0))

    


    save_habit(habit1, DATABASE_NAME)
    save_habit(habit2, DATABASE_NAME)
    save_habit(habit3, DATABASE_NAME)
    save_habit(habit4, DATABASE_NAME)
    save_habit(habit5, DATABASE_NAME)




    print(f"Saved seed habit to: {DATABASE_NAME}")

if __name__ == "__main__":
     seed_database()