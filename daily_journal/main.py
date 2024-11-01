"""Main module for daily journal app. Will initialize the controller,
passing it both the repository and the ui"""

import model
import controller
import repository
import logger 
import config

import tkinter as tk
from tkinter import ttk
import sqlite3


def db_connection(logger_:logger.logging.Logger) -> sqlite3.Connection|None:
    try:
        conn = sqlite3.connect(config.DB_NAME)
        logger_.info('Connection to DB established')
        return conn
    except Exception as e:
        logger_.exception('Exception while connecting to DB', e)
        return None
    

def main():
    """This function will initialize the logger, as well as the other modules. """
    geo = config.WINDOW_GEOMETRY # shortened the window geometry variable for a cleaner line later
    resize = config.WINDOW_RESIZEABLE
    # configure logger
    logger.configure_logger()

    #get the logger object to pass around
    log = logger.journal_logger()

    #initialize the tkinter window
    root = tk.Tk()
    root.geometry(f'{geo[0]}x{geo[1]}+{geo[2]}+{geo[3]}')
    root.resizable(resize[0],resize[1])
    root.title('Daily Journal')

    #initialize DB connection
    conn = db_connection(log)

    #initialize the repository
    app = controller.Controller(
        repository_ = repository.Entries(conn),
        root = root
    )

    #run the main loop for the UI
    root.mainloop()

    # close the DB connection
    conn.close()
    log.info('DB Connection Closed')


if __name__ == '__main__':
    main()