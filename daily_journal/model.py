import datetime
import calendar as cal


class Day:
    """Day class to hold all entries and future parts"""
    def __init__(self, date: datetime.date):
        self.date = date
        self.entry = ''


class Month:
    """Month class to hold all days and month calendar"""
    def __init__(self, month_num: int, year: int) -> list[list]:
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
                    date = datetime.date(self.year, self.month_num, day_num)
                    month_matrix[i][j] = Day(date)
        return month_matrix
    

    