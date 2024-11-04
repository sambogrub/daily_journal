'''This module will contain the main UI classes; today's page (main page), calendar page, and settings page'''

import tkinter as tk
from tkinter import ttk


class StyleManager:
    """This holds the configurations of the ttk styles used throughout the ui. 
    The separate class solely for styles, should help with readability and redundancy"""
    def __init__(self, root):
        self.root = root

        #initialize style instance
        self.style = ttk.Style(self.root)

        #set basic style to be used
        self.style.theme_use('alt')
        
        #call the style configuration function
        self.configure_styles()

    def configure_styles(self):
        #will be called to set specific styles for the app
        pass


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
        #this sets the tk.stringvar to the currently focused date
        self.date_str.set(self.cont.get_focus_date_str())

    def populate_frame(self):
        #this populates the frame with the date, text entry box, save entry button, as well as the calendar page button
        self.date_label = ttk.Label(self,textvariable=self.date_str)
        self.cal_page_button = ttk.Button(self, text = 'Cal Page', command = lambda: self.cont.show_page('calendar'))
        self.entry_textbox = tk.Text(self)
        self.save_entry_button = ttk.Button(self, text = 'Save Entry')

        #place the widgets
        self.date_label.place(anchor = 'n', relx = .5, y = 0, width = 150, height = 40)
        self.cal_page_button.place(anchor = 'ne', relx = .995, y = 0, width = 100, height = 40)
        self.entry_textbox.place(anchor = 'n', relx = .5, y = 45, relwidth= 1, relheight=.88)
        self.save_entry_button.place(anchor = 's', relx=.5, rely=.99, width = 125, height = 40)
        

class CalendarPage(ttk.Frame):
    """This is the second page. It has the calendar selection, the recent entries blurb,
    as well as the options button"""
    def __init__(self, root, controller_):
         #initialize the frame inheritance
        super().__init__(root)
        #place the main page frame
        self.place(anchor = 'ne',relx=1, y = 0, relwidth=.85, relheight=1)

        #call the populate frame function
        self.populate_frame()

    def populate_frame(self):
        #this will populate the calendar page frame
        self.calendar_label = ttk.Label(self, text= 'This is a quick test of the page change')

        #place the widgets
        self.calendar_label.place(anchor = 'n', relx = .5, y = 5, width = 200, height = 40)
        

class OptionsPage(ttk.Frame):
    """This is the third page. It will have the basic options that can be changed.
    It makes the change of style and font, as well as saving or deleting all entries """
    def __init__(self,root, controller_):
         #initialize the frame inheritance
        super().__init__(root)
        #place the main page frame
        self.place(x = 0, y = 0, relwidth=1, relheight=1)