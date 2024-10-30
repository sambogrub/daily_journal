import datetime
import daily_journal.model as model
class Controller:
    '''Controller for Daily Journal. Will be responsible for interactions with the repository,
    passing entry objects between ui and the repository'''
    def __init__(self, repository, ui):
        self.repository = repository
        self.ui = ui

    def app_start(self):
        # this function will call all needed functions to start the app. 
        # It will call to initialize a new entry for the current day,
        # and it will call to start the UI.
        pass

    def init_new_entry(self, date: datetime, text: str = None) -> object: #returns a new entry object
        # this function will create a new entry with the given date. 
        pass

    def assign_db_text_to_entry(self, entry) -> object: # returns the same entry object with a possible entry text
        # this function will get the text from the repository for the entry's date, if any exists
        pass

    def assign_ui_text_to_entry(self, entry, text) -> object:
        #this function will assign the given text from the ui textbox to the 



