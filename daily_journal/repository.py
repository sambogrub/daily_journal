"""Module will hold the entries repository, as well as the table initialization function"""

import sqlite3
from contextlib import contextmanager

import logger
import model


def init_entries_table(conn: sqlite3.Connection, logger_: logger.logging.Logger) -> None:
    """This initializes the entries table"""
    entries_query = f'''
    CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE UNIQUE,
    entry TEXT
    )'''

    index_query = '''CREATE UNIQUE INDEX IF NOT EXISTS idx_entries_date ON entries(date)'''

    # create the table, logging any basic error
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(entries_query)
        cursor.execute(index_query)
        conn.commit()
    except sqlite3.Error:
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

    @staticmethod
    def format_date(day: model.Day):
        return day.date.isoformat()

    def save(self, day: model.Day) -> None:
        """ Method performs upsert (update or insert) of given day into the entries table """
        query = '''
            INSERT INTO entries (date, entry) VALUES (?, ?)
            ON CONFLICT(date)
            DO UPDATE SET entry = EXCLUDED.entry
         '''
        formatted_date = self.format_date(day)
        with self.cursor_manager() as cursor:
            cursor.execute(query, (formatted_date, day.entry))
            self.logger.info(f'Entry saved for date {formatted_date}')

    def get_by_month(self, month: model.Month) -> list[model.Day]:
        """ Method fetches all entries for given month converted to Day objects """
        query = '''
                SELECT date, entry
                FROM entries
                WHERE STRFTIME('%Y-%m', date) = ?
                '''
        month_str = f'{month.year}-{month.month_num:02}'
        with self.cursor_manager() as cursor:
            cursor.execute(query, (month_str,))
            days = [model.str_to_day(*entry) for entry in cursor.fetchall()]
        self.logger.info('Entries retrieved for month: %s', month_str)
        return days

    def delete(self, day: model.Day) -> None:
        query = '''
            DELETE FROM entries
            WHERE date = ?
            '''
        formatted_date = self.format_date(day)

        with self.cursor_manager() as cursor:
            cursor.execute(query, (formatted_date, ))
            self.logger.info(f'Entry deleted for date: {formatted_date}')
        
