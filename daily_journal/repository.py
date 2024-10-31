'''Module will hold the entries repository, as well as the table initialization function'''

import sqlite3
import logger

from config import ENTRIES_TABLE

def init_entries_table(conn: sqlite3.Connection, logger: logger):
    '''This initializes the entries table'''
    entries_query = f'''
    CREATE TABLE IF NOT EXISTS {ENTRIES_TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE UNIQUE,
    entry TEXT
    )'''

    # create the table, logging any basic error
    try:
        cursor = conn.cursor()
        cursor.execute(entries_query)
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()
        logger.exception('SQLite error: %s', e)
    except Exception as e:
        conn.rollback()
        logger.exception('SQLite error: %s', e)
        raise
    finally:
        cursor.close()

class Entries:
    def __init__(self, db_conn):
        self.conn = db_conn
        self.logger = logger.journal_logger()
        init_entries_table(self.conn, self.logger)
        
