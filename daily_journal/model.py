import datetime
import calendar as cal


class Day:
    """Day class to hold all entries and future parts"""
    def __init__(self, date: datetime.date):
        self.date = date
        self.entry = ''
        self.date_string = self.get_date_string()
    
    def get_date_string(self) -> str:
        return datetime.datetime.strftime(self.date, '%B %d, %Y')


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
        self.weeks: list[Week] = self.build_calendar_matrix()
        self.last_day: int = 0
        self._first_day, self._number_of_days = cal.monthrange(year, month_number)

    def build_calendar_matrix(self) -> list[Week]:
        month_matrix = cal.monthcalendar(self.year, self.number)
        if len(month_matrix) < 6:
            month_matrix.append([0,0,0,0,0,0,0])
        for i, week in enumerate(month_matrix):
            for j, day_num in enumerate(week):
                if day_num != 0:
                    self.last_day = day_num
                    date = datetime.date(self.year, self.number, day_num)
                    month_matrix[i][j] = Day(date)
        return month_matrix

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
