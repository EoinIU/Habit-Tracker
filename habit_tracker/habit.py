from datetime import datetime

class Habit:
    """This defines the Habit class, which will be used to create Habit objects."""

    VALID_PERIODICITIES = ["daily", "weekly"]
    """As this app will support daily and weekly periodicities, this defines valid periodicity values at the class level."""

    def __init__(self, name, periodicity):
        if periodicity not in self.VALID_PERIODICITIES:
            raise ValueError("Periodicity can be either 'daily' or 'weekly'.")
            """Checks if the periodicity of a new habit is valid and throws an error if not."""
        
        """Attributes"""    
        self.name = name
        """Name attribute"""
        self.periodicity = periodicity
        """Periodicity attribute"""

    """Methods"""
    def complete(self, completed_at=None):
        """Record a completion for this habit. A datetime value can be passed as an argument, which might be useful for testing. If no datetime value is provided, the current time and date will be used."""
        if completed_at is None:
            completed_at = datetime.now()
    def is_daily(self):
        """Returns true if this habit has daily periodicity, or false if the periodicity is weekly (the only other valid option for periodicity)"""
        return self.periodicity == "daily"

        