import datetime
import calendar as cal


class Day:
    """Day class to hold all entries and future parts"""
    def __init__(self, date: datetime.date):
        self.date = date
        self.entry = ''
        self.date_string = self.get_date_string()
    
    def get_date_string(self):
        return datetime.datetime.strftime(self.date, '%B %d, %Y')


class Month:
    """Month class to hold all days and month calendar"""
    def __init__(self, month_num: int, year: int) -> list[list]:
        self.month_num = month_num
        self.year = year
        self.month_matrix = self.build_calendar_matrix()
        self.month_name = self.set_month_name()
        self.last_day = 0
        self._first_day, self._number_of_days = cal.monthrange(year, month_num)

    def __getitem__(self, day_of_month) -> Day:
        """Returns the requested day object. implementing this here ensures encapsulation"""
        if not 1 <= day_of_month <= self._number_of_days:
            raise IndexError(f'day_of_month must be between 1 and {self._number_of_days}, number given was {day_of_month}')
        week_index, day_index = divmod(day_of_month, 7)
        return self.month_matrix[week_index][day_index]

    def build_calendar_matrix(self):
        month_matrix = cal.monthcalendar(self.year, self.month_num)
        if len(month_matrix) < 6:
            month_matrix.append([0,0,0,0,0,0,0])
        for i, week in enumerate(month_matrix):
            for j, day_num in enumerate(week):
                if day_num != 0:
                    self.last_day = day_num
                    date = datetime.date(self.year, self.month_num, day_num)
                    month_matrix[i][j] = Day(date)
        return month_matrix
    
    def set_month_name(self):
        #this sets the string name for the month
        return cal.month_name[self.month_num]
    

    

    