import logging
import sqlite3

from mazegame.utils.global_variables.global_variables import GlobalVariables
from mazegame.utils.paths.paths import base_dir

log = logging.getLogger(__name__)

ASSETS_DIR = base_dir() / "assets"


class RecordsDatabase:
    """
    A class that manages the records table in the records-database.

    This class provides methods to check and adjust the number of columns in the records table.
    If the actual number of columns is less than the expected number of levels, missing columns are created.
    If the actual number of columns is greater than the expected number of levels, excess columns are removed.
    """

    def __init__(self) -> None:
        records_database_path = ASSETS_DIR / "databases" / "records.db"
        log.debug("Connecting to records database: %s", records_database_path)
        self.conn = sqlite3.connect(records_database_path)
        self.cursor = self.conn.cursor()
        self.number_of_levels = GlobalVariables.number_of_levels
        log.info("RecordsDatabase initialized (expected levels: %d)", self.number_of_levels)

    def check_and_adjust_columns_number(self) -> None:
        """
        Checks the number of columns in the records table and adjusts accordingly.
        (main method of the class)

        If the actual number of columns is less than the expected number of levels, missing columns are created.
        If the actual number of columns is greater than the expected number of levels, excess columns are removed.
        (excepted number of levels is a number of declared levels in the maze_creator.levels.py file).

        :param: None
        :return: None
        """
        log.debug("Checking and adjusting number of level columns in records table")
        # Check the number of level columns in the records table
        actual_num_levels = len(self.get_existing_columns_names()[1:])  # [1:] because the first column is a "nick"
        log.debug("Found %d level columns (expected %d)", actual_num_levels, self.number_of_levels)

        # Compare with the expected number of columns
        if actual_num_levels < self.number_of_levels:
            log.info("Creating %d missing columns", self.number_of_levels - actual_num_levels)
            self.create_missing_columns()
        elif actual_num_levels > self.number_of_levels:
            log.info("Removing %d excess columns", actual_num_levels - self.number_of_levels)
            self.remove_excess_columns()
        else:
            log.debug("Column count is correct (%d levels)", actual_num_levels)

    def get_existing_columns_names(self) -> list:
        """
        Retrieves a list of existing columns names in the records table.

        :param: None
        :return: A list of the column names existing in the records table
        """
        # Retrieve information about columns from the table
        query = f"PRAGMA table_info({'records'})"
        self.cursor.execute(query)
        columns = [column[1] for column in self.cursor.fetchall()]
        log.debug("Existing columns: %s", columns)
        return columns

    def create_missing_columns(self) -> None:
        """
        Creates missing columns in the records table.
        """
        # Get existing columns
        existing_columns = self.get_existing_columns_names()

        # Create list of names of missing columns
        missing_columns = []
        for i in range(1, self.number_of_levels + 1):
            column_name = "level" + str(i)
            if column_name not in existing_columns:
                missing_columns.append(column_name)

        log.debug("Missing columns to add: %s", missing_columns)

        # Add missing columns
        for column in missing_columns:
            self.add_column(column)

    def add_column(self, column_to_add_name: str) -> None:
        """
        Adds a new column to the records table.
        """
        try:
            # Add a new column to the table
            log.debug("Adding column '%s' to records table", column_to_add_name)
            query = f"ALTER TABLE {'records'} ADD COLUMN {column_to_add_name}"
            self.cursor.execute(query)
            self.conn.commit()
            log.info("Column '%s' added successfully", column_to_add_name)
        except Exception as ex:
            log.warning("Failed to add column '%s': %s", column_to_add_name, ex)

    def remove_excess_columns(self) -> None:
        """
        Removes excess columns from the records table.
        """
        # Get existing columns
        existing_columns = self.get_existing_columns_names()[1:]  # [1:] because the first column is a "nick"

        # Create list of excess columns
        excess_columns = []
        for column in existing_columns:
            if int(column[len("level") :]) > self.number_of_levels:
                excess_columns.append(column)

        log.debug("Excess columns to remove: %s", excess_columns)

        # Remove excess columns
        for column in excess_columns:
            self.remove_column(column)

    def remove_column(self, excess_column_name: str) -> None:
        """
        Removes a column from the records table.
        """
        try:
            log.debug("Removing column '%s' from records table", excess_column_name)
            # Get existing columns
            existing_columns = self.get_existing_columns_names()

            # Create a list of columns, excluding the column to be removed
            new_columns = [column for column in existing_columns if column != excess_column_name]

            # Create a new table without the removed column
            new_table_name = f"new_{'records'}"
            query = f"CREATE TABLE {new_table_name} ({', '.join(new_columns)})"
            self.cursor.execute(query)

            # Copy data from the existing table to the new table
            query = f"INSERT INTO new_{'records'} SELECT {', '.join(new_columns)} FROM {'records'}"
            self.cursor.execute(query)

            # Drop the original table
            query = f"DROP TABLE {'records'}"
            self.cursor.execute(query)

            # Rename the new table to the original name
            query = f"ALTER TABLE new_{'records'} RENAME TO {'records'}"
            self.cursor.execute(query)

            log.info("Column '%s' removed successfully", excess_column_name)

        except Exception as ex:
            log.warning("Failed to remove column '%s': %s", excess_column_name, ex)

        self.conn.commit()
