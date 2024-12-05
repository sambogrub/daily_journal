"""Main module for daily journal app. Will initialize the controller,
passing it both the repository and the ui"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

import controller
import repository
import logger 
import config
from ui import StyleManager

def db_connection(logger_: logger.logging.Logger) -> sqlite3.Connection:
    """initialize the db connection at the beginning so that it can be passed around as needed,
    rather than opening and closing multiple times throughout the app"""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        logger_.info('Connection to DB established')

    except sqlite3.Error:
        logger_.exception('Error while connecting to DB')
        #let the end user know that there was an error with the connection
        db_connection_error('An error occurred while connecting to the database. \nThe app needs to restart.') 
        #still pass the error along so that the app stops properly
        raise

    return conn 

def db_connection_error(message: str):
    """This function shows a popup error window if the database connection has an issue"""
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('Application error ', message)
    root.destroy()
    
def main():
    """This function will initialize the logger, as well as the other modules. """ 
    #this sets up the logger at the very beginning of the app so when a logger instance is called its
    #the same logger every time
    logger.configure_logger()
    log = logger.journal_logger()

    #initialize DB connection here to catch any errors with connecting to the database,
    #stopping the rest of the app initialization 
    conn = db_connection(log)

    #initialize the tkinter window in main so the root window is 
    # passed to all needed modules through controller
    root = tk.Tk()
    root.geometry(config.WINDOW_GEOMETRY)
    root.resizable(*config.WINDOW_RESIZEABLE)
    root.title('Daily Journal')

    #Initialize the stylemanager here to have it attach to the root window at the beginning
    _style_manager = StyleManager(root)

    try:
        app = controller.Controller(
            repository_ = repository.Entries(conn),
            root = root
        )
        #run the main loop for the UI after the the business logic is initialized
        root.mainloop()
    finally:
        # the connection close is done here to ensure that the connection is closed properly when the app closes
        conn.close()
        log.info('DB Connection Closed')


if __name__ == '__main__':
    main()
    