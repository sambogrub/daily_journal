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
    def __init__(self, repository_, root: tk.Tk) -> None:
        self.data_controller = DataController(repository_)
        self.root = root

        #set the focus month at the beginning so it can be used by the ui. the focus day is set in the focus month setter
        
        self.focus_month = datetime.date.today()

        self.distribute_entries_to_month()
        
    
        #initialize the ui management after the initial business logic is complete
        self.ui_pages = self.init_ui_pages(self._focus_day)
        self.show_page(PageId.MAIN)

    #----------------------- focus day management -------------------

    @property
    def focus_day(self) -> model.Day:
        #using property decorator for the _focus_day variable so that it can be called easily
        return self._focus_day
    
    @focus_day.setter
    def focus_day(self, day: model.Day) -> None:
        self._focus_day = day

    #------------------------ focus month management ------------------

    @property
    def focus_month(self) -> model.Month:
        return self._focus_month
    
    @focus_month.setter
    def focus_month(self, date) -> None:
        self._focus_month = model.Month(date.month, date.year)
        #get the focus day here so that it will stay in sync with the focus month
        self._focus_day = self._focus_month[date.day]

    @property
    def month_cal(self) -> list[list[model.Day | None]]:
        #this returns the current month calendar reference matrix to be used in the ui to build the button matrix
        return self._focus_month.month_matrix
    
    @property
    def month_year_str(self) -> str: 
        #wanted to handle the string formatting here in controller rather than in the ui
        return f'{self._focus_month.month_name} {self._focus_month.year}'
    
    def adv_focus_month(self) -> None:
        #Had to have a way to keep track of the current date, so just used the focus date. 
        #Since the calendar is used only to choose a previous date
        cur_date = datetime.date(self._focus_month.year, self._focus_month.month_num, 1)
        next_month = cur_date + relativedelta(months = 1)
        self.focus_month = next_month
        self.distribute_entries_to_month()

    def rev_focus_month(self) -> None:
        #Had to have a way to keep track of the current date, so just used the focus date. 
        #Since the calendar is used only to choose a previous date
        cur_date = datetime.date(self._focus_month.year, self._focus_month.month_num, 1)
        next_month = cur_date + relativedelta(months = -1)
        self.focus_month = next_month
        self.distribute_entries_to_month()
    
    #------------------------- UI management ---------------------

    def init_ui_pages(self, init_day: model.Day) -> dict:
        pages = {
            PageId.MAIN: ui.MainPage(self.root, self, init_day),
            PageId.CALENDAR: ui.CalendarPage(self.root, self),
            PageId.OPTIONS: ui.OptionsPage(self.root, self)
        }
        return pages
    
    def show_page(self, page_name: PageId) -> None:
        #This is to let controller manage the ui view, raising the appropriate page to the top
        page = self.ui_pages.get(page_name)
        if page:
            page.tkraise()

    def calendar_button_clicked(self, day_of_month: int) -> None:
        """Call back method bound to calendar buttons. This switches focus to given day_of_month"""
        day = self._focus_month[day_of_month]
        self.focus_day = day
        self.ui_pages[PageId.MAIN].init_day_info(day)
        self.show_page(PageId.MAIN)

    def today_clicked(self) -> None:
        self.focus_month = datetime.date.today()
        self.distribute_entries_to_month()
        self.ui_pages[PageId.MAIN].init_day_info(self._focus_day)
        self.ui_pages[PageId.CALENDAR].refresh_calendar_frame()
        self.show_page(PageId.MAIN)

    #--------------------- Data Controller interaction ----------------------

    def save_day(self, entry):
        #wanted to make sure to extract the needed data to pass to the data controller,
        #rather than pass the day object
        date = self._focus_day.date
        if self._focus_day.entry:
            self.data_controller.update_entry(date, entry)
        else:
            self.data_controller.save_entry(date, entry)
        self._focus_day.set_entry(entry)

    def delete_entry(self, date: datetime.date):
        if self._focus_day.entry:
            self.data_controller.delete_entry(date)
            self._focus_day.delete_entry()

    def distribute_entries_to_month(self):
        #this should just request the entries from the data controller and pass it directly to the month instance
        start_date, end_date = self.focus_month.start_and_end_dates()
        entries = self.data_controller.get_months_entries(start_date, end_date)
        self._focus_month.populate_days_with_entries(entries)

    
    

class DataController:
    """This controller will interact with the repository and pass data to the main controller
    The data and main controller are separated in case the data controller needs to do more with the repository"""
    def __init__(self, repository_):
        self.entries = repository_

    def save_entry(self, date: datetime.date, entry: str):
        self.entries.store_entry(date, entry)

    def update_entry(self, date: datetime.date, entry: str):
        self.entries.update_entry(date, entry)
    
    def get_months_entries(self, start_date: datetime.date, end_date: datetime.date) -> list[tuple]:
        entries_list = self.entries.get_entries(start_date, end_date)
        return entries_list
    
    def delete_entry(self, date: datetime.date):
        self.entries.delete_entry(date)
    
    