"""this is the module that will hold the controller for the daily journal app"""
import datetime
import tkinter as tk
from enum import StrEnum

import logger
import model
import ui


class PageId(StrEnum):
    """ IDs of all UI Pages """
    MAIN = 'main'
    CALENDAR = 'calendar'
    OPTIONS = 'options'


class Controller:
    """Controller for Daily Journal. Will be responsible for interactions with the repository,
    passing entry objects between ui and the repository"""
    def __init__(self, repository_, root: tk.Tk, logger_ = logger.journal_logger()):
        self._logger = logger_
        self.data_controller = DataController(repository_)
        self.root = root

        #set the initial focus date and calendar matrix before UI is initialized, that way it is usable by UI
        self.focus_month = datetime.date.today()

        #initialize the ui management after the initial business logic is complete
        self.ui_pages: dict[PageId, ui.UiPage] = self.init_ui_pages()

        self.ui_pages[PageId.MAIN].update_day_info(self._focus_day)
        self.show_page(PageId.MAIN)

    #----------------------- focus date and day management -------------------

    @property
    def focus_day(self) -> model.Day:
        #using property decorator for the _focus_day variable so that it can be called easily
        return self._focus_day
    
    @focus_day.setter
    def focus_day(self, day: model.Day) -> None:
        # TODO - consider adding logic checking, if new day is within focus_month
        # the point is to always keep focus_day and focus_month in sync
        self._focus_day = day

    #------------------------ focus month management ------------------

    @property
    def focus_month(self) -> model.Month:
        return self._focus_month

    @focus_month.setter
    def focus_month(self, date) -> None:
        self._focus_month = model.Month(date.month, date.year)
        # don't let focus_day stuck in the wrong month
        self._focus_day = self._focus_month[date.day]

    @property
    def month_cal(self) -> list[list[model.Day | None]]:
        #this returns the current month calendar reference matrix to be used in the ui to build the button matrix
        return self._focus_month.weeks

    #------------------------- UI management ---------------------

    def init_ui_pages(self) -> dict[PageId, ui.UiPage]:
        main_page = ui.MainPage(
            root=self.root,
            cal_btn_callback=lambda: self.show_page(PageId.CALENDAR),
            # save handler does nothing for now
            save_btn_callback=lambda: ...
        )
        cal_page = ui.CalendarPage(
            root=self.root,
            month=self._focus_month,
            change_month_callback=self.change_month_handler,
            select_day_callback=self.calendar_button_clicked,
        )
        pages = {
            PageId.MAIN: main_page,
            PageId.CALENDAR: cal_page,
            PageId.OPTIONS: ui.OptionsPage(self.root, self)
        }
        return pages
    
    def show_page(self, page_name: PageId) -> None:
        """ Raise desired page to the top making it visible, while hiding the remaining pages. """
        try:
            self.ui_pages[page_name].tkraise()
        except KeyError:
            self._logger.exception(f'Request to show unknown page {page_name}')

    def calendar_button_clicked(self, day_of_month: int) -> None:
        """ Callback method bound to calendar buttons. Switches focus to given day_of_month """
        day = self._focus_month[day_of_month]
        self.focus_day = day
        self.ui_pages[PageId.MAIN].update_day_info(day)
        self.show_page(PageId.MAIN)

    def change_month_handler(self, month_delta: int) -> None:
        """ Callback handling change of the focus_month """
        self._focus_month += month_delta
        self._focus_day = 1
        self.ui_pages[PageId.CALENDAR].update_calendar(self._focus_month)

    #--------------------- Data Controller interaction ----------------------

    def save_day(self) -> None:
        #wanted to make sure to extract the needed data to pass to the data controller,
        #rather than pas the day object
        date = self._focus_day.date
        entry = self._focus_day.entry
        self.data_controller.save_entry(date, entry)
    

class DataController:
    """This controller will interact with the repository and pass data to the main controller"""
    def __init__(self, repository_):
        self.entries = repository_

    def save_entry(self, date, entry) -> None:
        self.entries.store_entry(date, entry)

    def get_months_entries(self, start_date, end_date) -> dict:
        entries_dict = self.entries.get_entries(start_date, end_date)
