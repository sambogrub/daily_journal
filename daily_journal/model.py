import datetime
import calendar as cal


class Day:
    """Day class to hold all entries and future parts"""
    def __init__(self, date: datetime.date, entry: str = ''):
        self.date = date
        self.entry = entry
        self.date_string = date.strftime('%B %d, %Y')

def day(year: int, month: int, day_: int) -> Day:
    """ Factory function simplifying creation of new Day instances """
    return Day(datetime.date(year, month, day_))


type Week = list[Day | None]
""" 
Represents 7 days of a week. Entries with None value
are days of the past or the future month.
"""


class Month:
    """Month class to hold all days and month calendar"""
    def __init__(self, month_number: int, year: int):
        self.number: int = month_number
        self.year: int = year
        self.name: str = cal.month_name[month_number]
        self.weeks: list[Week] = self.week_list(year_=year, month_=month_number)
        self._first_day, self._number_of_days = cal.monthrange(year, month_number)

    @staticmethod
    def week_list(year_: int, month_: int) -> list[Week]:
        """
        Builds list of weeks for the given year and month.

        Each Week is a list of 7 Day instances. Weeks which
        span through the previous or the next month are padded
        with None instead of Day instances.
        """
        month_calendar = cal.monthcalendar(year_, month_)
        # ensure there are always 6 weeks as it helps to simplify UI layout
        if len(month_calendar) < 6:
            month_calendar.append([0] * 7)
        weeks = [
            # source day_ is mapped to None if it doesn't belong to the given month_
            [day(year_, month_, day_) if day_ else None for day_ in week]
            for week in month_calendar
        ]
        return weeks

    @property
    def month_year(self) -> str:
        return f'{self.name} {self.year}'

    def __getitem__(self, day_of_month: int) -> Day:
        """ Returns requested day of this month """
        if not 1 <= day_of_month <= self._number_of_days:
            raise IndexError(f'day_of_month must be between 1 and {self._number_of_days}, but was {day_of_month}.')
        matrix_day = self._first_day + day_of_month - 1
        week_index, day_index = divmod(matrix_day, 7)
        return self.weeks[week_index][day_index]

    def _delta(self, delta: int) -> 'Month':
        """
        Helper method creating new Month instance which is "delta" months
        in the future (if delta > 0) or past (if delta < 0).
        """
        year_diff, new_month = divmod(self.number + delta, 12)
        if not new_month:
            # December will always come out as 0 when using mod
            new_month = 12
            # December will always have additional (unwanted) year when using div
            year_diff -= 1
        return Month(new_month, self.year + year_diff)

    def __add__(self, months_delta: int) -> 'Month':
        """
        Creates a new Month instance which will be "months_delta"
        months in the future compared to the month the self represents.
        """
        return self._delta(delta=months_delta)

    def __sub__(self, months_delta: int) -> 'Month':
        """
        Creates a new Month instance which will be "months_delta"
        months in the past compared to the month the self represents.
        """
        return self._delta(delta=-months_delta)
