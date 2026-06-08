from calendar import week
from datetime import date, timedelta

def list_all_habits(habits):
    """Return names and periodicities for all currently tracked habits."""
    return [(habit.name, habit.periodicity) for habit in habits]

def list_all_habits_with_given_periodicity(habits, periodicity):
    """This function lists all habits with a given periodicity which is passed to the function as an argument."""

   # Initializes an empty list to store habits that match the given periodicity.
    matching_habits = []

    #Iterates over all habits and checks if the periodicity of each habit matches the given periodicity. If it does, the habit is added to the list of matching habits.
    for habit in habits:
        if habit.periodicity == periodicity:
            matching_habits.append(habit)
    
    #Returns the list of habits that match the given periodicity.
    return matching_habits

def list_longest_streak_for_given_habit(habit):
    """This function calculates the longest streak for the habit passed to the function as an argument."""

    #Initializes an empty list to store the completed periods for this habit. A completed period is a day for habits with daily periodicity, or a week for habits with weekly periodicity, in which the habit was completed.
    completed_periods = []

    #Iterates over all completions for this habit and calculates the corresponding completed period for each completion. The completed periods are added to the list of completed periods for this habit.
    for completed_at in habit.completions:

        #For habits with daily periodicity, the completed period is the date of the completion. 
        if habit.is_daily():
            completed_periods.append(completed_at.date())
        #For habits with weekly periodicity, the completed period is the date of the Monday of the week of the completion, which is calculated using the isocalendar method and the fromisocalendar method from the datetime module.
        else:
            iso_year, iso_week, _ = completed_at.isocalendar()
            week_start = date.fromisocalendar(iso_year, iso_week, 1)
            completed_periods.append(week_start)
            
    #Removes duplicates and sorts the list
    completed_periods = sorted(set(completed_periods))

    #If there are no completed periods, the longest streak is 0, so the function returns 0.
    if len(completed_periods) == 0:
        return 0

    #Initializes the current streak and longest streak to 1, as the minimum streak is 1 if there is at least one completed period.
    current_streak = 1
    longest_streak = 1

    #Iterates over the completed periods and compares each completed period to the previous one to check if they are consecutive.
    for i in range(1, len(completed_periods)):
        previous_period = completed_periods[i - 1]
        current_period = completed_periods[i]

        #Calculates the expected next period based on the periodicity of the habit. For daily habits, the expected next period is the previous period plus one day. 
        if habit.is_daily():
            expected_next_period = previous_period + timedelta(days=1)
        #For weekly habits, the expected next period is the previous period plus one week.
        else:
            expected_next_period = previous_period + timedelta(weeks=1)

        #Checks if the current period matches the expected next period. If it does, the current streak is incremented. 
        if current_period == expected_next_period:
            current_streak += 1
        #If not, the current streak is reset to 1. The longest streak is updated whenever the current streak exceeds it.
        else:
            current_streak = 1

        #Checks if the current streak is greater than the longest streak and updates the longest streak if necessary.
        if current_streak > longest_streak:
            longest_streak = current_streak

    #Returns the longest streak for this habit.
    return longest_streak

def return_longest_streak_of_all_habits(habits):
    """Return the longest streak, unit, and habit name across all tracked habits."""

    #If there are no habits tracked yet, the function returns 0 for the longest streak and None for the unit and habit name.
    if len(habits) == 0:
        return 0, None, None

    #Initializes variables to keep track of the longest streak, unit, and habit name across all tracked habits.
    best_streak = 0
    best_unit = None
    best_habit_name = None

    #Iterates over all tracked habits and calculates the longest streak for each habit using the list_longest_streak_for_given_habit function. 
    for habit in habits:
        #Calculates the longest streak for this habit and assigns it to the variable streak.
        streak = list_longest_streak_for_given_habit(habit)
        #The unit is determined based on whether the habit has daily or weekly periodicity using the is_daily method. 
        unit = "days" if habit.is_daily() else "weeks"
        #If the longest streak for a habit is greater than the best streak found so far, the best streak, unit, and habit name are updated accordingly.
        if streak > best_streak:
            best_streak = streak
            best_unit = unit
            best_habit_name = habit.name

    #Returns the longest streak, unit, and habit name across all tracked habits.
    return best_streak, best_unit, best_habit_name