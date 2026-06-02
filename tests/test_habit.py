import pytest
from habit_tracker.habit import Habit

def test_habit_can_be_created():
    """Tests if a habit can be succesfully created"""

    habit = Habit("Drink water", "daily")

    assert habit.name == "Drink water"
    assert habit.periodicity == "daily"

def test_invalid_periodicity_raises_error():
    """Tests whether an invalid periodicity (anything other than daily or weekly) raises an error"""

    with pytest.raises(ValueError):
        Habit("Drink water", "monthly")

def test_is_daily_returns_true_for_daily_habit():
    """Tests whether the is_daily method returns true for a habit with a daily periodicity"""
    habit = Habit("Drink water", "daily")

    assert habit.is_daily() is True

def test_is_daily_returns_false_for_weekly_habit():
    """Tests whether the is_daily method returns false for a habit with a weekly periodicity"""
    habit = Habit("Gym", "weekly")

    assert habit.is_daily() is False