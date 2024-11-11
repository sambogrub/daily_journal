import datetime
import calendar as cal


class Entry:
    """Basic Entry class. Will hold the date and text for each entry"""
    def __init__(self, date: datetime, text: str = None):
        self.date = date
        self.text = text


class Day:
    """Day class to hold all entries and future parts"""
    def __init__(self, day_num: int):
        self.day_num = day_num
        self.entry = ''


class Month:
    """Month class to hold all days and month calendar"""
    def __init__(self, month_num: int, year: int):
        self.month_num = month_num
        self.year = year
        self.month_matrix = self.build_calendar_matrix()

    def build_calendar_matrix(self):
        month_matrix = cal.monthcalendar(self.year, self.month_num)
        if len(month_matrix) < 6:
            month_matrix.append([0,0,0,0,0,0,0])
        for i, week in enumerate(month_matrix):
            for j, day_num in enumerate(week):
                if day_num != 0:
                    month_matrix[i][j] = Day(day_num)
        return month_matrix
    

    