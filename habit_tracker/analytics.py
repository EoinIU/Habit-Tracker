from calendar import week
from datetime import date, timedelta

def list_all_habits(habits):
    """This function returns all habits currenty tracked."""
    return habits

def list_all_habits_with_given_periodicity(habits, periodicity):
    """This function lists all habits with a given periodicity which is passed to the function as an argument."""

    matching_habits = []

    for habit in habits:
        if habit.periodicity == periodicity:
            matching_habits.append(habit)
    
    return matching_habits

def list_longest_streak_for_given_habit(habit):
    """This function calculates the longest streak for the habit passed to the function as an argument."""

    completed_periods = []

    for completed_at in habit.completions:

        if habit.is_daily():
            """If loop checks whether habit has daily periodicity"""
            completed_periods.append(completed_at.date())
            """completed periods are added to the empty list complete_periods"""
        else:
            """If the habit does not have daily periodicity, it must have weekly as that is the only other valid option"""
            iso_year, iso_week, _ = completed_at.isocalendar()
            week_start = date.fromisocalendar(iso_year, iso_week, 1)
            completed_periods.append(week_start)
            
    completed_periods = sorted(set(completed_periods))
    """removes duplicates and sortes the list"""

    if len(completed_periods) == 0:
        return 0
        """If there are no completions, return 0, as the longest streak is 0"""

    current_streak = 1
    longest_streak = 1

    for i in range(1, len(completed_periods)):
        """for loop that iterates over all completed periods"""
        previous_period = completed_periods[i - 1]
        current_period = completed_periods[i]

        if habit.is_daily():
            """Calculates the expected next period for habits with daily periodicity"""
            expected_next_period = previous_period + timedelta(days=1)
        else:
            """Calculates the expected next period for habits with weekly periodicity"""
            expected_next_period = previous_period + timedelta(weeks=1)

        if current_period == expected_next_period:
            """If the current period matches the expected next period, increment the current streak"""
            current_streak += 1
        else:
            """Otherwise, reset the current streak"""
            current_streak = 1

        if current_streak > longest_streak:
            """If the current streak is greater than the longest streak, update the longest streak"""
            longest_streak = current_streak

    return longest_streak

def return_longest_streak_of_all_habits(habits):
    """This function returns the longest streak of all habits currently tracked."""

    longest_streaks = {}

    for habit in habits:
        """for loop that iterates over all habits and calculates the longest streak for each habit, storing the result in a dictionary."""
        longest_streaks[habit.name] = list_longest_streak_for_given_habit(habit)

    if len(habits) == 0:
        """Checks if the habit list is empty and returns 0 if it is, as there are no habits to calculate streaks for."""
        return 0
    
    return max(longest_streaks.values())