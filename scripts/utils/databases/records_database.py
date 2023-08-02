import logging
import sqlite3

from scripts.utils.global_variables.global_variables import GlobalVariables


class RecordsDatabase:
    """
    A class that manages the records table in the records-database.

    This class provides methods to check and adjust the number of columns in the records table.
    If the actual number of columns is less than the expected number of levels, missing columns are created.
    If the actual number of columns is greater than the expected number of levels, excess columns are removed.
    """
    def __init__(self) -> None:
        self.conn = sqlite3.connect('databases/records.db')
        self.cursor = self.conn.cursor()
        self.number_of_levels = GlobalVariables.number_of_levels

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
        # Check the number of level columns in the records table
        actual_num_levels = len(self.get_existing_columns_names()[1:])  # [1:] because the first column is a "nick"

        # Compare with the expected number of columns
        if actual_num_levels < self.number_of_levels:
            self.create_missing_columns()
        elif actual_num_levels > self.number_of_levels:
            self.remove_excess_columns()

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
        return columns

    def create_missing_columns(self) -> None:
        """
        Creates missing columns in the records table.

        Checks for missing level columns and adds them to the table.

        :param: None
        :return: None
        """
        # Get existing columns
        existing_columns = self.get_existing_columns_names()

        # Create list of names of missing columns
        missing_columns = []
        for i in range(1, self.number_of_levels + 1):
            column_name = 'level' + str(i)
            if column_name not in existing_columns:
                missing_columns.append(column_name)

        # Add missing columns
        for column in missing_columns:
            self.add_column(column)

    def add_column(self, column_to_add_name: str) -> None:
        """
        Adds a new column to the records table.

        :param column_to_add_name: The name of the column to be added
        :return: None
        """
        try:
            # Add a new column to the table
            query = f"ALTER TABLE {'records'} ADD COLUMN {column_to_add_name}"
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as ex:
            logging.warning(ex)

    def remove_excess_columns(self) -> None:
        """
        Removes excess columns from the records table.

        Checks for excess columns and removes them from the table.

        :param: None
        :return: None
        """
        # Get existing columns
        existing_columns = self.get_existing_columns_names()[1:]  # [1:] because the first column is a "nick"

        # Create list of excess columns
        excess_columns = []
        for column in existing_columns:
            if int(column[len('level'):]) > self.number_of_levels:
                excess_columns.append(column)

        # Remove excess columns
        for column in excess_columns:
            self.remove_column(column)

    def remove_column(self, excess_column_name: str) -> None:
        """
        Removes a column from the records table.

        Creates a new tabel without excess_column_name -> deletes the old table -> renames the new table to the old name

        :param excess_column_name: The name of the column to be removed
        :return: None
        """
        try:
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

        except Exception as ex:
            logging.warning(ex)

        self.conn.commit()
