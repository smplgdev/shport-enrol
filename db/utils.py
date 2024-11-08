import logging
import os
import sqlite3

logger = logging.getLogger(__name__)


class DatabaseSession:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

        self._create_database_if_not_exists()

    def _create_database_if_not_exists(self):
        if os.path.exists(self.db_path):
            logger.debug("Database file already exists: %s", self.db_path)
            return

        # Create directories if they don't exist
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        # Create the file
        with open(self.db_path, 'w'):
            pass  # Simply open and close the file to create it

        logger.info("Created database file: %s", self.db_path)

    def connect(self):
        """Returns a context manager that provides the cursor."""
        return self

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        # If an exception occurred, handle the rollback
        if exc_type:
            self.conn.rollback()  # Rollback if an exception happened
        else:
            self.conn.commit()  # Commit if no exception occurred

        # Close the cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
