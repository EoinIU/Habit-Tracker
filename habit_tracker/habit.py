from datetime import datetime

class Habit:
    """This defines the Habit class, which will be used to create Habit objects."""

    #As this app will support daily and weekly periodicities, this defines valid periodicity values at the class level.
    VALID_PERIODICITIES = ["daily", "weekly"]

    def __init__(self, name, periodicity, completions=None):
        """Checks if the periodicity of a new habit is valid and throws an error if not."""
        if periodicity not in self.VALID_PERIODICITIES:
            raise ValueError("Periodicity can be either 'daily' or 'weekly'.")
            
        
        #Attributes 
        # #Name attribute   
        self.name = name
        #Periodicity attribute
        self.periodicity = periodicity
        #Completions attribute, which is a list of datetimes when the habit was completed. This will be used to calculate streaks.
        self.completions = []
        #Created_at attribute, which is the datetime when the habit was created.
        self.created_at = datetime.now()

    #Methods
    def complete(self, completed_at=None):
        """Record a completion for this habit. A datetime value can be passed as an argument, which might be useful for testing. If no datetime value is provided, the current time and date will be used."""
        if completed_at is None:
            completed_at = datetime.now()
            
        #Appends the datetime of the completion to the completions list for this habit.
        self.completions.append(completed_at)

    def is_daily(self):
        """Returns true if this habit has daily periodicity, or false if the periodicity is weekly (the only other valid option for periodicity)"""
        return self.periodicity == "daily"

        