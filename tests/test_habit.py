from datetime import datetime
import pytest
from habit_tracker import habit
from habit_tracker.habit import Habit

def test_habit_can_be_created():
    """Tests if a habit can be succesfully created and that its attributes are correctly set"""

    #Creates a habit with the name "Drink water" and periodicity "daily".
    habit = Habit("Drink water", "daily")

    #Checks that the habit's name and periodicity attributes are correctly set and that the created_at attribute is a datetime object.
    assert habit.name == "Drink water"
    assert habit.periodicity == "daily"
    assert isinstance(habit.created_at, datetime)

def test_invalid_periodicity_raises_error():
    """Tests whether an invalid periodicity (anything other than daily or weekly) raises an error"""

    #Tries to create a habit with an invalid periodicity value and checks that a ValueError is raised.
    with pytest.raises(ValueError):
        Habit("Drink water", "monthly")

def test_is_daily_returns_true_for_daily_habit():
    """Tests whether the is_daily method returns true for a habit with a daily periodicity"""
    #Creates a habit with daily periodicity.
    habit = Habit("Drink water", "daily")

    #Checks that the is_daily method returns true.
    assert habit.is_daily() is True

def test_is_daily_returns_false_for_weekly_habit():
    """Tests whether the is_daily method returns false for a habit with a weekly periodicity"""
    #Creates a habit with weekly periodicity.
    habit = Habit("Gym", "weekly")

    #Checks that the is_daily method returns false.
    assert habit.is_daily() is False