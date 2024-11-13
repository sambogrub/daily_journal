import datetime
import calendar as cal


class Day:
    """Day class to hold all entries and future parts"""
    def __init__(self, date: datetime.date, entry: str = ''):
        self.date = date
        self.entry = entry
        self.date_string = self.get_date_string()

    # FIXME: this method doesn't seem to be used anywhere but in __init__.
    # I'd recommend to drop it for good and use just
    # 'self.date_string = date.strftime('%B %d, %Y')' in the __init__.
    def get_date_string(self):
        return datetime.datetime.strftime(self.date, '%B %d, %Y')


def day(year: int, month: int, day_: int) -> Day:
    """ Factory function simplifying creation of new Day instances """
    return Day(datetime.date(year, month, day_))


type Week = list[Day|None]
""" 
Represents 7 days of a week. Entries with None value
are days of the past or the future month.
"""


class Month:
    """Month class to hold all days and month calendar"""
    def __init__(self, month_num: int, year: int):
        # TODO: consider renaming month_num to number as it's always clear
        # from the context, that it's Month.number :-)
        self.month_num: int = month_num
        self.year: int = year
        # TODO: consider renaming month_matrix to weeks
        self.month_matrix: list[Week] = self.build_calendar_matrix()
        # general comment for __init__ - it's better to specify types
        # of instance attributes explicitly

    def build_calendar_matrix(self):
        month_matrix = cal.monthcalendar(self.year, self.month_num)
        if len(month_matrix) < 6:
            month_matrix.append([0,0,0,0,0,0,0])
        for i, week in enumerate(month_matrix):
            for j, day_num in enumerate(week):
                # FIXME: every integer other than 0 is evaluated at True in a condition.
                # It's seen as a best practice approach to use 'if day_num:'
                if day_num != 0:
                    date = datetime.date(self.year, self.month_num, day_num)
                    # python type error checker doesn't like this line as you're
                    # mixing integers and Days in the same list. It works, 'cause
                    # python doesn't care about the item types in the list, but
                    # heterogeneous lists can be a source of hard to find errors...
                    month_matrix[i][j] = Day(date)
        # TL;DR - Even if it's possible to reuse month_matrix list by converting it
        # from list[list[int]] to list[list[Day | int]], it's not a recommended way...
        return month_matrix

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

    # TODO: consider renaming this property from month_name to name, as it's
    # always clear from the context, that it belongs to the Month.
    @property
    def month_name(self) -> str:
        return cal.month_name[self.month_num]

