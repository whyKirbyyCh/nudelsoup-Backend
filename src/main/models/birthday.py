

class Birthday:
    """Class that represents a birthday."""

    def __init__(self, year: int, month: int, day: int) -> None:
        """
        Initializes the class with the month and day of the birthday.

        Args:
            year (int): The year of the birthday.
            month (int): The month of the birthday.
            day (int): The day of the birthday.

        Returns:
            None

        Raises:
            ValueError: If the year, month, or day is not there.
            TypeError: If the year, month, or day is not an integer.
        """
        if not year:
            raise ValueError("year must not be empty")

        if not isinstance(year, int):
            raise TypeError("year must be an integer")

        if not month:
            raise ValueError("month must not be empty")

        if not isinstance(month, int):
            raise TypeError("month must be an integer")

        if not day:
            raise ValueError("day must not be empty")

        if not isinstance(day, int):
            raise TypeError("day must be an integer")

        self.year = year
        self.month = month
        self.day = day
