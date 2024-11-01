import datetime


class Entry:
    """Basic Entry class. Will hold the date and text for each entry"""
    def __init__(self, date: datetime, text: str = None):
        self.date = date
        self.text = text
