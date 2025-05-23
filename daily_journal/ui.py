"""This module will contain the main UI classes; today's page (main page), calendar page, and settings page"""

import tkinter as tk
from tkinter import ttk
from functools import partial

import logger


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
        """Defines the styles for different widgets."""
        # Global styles
        self.style.configure('TLabel', font=('Helvetica', 12), padding=5)
        self.style.configure('TButton', font=('Helvetica', 12, 'bold'), padding=5)
        self.style.configure('TFrame', background='#f0f0f0')

        # Entry box style
        self.style.configure('TText', background='#ffffff', padding=5, relief='flat')

        # Calendar day buttons
        self.style.configure('CalendarButton.TButton', background='#e6f7ff', foreground='#004080')
        self.style.map('CalendarButton.TButton', background=[('active', '#cce7ff')])

        # Save button
        self.style.configure('SaveButton.TButton', background='#4CAF50', foreground='#ffffff')
        self.style.map('SaveButton.TButton', background=[('active', '#45a049')])

        # Navigation buttons
        self.style.configure('NavButton.TButton', background='#4CAF50', foreground='#ffffff')
        self.style.map('NavButton.TButton', background=[('active', '#0056b3')])

    def set_dark_mode(self):
        """Switches to a dark mode theme."""
        self.style.configure('TLabel', background='#2e2e2e', foreground='#f0f0f0')
        self.style.configure('TButton', background='#444444', foreground='#f0f0f0')
        self.style.configure('TFrame', background='#1e1e1e')
        self.style.configure('TText', background='#3e3e3e', foreground='#ffffff')

    def set_light_mode(self):
        """Switches to a light mode theme."""
        self.configure_styles()  # Reset to default light theme styles


class MainPage(ttk.Frame):
    """This is the main page, has a basic layout of date, text entry box, and a save entry button.
    This will also have the button to get to the calendar page"""
    def __init__(self, root, controller_, init_day):
        #initialize the frame inheritance
        super().__init__(root)

        self.log = logger.journal_logger()

        #place the main page frame
        self.place(x=0, y=0, relwidth=1, relheight=1)

        #name the passed controller instance
        self.cont = controller_

        #initialize tk variables
        self.date_str = tk.StringVar()

        self.populate_frame()
        self.init_day_info(init_day)
    
    def init_day_info(self, day):
        #this takes the day object and passes the needed info to the proper locations
        self.clear_textbox()
        self.set_date_str(day)
        self.populate_textbox(day)
        
    def set_date_str(self, day):
        #this sets the tk.stringvar to the currently focused date
        self.date_str.set(day.date_string)

    def populate_frame(self):
        #this populates the frame with the date, text entry box, save entry button, as well as the calendar page button
        self.date_label = ttk.Label(self, textvariable=self.date_str)
        self.cal_page_button = ttk.Button(self, text='Calendar Page', style='NavButton.TButton', command=lambda: self.cont.show_page('calendar'))
        self.entry_textbox = tk.Text(self, wrap='none')
        self.save_entry_button = ttk.Button(self, text='Save Entry', style='SaveButton.TButton', command=self.save_entry_button_clicked)

        #place the widgets
        self.date_label.place(anchor='n', relx=.5, y=0, width=150, height=40)
        self.cal_page_button.place(anchor='ne', relx=.995, y=5, width=150, height=40)
        self.entry_textbox.place(anchor='n', relx=.5, y=45, relwidth=1, relheight=.88)
        self.save_entry_button.place(anchor='s', relx=.5, rely=.99, width=125, height=40)
    
    def save_entry_button_clicked(self):
        #this should grab the text in the tkinter text widget, then send it to the controller,
        #the controller should already be aware of the days date
        entry = self.entry_textbox.get('1.0', 'end-1c')
        self.cont.save_day(entry)

    def clear_textbox(self):
        #this should be called any time a new date is selected
        self.entry_textbox.delete('1.0', 'end')

    def populate_textbox(self, day):
        entry = day.entry
        self.entry_textbox.insert('1.0', entry)


