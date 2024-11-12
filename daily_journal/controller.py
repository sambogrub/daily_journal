"""this is the module that will hold the controller for the daily journal app"""
import model
import ui

import datetime
import tkinter as tk
import calendar as cal
from dateutil.relativedelta import relativedelta

class Controller:
    """Controller for Daily Journal. Will be responsible for interactions with the repository,
    passing entry objects between ui and the repository"""
    def __init__(self, repository_, root: tk.Tk):
        self.data_controller = DataController(repository_)
        self.root = root

        #set the initial focus date and calendar matrix before ui is initialized
        self._focus_date = self.set_focus_date()
        self._focus_month = self.set_focus_month(self._focus_date)

        init_day = self.get_init_day()

        self.ui_pages = self.init_ui_pages(init_day)

        #start building the app
        self.app_start()
        
    def app_start(self):
        # this function will call all needed functions to start the app. 
        # It will call to initialize a new entry for the current day,
        # and it will call to start the UI.
        self.show_page('main')

    def init_ui_pages(self, init_day: datetime.date) -> dict:
        #this initializes the ui pages to be called when needed
        pages = {
            'main': ui.MainPage(self.root, self, init_day),
            'calendar': ui.CalendarPage(self.root, self),
            'options': ui.OptionsPage(self.root, self)
        }
        return pages
    
    def show_page(self, page_name: str):
        #This raises the indicated page to the top of the view
        page = self.ui_pages.get(page_name)
        if page:
            page.tkraise()

    def set_focus_date(self, date: datetime.date = datetime.date.today()):
        #This sets the focus date fo the journal entry, will set it to 'today's' date if none is provided
        return date
        
    def set_focus_month(self, date):
        #This gets the month object that is focused on at the moment
        
        return model.Month(date.month, date.year)

    def get_focus_date(self) -> datetime.date:
        #this returns the currently focused date
        return self._focus_date
    
    def get_month_cal(self):
        #this returns the current month calendar matrix
        return self._focus_month.month_matrix
    
    def get_month_name(self) -> str:
        #this returns the current focused month's name 
        return self._focus_month.month_name

    def get_focus_date_str(self) ->str:
        #returns a string of the date in 'MonthName Day, Year' format
        month_str = cal.month_name[self._focus_date.month]
        date_str = f'{month_str} {self._focus_date.day}, {self._focus_date.year}'
        return date_str

    def adv_focus_month(self):
        #advances the focus month by one
        cur_date = datetime.date(self._focus_month.year, self._focus_month.month_num, 1)
        next_month = cur_date + relativedelta(months = 1)
        self._focus_month = self.set_focus_month(next_month)

    def rev_focus_month(self):
        #advances the focus month by one
        cur_date = datetime.date(self._focus_month.year, self._focus_month.month_num, 1)
        next_month = cur_date + relativedelta(months = -1)
        self._focus_month = self.set_focus_month(next_month)
        
    def calendar_button_clicked(self, i, j):
        #pulls the specific date referenced from the button calendar, and passes the date from the clicked day to the 
        #set focus date function
        day = self._focus_month.month_matrix[i][j]
        self.set_focus_date(day.date)
        self.ui_pages['main'].init_day_info(day)
        self.show_page('main')

    def get_init_day(self):
        #this gets the intial day object
        for week in self._focus_month.month_matrix:
            for day in week:
                if day != 0:
                    if day.date.day == self._focus_date.day:
                        return day

    def init_new_entry(self, date: datetime, text: str = None) -> object: #returns a new entry object
        # this function will create a new entry with the given date. 
        pass

    def assign_db_text_to_entry(self, entry) -> object: # returns the same entry object with a possible entry text
        # this function will get the text from the repository for the entry's date, if any exists
        pass

    def assign_ui_text_to_entry(self, entry, text) -> object:
        #this function will assign the given text from the ui textbox to the 
        pass


class DataController:
    """This controller will interact with the repository and pass data to the main controller"""
    def __init__(self, repository_):
        self.entries = repository_
