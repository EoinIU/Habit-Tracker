from habit_tracker.analytics import list_all_habits, list_all_habits_with_given_periodicity, list_longest_streak_for_given_habit, return_longest_streak_of_all_habits
from habit_tracker.habit import Habit
from datetime import datetime

#Habits to be used for testing.
habit1 = Habit("Drink water", "daily")
habit2 = Habit("Gym", "weekly")
habits_list = [habit1, habit2]

def test_list_all_habits():
    """Tests that the function to list all habits returns a list of all habits."""

    #Calls the function to list all habits and assigns the result to the variable result.
    result = list_all_habits(habits_list)

    #Checks that the result contains the name and periodicity of each habit.
    assert result == [("Drink water", "daily"), ("Gym", "weekly")]

def test_all_habits_daily():
    """Tests if all daily habits can be listed."""

    #Calls the function to list all habits with daily periodicity and assigns the result to the variable result.
    result = list_all_habits_with_given_periodicity(habits_list, "daily")

    #Checks that the result is a list containing only habit1, which is the only habit in the habits_list with daily periodicity.
    assert result == [habit1]

def test_all_habits_weekly():
    """Tests if all weekly habits can be listed."""

    #Calls the function to list all habits with weekly periodicity and assigns the result to the variable result.
    result = list_all_habits_with_given_periodicity(habits_list, "weekly")

    #Checks that the result is a list containing only habit2, which is the only habit in the habits_list with weekly periodicity.
    assert result == [habit2]

def test_longest_streak_for_daily_habit():
    """tests the logic for calculating the longest streak for a daily habit"""
    #Creates a habit with daily periodicity and completes it for three consecutive days.
    habit = Habit("Drink water", "daily")

    habit.complete(datetime(2025, 1, 1))
    habit.complete(datetime(2025, 1, 2))
    habit.complete(datetime(2025, 1, 3))

    #Calls the function to calculate the longest streak for this habit and assigns the result to the variable result.
    result = list_longest_streak_for_given_habit(habit)

    #Checks that the result is 3, which is the longest streak of consecutive completions for this habit.
    assert result == 3

def test_longest_streak_for_weekly_habit():
    """tests the logic for calculating the longest streak for a weekly habit."""
    #Creates a habit with weekly periodicity and completes it for four consecutive weeks.
    habit = Habit("Go to the gym", "weekly")

    habit.complete(datetime(2025, 1, 1))
    habit.complete(datetime(2025, 1, 8))
    habit.complete(datetime(2025, 1, 15))

    #Calls the function to calculate the longest streak for this habit and assigns the result to the variable result.
    result = list_longest_streak_for_given_habit(habit)

    #Checks that the result is 3, which is the longest streak of consecutive completions for this habit.
    assert result == 3

def test_longest_streak_of_all_habits():
    """tests the logic for calculating the longest streak for all tracked habits."""
    #Creates two habits, one with daily periodicity and one with weekly periodicity, and completes them for different numbers of consecutive periods.
    habit1 = Habit("Drink water", "daily")
    habit2 = Habit("Go to the gym", "weekly")

    habit1.complete(datetime(2025, 1, 1))
    habit1.complete(datetime(2025, 1, 2))
    habit1.complete(datetime(2025, 1, 3))

    habit2.complete(datetime(2025, 1, 1))
    habit2.complete(datetime(2025, 1, 8))
    habit2.complete(datetime(2025, 1, 15))
    habit2.complete(datetime(2025, 1, 22))

    #Calls the function to calculate the longest streak across all tracked habits and assigns the result to the variable result.
    result = return_longest_streak_of_all_habits([habit1, habit2])

    #Checks that the result is a tuple containing the longest streak (4), the unit ("weeks"), and the habit name ("Go to the gym") for the habit with the longest streak among the two habits.
    assert result == (4, "weeks", "Go to the gym")