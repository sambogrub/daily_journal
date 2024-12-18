"""The domain classes Day and Month are in thie module. They hold the date, entry, calendar reference matrix,
as well as other class specific methods"""

import datetime
import calendar as cal
from typing import Tuple

import logger


class Day:
    """Day class to hold all entries and future parts"""
    def __init__(self, date: datetime.date):
        self.date = date
        self.entry = ''
        self.date_string = self.get_date_string()
    
    def get_date_string(self):
        return f'{self.date:%B} {self.date.day}, {self.date.year}'
    
    def set_entry(self, entry: str):
        self.entry = entry

    def delete_entry(self):
        self.entry = ''


class Month:
    """Month class to hold all days and month calendar"""
    def __init__(self, month_num: int, year: int) -> list[list]:
        self.month_num = month_num
        self.year = year
        self.month_matrix = self.build_calendar_matrix()
        self.month_name = self.set_month_name()
        self.last_day = 0
        self._first_day, self._number_of_days = cal.monthrange(year, month_num)
        self.logger_ = logger.journal_logger()

    def __getitem__(self, day_of_month) -> Day:
        """Returns the requested day object. implementing this here ensures encapsulation"""
        if not 1 <= day_of_month <= self._number_of_days: #make sure the day of month requested is in the number of days range
            self.logger_.info(f'IndexError at Month __getitem__: day_of_month given, {day_of_month}, was outside of range 1 to {self._number_of_days}')
            day_of_month = self._number_of_days #set the day of month to the last day if it is out of the range
        matrix_index = self._first_day + day_of_month - 1
        week_index, day_index = divmod(matrix_index, 7)
        return self.month_matrix[week_index][day_index]

    def build_calendar_matrix(self) -> list[list]:
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
    
    def populate_days_with_entries(self, entries: list[tuple]):
        #this should take a bulk list of entries and parse them to the correct day
        #this is in the month class to ensure any controller does not have to use this business logic
        if entries:
            for item in entries:
                date, entry = item 
                y, m, day_of_month = date.split('-')
                day = self.__getitem__(int(day_of_month))
                day.set_entry(entry)
    
    def set_month_name(self):
        #this sets the string name for the month
        return cal.month_name[self.month_num]
    
    def start_and_end_dates(self) -> Tuple[datetime.date, datetime.date]:
        #I put this here to ensure that the correct first and last day of the month are used
        start_date = datetime.date(self.year, self.month_num, 1)
        end_date = datetime.date(self.year, self.month_num, self._number_of_days)
        return start_date, end_date
    

    

    