"""this is the module that will hold the controller for the daily journal app"""
import model
import ui

import datetime
import tkinter as tk
import calendar as cal

class Controller:
    """Controller for Daily Journal. Will be responsible for interactions with the repository,
    passing entry objects between ui and the repository"""
    def __init__(self, repository_, root: tk.Tk):
        self.data_controller = DataController(repository_)
        self.root = root

        #set the initial focus date and calendar matrix before ui is initialized
        self.set_focus_date()
        self.set_focus_month()

        self.ui_pages = self.init_ui_pages()

        #start building the app
        self.app_start()
        
    def app_start(self):
        # this function will call all needed functions to start the app. 
        # It will call to initialize a new entry for the current day,
        # and it will call to start the UI.
        self.show_page('main')

    def init_ui_pages(self) -> dict:
        #this initializes the ui pages to be called when needed
        pages = {
            'main': ui.MainPage(self.root, self),
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
        self._focus_date = date
        
    def set_focus_month(self):
        #This gets the month object that is focused on at the moment
        month_num = self._focus_date.month
        year = self._focus_date.year
        self._focus_month = model.Month(month_num, year)

    def get_focus_date(self) -> datetime.date:
        #this returns the currently focused date
        return self._focus_date
    
    def get_month_cal(self):
        #this returns the current month calendar matrix
        return self._focus_month.month_matrix

    def get_focus_date_str(self) ->str:
        #returns a string of the date in 'MonthName Day, Year' format
        month_str = cal.month_name[self._focus_date.month]
        date_str = f'{month_str} {self._focus_date.day}, {self._focus_date.year}'
        return date_str

    def calendar_button_clicked(self, i, j):
        #pulls the specific date referenced from the button calendar, and passes the date from the clicked day to the 
        #set focus date function
        day = self._focus_month.month_matrix[i][j]
        self.set_focus_date(day.date)
        self.ui_pages['main'].set_date_str()
        self.show_page('main')

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
