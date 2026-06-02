from datetime import timedelta

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
        completed_periods.append(completed_at.date())
        """completed periods are added to the empty list complete_periods"""

    completed_periods = sorted(set(completed_periods))
    """removes duplicates and sortes the list"""

    if len(completed_periods) == 0:
        return 0
        """If there are no completions, return 0, as the longest streak is 0"""

    current_streak = 1
    longest_streak = 1

    for i in range(1, len(completed_periods)):
        """sets up a for loop, to loop over completed_periods ranging from 1 to the length of the list """
        previous_day = completed_periods[i - 1]
        current_day = completed_periods[i]



        if current_day == previous_day + timedelta(days=1):
            current_streak += 1
            """If two consecutive completons occur side by side, streak increases by 1"""
        else:
            current_streak = 1
            """Otherwise streak resets to 1"""

        
        if current_streak > longest_streak:
            longest_streak = current_streak
            """If the current streak is longer than longest_streak, longest_streak is set equal to current_streak"""
    
    return longest_streak