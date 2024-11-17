"""Module will hold the entries repository, as well as the table initialization function"""

import sqlite3
import logger
import datetime
from contextlib import contextmanager

from config import ENTRIES_TABLE


def init_entries_table(conn: sqlite3.Connection, logger_: logger.logging.Logger) -> None:
    """This initializes the entries table"""
    entries_query = f'''
    CREATE TABLE IF NOT EXISTS {ENTRIES_TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE UNIQUE,
    entry TEXT
    )'''

    # create the table, logging any basic error
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(entries_query)
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        logger_.exception('SQLite error:')
    except Exception:
        conn.rollback()
        logger_.exception('SQLite error:')
        raise
    finally:
        if cursor is not None:
            cursor.close()


class Entries:
    """This is the entries repository, responsible for interactions with the database"""
    def __init__(self, db_conn):
        self.conn = db_conn

        #get the logger
        self.logger = logger.journal_logger()
        
        #initialize the tables
        init_entries_table(self.conn, self.logger)

    @contextmanager
    def cursor_manager(self):
        #basic context manager for connections with the database
        cursor = self.conn.cursor()
        try:
            yield cursor
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.conn.rollback()
            self.logger.exception('SQLite error:')
        except Exception:
            self.conn.rollback()
            self.logger.exception('Error at:')
            raise
        finally:
            cursor.close()

    def store_entry(self, date: datetime.date, text: str):
        #stores a new entry
        query = f'''
            INSERT INTO {ENTRIES_TABLE} (date, entry)
            VALUES (?, ?)
        '''
        formatted_date = date.isoformat() #make sure the date is formatted to iso; 'yyyy-mm-dd'

        with self.cursor_manager() as cursor:
            cursor.execute(query, (formatted_date, text))

    def get_entries(self, start_date: datetime.date, end_date: datetime.date) -> str:
        #retreives a specific entry with a given date
        query = f'''
            SELECT date, entry
            FROM {ENTRIES_TABLE}
            WHERE date BETWEEN ? and ?
            '''
        f_start_date = start_date.isoformat() #make sure the date is formatted to iso: 'yyyy-mm-dd'
        f_end_date = end_date.isoformat()

        with self.cursor_manager() as cursor:
            cursor.execute(query, (f_start_date, f_end_date))
            entries = cursor.fetchall()
            return entries
        
        
        
