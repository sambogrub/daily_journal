"""Main module for daily journal app. Will initialize the controller,
passing it both the repository and the ui"""

import sqlite3
import tkinter as tk

import config
import controller
import logger
import repository
from ui import StyleManager


def db_connection(logger_: logger.logging.Logger) -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(config.DB_NAME)
        logger_.info('Connection to DB established')
    except sqlite3.Error:
        logger_.exception('Exception while connecting to DB')
        raise
    return conn


def main():
    """This function will initialize the logger, as well as the other modules. """

    logger.configure_logger()
    logger_ = logger.journal_logger()

    # initialize the tkinter window TODO: because ...
    root = tk.Tk()
    root.geometry(config.WINDOW_GEOMETRY)
    root.resizable(*config.WINDOW_RESIZEABLE)
    root.title('Daily Journal') # TODO: Window geometry is in config. Why not title?

    # initialize style manager directly to root TODO: because ...
    style_manager = StyleManager(root)

    # TODO: add modal dialog informing end-user about DB error?
    conn = db_connection(logger_)

    try:
        # initialize the repository TODO: because ...
        app = controller.Controller(
            repository_ = repository.Entries(conn),
            root = root
        )

        # run the main loop for the UI TODO: because ...
        root.mainloop()
    finally:
        conn.close()
        logger_.info('DB Connection Closed')


if __name__ == '__main__':
    main()
