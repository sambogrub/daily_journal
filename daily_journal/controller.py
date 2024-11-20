"""this is the module that will hold the controller for the daily journal app"""
import datetime
import tkinter as tk
from enum import StrEnum
from dateutil.relativedelta import relativedelta

import model
import ui


class PageId(StrEnum):
    """IDs of all UI Pages. Using StrEnum to make sure everything stays constant and ensure type control"""
    MAIN = 'main'
    CALENDAR = 'calendar'
    OPTIONS = 'options'


class Controller:
    """Controller for Daily Journal. Will be responsible for interactions with the repository,
    passing entry objects between ui and the repository"""
    def __init__(self, repository_, root: tk.Tk):
        self.data_controller = DataController(repository_)
        self.root = root

        #set the initial focus date and calendar matrix before UI is initialized, that way it is usable by UI
        today = datetime.date.today()
        self._focus_month = self.set_focus_month(today)
        self._focus_day = self._focus_month[today.day]

        #initialize the ui management after the initial business logic is complete
        self.ui_pages = self.init_ui_pages(self._focus_day)
        self.show_page(PageId.MAIN)

    #----------------------- focus date and day management -------------------

    @property
    def focus_day(self) -> model.Day:
        #using property decorator for the _focus_day variable so that it can be called easily
        return self._focus_day
    
    @focus_day.setter
    def focus_day(self, day: model.Day):
        self._focus_day = day

    #------------------------ focus month management ------------------

    def set_focus_month(self, date):
        #This gets the instance of the currently focused month, so it can be used in the calendar
        return model.Month(date.month, date.year)

    def get_month_cal(self):
        #this returns the current month calendar reference matrix to be used in the ui to build the button matrix
        return self._focus_month.month_matrix
    
    def get_month_year_str(self) -> str: 
        #wanted to handle the string formatting here in controller rather than in the ui
        return f'{self._focus_month.month_name} {self._focus_month.year}'
    
    def adv_focus_month(self):
        #Had to have a way to keep track of the current date, so just used the focus date. 
        #Since the calendar is used only to choose a previous date
        cur_date = datetime.date(self._focus_month.year, self._focus_month.month_num, 1)
        next_month = cur_date + relativedelta(months = 1)
        self._focus_month = self.set_focus_month(next_month)

    def rev_focus_month(self):
        #Had to have a way to keep track of the current date, so just used the focus date. 
        #Since the calendar is used only to choose a previous date
        cur_date = datetime.date(self._focus_month.year, self._focus_month.month_num, 1)
        next_month = cur_date + relativedelta(months = -1)
        self._focus_month = self.set_focus_month(next_month)
    
    #------------------------- UI management ---------------------

    def init_ui_pages(self, init_day: model.Day) -> dict:
        pages = {
            PageId.MAIN: ui.MainPage(self.root, self, init_day),
            PageId.CALENDAR: ui.CalendarPage(self.root, self),
            PageId.OPTIONS: ui.OptionsPage(self.root, self)
        }
        return pages
    
    def show_page(self, page_name: PageId):
        #This is to let controller manage the ui view, raising the appropriate page to the top
        page = self.ui_pages.get(page_name)
        if page:
            page.tkraise()

    def calendar_button_clicked(self, i, j):
        #pulls the specific day referenced from the button calendar from the ui by i and j, 
        # and passes the date from the clicked day to the set focus date function
        day = self._focus_month.month_matrix[i][j]
        self.focus_day = day
        self.focus_date = day.date
        self.ui_pages[PageId.MAIN].init_day_info(day)
        self.show_page(PageId.MAIN)

    #--------------------- Data Controller interaction ----------------------

    def save_day(self):
        #wanted to make sure to extract the needed data to pass to the data controller,
        #rather than pas the day object
        date = self._focus_day.date
        entry = self._focus_day.entry
        self.data_controller.save_entry(date, entry)
    

class DataController:
    """This controller will interact with the repository and pass data to the main controller"""
    def __init__(self, repository_):
        self.entries = repository_

    def save_entry(self, date, entry):
        self.entries.store_entry(date, entry)

    def get_months_entries(self, start_date, end_date) -> dict:
        entries_dict = self.entries.get_entries(start_date, end_date)