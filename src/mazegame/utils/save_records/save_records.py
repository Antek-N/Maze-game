import sqlite3
import logging

from mazegame.utils.global_variables.global_variables import GlobalVariables
from mazegame.utils.paths.paths import base_dir

ASSETS_DIR = base_dir() / "assets"

log = logging.getLogger(__name__)


class SaveRecords:
    """
    The SaveRecords class is responsible for saving game records to the database.

    The SaveRecords class establishes a connection to the SQLite database and provides methods to save
    the game records. It retrieves the times list (times of the current game) and the database times
    (times from the records-database), creates a new record list by comparing the database times with
    the times list, and updates the database with the created new record list.
    """
    def __init__(self) -> None:
        # Establish a connection to the SQLite database
        records_database_path = ASSETS_DIR / "databases" / "records.db"
        self.conn = sqlite3.connect(records_database_path)
        self.cursor = self.conn.cursor()
        log.debug("Connected to records database at %s", records_database_path)

    def save_records(self) -> None:
        """
        Save the records to the database.
        (main method of the class)

        Retrieves the times list (times of the current game) and the database times (times from the records-database),
        creates a new record list by comparing the database times with the times list,
        and updates the database with the new record list.

        :param: None
        :return: None
        """
        log.info("Saving player records to database")
        # Retrieve the times_list(times of the current game) and the database_times (times from records database)
        times_list = GlobalVariables.times_list
        database_times = self.get_database_times()
        log.debug("Loaded %d times from database and %d from session", len(database_times), len(times_list))

        # Create a new record list by comparing the database_times with the times_list
        new_times_list = self.create_new_record_list(times_list, database_times)
        log.debug("Created new record list: %s", new_times_list)

        # Update the database with the new record list
        self.update_database(new_times_list)
        log.info("Database updated successfully for player '%s'", GlobalVariables.nick)

        # Close the database connection
        self.conn.close()
        log.debug("Database connection closed")

    def get_database_times(self) -> tuple:
        """
        Retrieves the database times for a given nick.

        Constructs an SQL query to select the times from the database for a given nick,
        executes the query, and fetches the result.

        :param: None
        :return: The tuple containing times from the database.
        """
        log.debug("Fetching database times for player '%s'", GlobalVariables.nick)
        # Retrieve necessary variables
        nick = GlobalVariables.nick
        level_numbers = GlobalVariables.number_of_levels

        # Construct the SQL query to select the times from the database for a given nick
        select_query = "SELECT "
        select_query += ", ".join([f"level{i}" for i in range(1, level_numbers + 1)])
        select_query += " FROM records WHERE nick=?"

        # Execute the SQL query and fetch the result
        self.cursor.execute(select_query, (nick,))
        database_times = self.cursor.fetchone()
        log.debug("Database times retrieved: %s", database_times)

        return database_times

    @staticmethod
    def create_new_record_list(times_list: list, database_times: tuple) -> list:
        """
        Creates a new record list by comparing the database times with the times list.

        Compares each pair of times in the database_times and the times_list. If the database time exists, it
        appends the minimum of the database time and the time from the times list (just the best time).
        If the database time is None, it appends the time from the times list.
        It also appends any remaining records from the database times that are not present in the times list.

        Example:
            create_new_record_list([10.0, 20.0, 30.0], [None, 15.0, 25.0, 35.0]) => [10.0, 15.0, 25.0, 35.0]

        :param times_list: The times list (times of the current game)
        :param database_times: The database times tuple (times from the database)

        :return: The new record list (combined database_times and times_list)
        """
        log.debug("Creating new record list from times_list=%s and database_times=%s", times_list, database_times)
        record_list = []

        # Compare each pair of times in the database_times and the times_list
        for db_time, time in zip(database_times, times_list):
            if db_time is not None:
                # If the database time exists, append the minimum of the db_time and the time
                record_list.append(min(db_time, time))
            else:
                # If the database time is None, append the time from the times list
                record_list.append(time)

        # Append any remaining records from the database times that are not present in the times list
        remaining_records = database_times[len(times_list):]
        record_list.extend(remaining_records)

        log.debug("New record list created: %s", record_list)
        return record_list

    def update_database(self, new_times_list: list) -> None:
        """
        Updates the records in the database for a given nick with the new times list
        (inserts the data from new_times_list into the database).

        Constructs an SQL query and values to update the records in the database for a given nick,
        and executes the SQL query.

        :param new_times_list: The new times list (combined database_times and times_list)
        :return: None
        """
        log.debug("Updating database for player '%s' with values: %s", GlobalVariables.nick, new_times_list)
        # Retrieve necessary variables
        nick = GlobalVariables.nick
        level_numbers = GlobalVariables.number_of_levels

        # Create the placeholders for the SQL query
        placeholders = [f"level{i + 1} = ?" for i in range(level_numbers)]
        placeholders_str = ", ".join(placeholders)

        # Construct the SQL query and values to update the records in the database for a given nick
        query = f"UPDATE records SET {placeholders_str} WHERE nick = ?"
        values = new_times_list + [nick]

        # Execute SQL query
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            log.info("Records updated successfully for '%s'", nick)
        except Exception as ex:
            log.warning("Failed to update records for '%s': %s", nick, ex)