class CalendarPage(ttk.Frame):
    """This is the second page. It has the calendar selection, the recent entries blurb,
    as well as the options button"""
    def __init__(self, root, controller_):
        
        super().__init__(root)

        self.log = logger.journal_logger()

        #use place for the curent frame as it is more versitile
        self.place(anchor='ne',relx=1, y=0, relwidth=.85, relheight=1)

        
        self.cont = controller_

        
        self.month_name_var = tk.StringVar()
       # the month name variable is set in the populate calendar frame function
       # this is to reduce redundancy
        
        
        self.populate_frame()

    def populate_frame(self):
        date_snips = {'12-7-2024':'This entry is a test', '12-6-2024':'This is also a test', '12-1-2024':'Testing with the third one'}

        self.calendar_label = ttk.Label(self, textvariable=self.month_name_var)
        self.prev_month_button = ttk.Button(self, text='Prev', command=self.reverse_calendar)
        self.next_month_button = ttk.Button(self, text='Next', command=self.advance_calendar)
        self.calendar_frame = CalendarFrame(self, self.cont)
        self.refresh_calendar_frame()
        self.today_button = ttk.Button(self, text='Today', command=self.cont.today_clicked)
        self.recent_entries = RecentEntriesFrame(self, self.cont)

        
        self.calendar_label.place(anchor='n', relx=.5, y=5, width=120, height=40)
        self.calendar_frame.place(anchor='center', relx=.5, rely=.25, width=300, height=300)
        self.prev_month_button.place(anchor='n', relx=.25, y=5, width=75, height=40)
        self.next_month_button.place(anchor='n', relx=.75, y=5, width=75, height=40)
        self.today_button.place(x=5, rely=.15, width=50, height=45)
        self.recent_entries.place(anchor='se', relx=.99, rely=.99, relwidth=.97, relheight=.45)

        recent_entries_data = self.cont.get_recent_entries()

        self.recent_entries.set_date_entry_text(recent_entries_data)

    def refresh_calendar_frame(self):
        """This function was made separate from the calendar frame class to make it easier for the controller to call"""
        self.calendar_frame.populate_calendar_frame()
        self.set_month_name_var()

    def advance_calendar(self):
        self.cont.adv_focus_month()   
        self.set_month_name_var()
        self.calendar_frame.populate_calendar_frame()

    def reverse_calendar(self):
        self.cont.rev_focus_month()   
        self.set_month_name_var()
        self.calendar_frame.populate_calendar_frame()

    def set_month_name_var(self):
        #this sets the month name variable to the currently focused month
        self.month_name_var.set(self.cont.month_year_str)

  
class CalendarFrame(ttk.Frame):
    """this class holds the building and populating of the calendar frame for the calendar page"""
    def __init__(self, parent, controller_):
        super().__init__(parent)
        
        self.log = logger.journal_logger()

        self.cont = controller_
        self._callback = controller_.calendar_button_clicked

    def populate_calendar_frame(self):
        """This function is called by the calendar page class to allow the controller easier access"""

        #to keep the calendar consistant the previous widgets have to be cleared
        for widget in self.winfo_children():
            widget.destroy()

        self.calendar_matrix = self.build_calendar_matrix()    

        #set row and column weight to keep size uniform
        for i in range(7):
            self.grid_columnconfigure(i,weight=1, uniform='calendar_column')
            self.grid_rowconfigure(i, weight=1, uniform='calendar_row')

        #build and grid the days of the week labels        
        days = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
        for i,day in enumerate(days):
            ttk.Label(self, text = day).grid(row=0, column=i)
        for r,week in enumerate(self.calendar_matrix, start=1):
            for c, button in enumerate(week):
                if button is not None:
                    button.grid(row=r, column=c, sticky='nsew')
        
    def build_calendar_matrix(self) -> list[list]:
        """Helper Method for conversion of model.Month.month_matrix into tkinter button grid"""
        
        calendar_matrix = []
        for week in self.cont.month_cal:
            new_week = []
            for day in week:
                if day:
                    day_ = day.date.day
                    button = ttk.Button(
                        self, 
                        text = day_, 
                        command=lambda d=day_: self._callback(d)
                        )
                    new_week.append(button)
                else:
                    new_week.append(None)
            calendar_matrix.append(new_week)
        
        return calendar_matrix
    

class RecentEntriesFrame(ttk.Frame):
    def __init__(self, parent, controller_) -> None:
        super().__init__(parent)
        self.log = logger.journal_logger()
        self.cont = controller_
        self.date1 = tk.StringVar()
        self.date2 = tk.StringVar()
        self.date3 = tk.StringVar()
        self.entry_snip1 = tk.StringVar()
        self.entry_snip2 = tk.StringVar()
        self.entry_snip3 = tk.StringVar()

        self.populate_recent_frame()

    def populate_recent_frame(self):
        frame_label = ttk.Label(self, text='Recent Entries')
        date_button1 = ttk.Button(self, textvariable=self.date1)
        date_button2 = ttk.Button(self, textvariable=self.date2)
        date_button3 = ttk.Button(self, textvariable=self.date3)

        entry_label1 = ttk.Label(self, textvariable=self.entry_snip1)
        entry_label2 = ttk.Label(self, textvariable=self.entry_snip2)
        entry_label3 = ttk.Label(self, textvariable=self.entry_snip3)

        frame_label.grid(column=0, row=0, columnspan=3)
        date_button1.grid(column=0, row=1, columnspan=1)
        date_button2.grid(column=0, row=2, columnspan=1)
        date_button3.grid(column=0, row=3, columnspan=1)

        entry_label1.grid(column=1, row=1, columnspan=2)
        entry_label2.grid(column=1, row=2, columnspan=2)
        entry_label3.grid(column=1, row=3, columnspan=2)
    
    def set_date_entry_text(self, data: list[tuple]):
        dates = [self.date1, self.date2, self.date3]
        entry_snips = [self.entry_snip1, self.entry_snip2, self.entry_snip3]
        index = 0
        for item in data:
            dates[index].set(item[0])
            entry_snips[index].set(item[1][:45])
            index += 1


class OptionsPage(ttk.Frame):
    """This is the third page. It will have the basic options that can be changed.
    It makes the change of style and font, as well as deleting one or all entries
    and downloading entries as a csv or txt"""
    def __init__(self,root, controller_):
         #initialize the frame inheritance
        super().__init__(root)
        #place the main page frame
        self.place(x = 0, y = 0, relwidth=1, relheight=1)
        