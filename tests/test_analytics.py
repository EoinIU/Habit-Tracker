from habit_tracker.analytics import list_all_habits, list_all_habits_with_given_periodicity, list_longest_streak_for_given_habit
from habit_tracker.habit import Habit
from datetime import datetime

"""Habits to be used for testing."""
habit1 = Habit("Drink water", "daily")
habit2 = Habit("Gym", "weekly")
habits_list = [habit1, habit2]

def test_list_all_habits():
    """Tests that the function to list all habits returns a list of all habits."""

    result = list_all_habits(habits_list)

    assert result == [habit1, habit2] 

def test_all_habits_daily():
    """Tests if all daily habits can be listed."""

    result = list_all_habits_with_given_periodicity(habits_list, "daily")

    assert result == [habit1]

def test_all_habits_weekly():
    """Tests if all weekly habits can be listed."""

    result = list_all_habits_with_given_periodicity(habits_list, "weekly")

    assert result == [habit2]

def test_longest_streak_for_daily_habit():
    """tests the logic for calculating the longest streak for a daily habit"""
    habit = Habit("Drink water", "daily")

    habit.complete(datetime(2025, 1, 1))
    habit.complete(datetime(2025, 1, 2))
    habit.complete(datetime(2025, 1, 3))

    result = list_longest_streak_for_given_habit(habit)

    assert result == 3