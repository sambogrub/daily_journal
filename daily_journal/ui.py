'''This module will contain the main UI classes; today's page (main page), calendar page, and settings page'''

import tkinter as tk
from tkinter import ttk


class MainPage(ttk.Frame):
    """This is the main page, has a basic layout of date, text entry box, and a save entry button.
    This will also have the button to get to the calendar page"""
    def __init__(self, root, controller_):
        #initialize the frame inheritance
        super().__init__(root)
        #place the main page frame
        self.place(x = 0, y = 0, relwidth=1, relheight=1)

        #set controller instance
        self.cont = controller_

        #initialize tk variables
        self.date_str = tk.StringVar()

        self.set_date_str()
        self.populate_frame()

    def set_date_str(self):
        self.date_str.set(self.cont.get_focus_date_str())

    def populate_frame(self):
        #this populates the frame with the date, text entry box, save entry button, as well as the calendar page button
        self.date_label = ttk.Label(self,textvariable=self.date_str)

        self.date_label.place(anchor = 'n', relx = .5, y = 0, width = 150, height = 40)
        

class CalendarPage(ttk.Frame):
    """This is the second page. It has the calendar selection, the recent entries blurb,
    as well as the options button"""
    def __init__(self, root, controller_):
         #initialize the frame inheritance
        super().__init__(root)
        #place the main page frame
        self.place(x = 0, y = 0, relwidth=1, relheight=1)
        

class OptionsPage(ttk.Frame):
    """This is the third page. It will have the basic options that can be changed.
    It makes the change of style and font, as well as saving or deleting all entries """
    def __init__(self,root, controller_):
         #initialize the frame inheritance
        super().__init__(root)
        #place the main page frame
        self.place(x = 0, y = 0, relwidth=1, relheight=1)