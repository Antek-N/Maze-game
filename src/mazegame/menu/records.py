import logging
import sqlite3

import pygame_menu

from mazegame.menu.menu_manager.menu_manager import MenuManager
from mazegame.menu.window_settings import WindowSettings
from mazegame.utils.global_variables.global_variables import GlobalVariables
from mazegame.utils.paths.paths import base_dir
from mazegame.utils.time.convert_time import convert_time

log = logging.getLogger(__name__)

ASSETS_DIR = base_dir() / "assets"


class MainRecords:
    """
    A class that defines the main record screen for the game menu.

    This class displays the main record screen with buttons leading to the `MyRecords` and `GlobalRecords` screens.
    """

    def __init__(self) -> None:
        log.info("Opening Main Records screen")
        self.main_records_screen()

    @staticmethod
    def main_records_screen() -> None:
        """
        Displays the main record screen (screen with buttons leading to the `MyRecords` and `GlobalRecords` screens).

        :param: None
        :return: None
        """
        log.debug("Initializing Main Records UI")
        menu = pygame_menu.Menu(
            height=WindowSettings.DISPLAY_HEIGHT,
            width=WindowSettings.DISPLAY_WIDTH,
            theme=WindowSettings.THEME,
            title="Records",
        )

        menu.add.button("My records", lambda: MenuManager().go_to_screen("my_records"))
        menu.add.button("Global records", lambda: MenuManager().go_to_screen("global_records"))
        menu.add.button("Back", lambda: MenuManager().go_to_screen("menu_when_login"))

        menu.mainloop(WindowSettings.DISPLAY)


class MyRecords:
    """
    A class that defines the screen with the user's records for the game menu.

    This class displays the screen with the user's records.
    The user's records are retrieved from the database and displayed as a formatted string.
    """

    def __init__(self) -> None:
        log.info("Opening My Records screen for '%s'", GlobalVariables.nick)
        self.my_records_screen()

    def my_records_screen(self) -> None:
        """
        Displays the screen with the user's records.
        (main method of the class)

        The user's records are retrieved from the database and displayed as a formatted string.

        :param: None
        :return: None
        """
        menu = pygame_menu.Menu(
            height=WindowSettings.DISPLAY_HEIGHT,
            width=WindowSettings.DISPLAY_WIDTH,
            theme=WindowSettings.THEME,
            title="My records",
        )

        database_times = self.get_database_times()
        record_string = self.create_record_string(database_times)
        menu.add.label(record_string, font_size=25, font_color=(40, 40, 40))

        menu.add.button("Back", lambda: MenuManager().go_to_previous_screen())

        menu.mainloop(WindowSettings.DISPLAY)

    @staticmethod
    def get_database_times() -> tuple | None:
        """
        Retrieves the user's record times from the database.

        :param: None
        :return: Tuple with record times
        """
        nick = GlobalVariables.nick
        level_numbers = GlobalVariables.number_of_levels

        # Create query
        select_query = "SELECT "
        select_query += ", ".join([f"level{i}" for i in range(1, level_numbers + 1)])
        select_query += " FROM records WHERE nick=?"

        # Get record times
        records_database_path = ASSETS_DIR / "databases" / "records.db"
        log.debug("Fetching records for '%s' from DB: %s", nick, records_database_path)
        with sqlite3.connect(records_database_path) as conn:
            cursor = conn.cursor()
            cursor.execute(select_query, (nick,))
            database_times = cursor.fetchone()

        if database_times is None:
            log.info("No records found for '%s'", nick)

        return database_times

    @staticmethod
    def create_record_string(database_times_list: tuple | list | None) -> str:
        """
        Creates a formatted string from the database record times.

        Creates a formatted string with the levels number and record times.
        If there is no record time for a level, 'None' is displayed instead.

        :param database_times_list: The record times as a list or tuple
        :return: The formatted record string
        """
        record_string = ""
        number_of_levels = GlobalVariables.number_of_levels

        # Handle the case where no records exist at all (database_times_list is None)
        if database_times_list is None:
            log.warning("database_times_list is None (no records found), creating empty string")
            for i in range(number_of_levels):
                record_string += f"Level{i + 1} - None\n"
            return record_string

        # Iterate over each level
        for i in range(number_of_levels):
            try:
                # Try to retrieve the record time for the current level
                record_string += f"Level{i+1} - {convert_time(database_times_list[i])}\n"
            except Exception as ex:
                # If an exception occurs, there is no record time for the level
                record_string += f"Level{i + 1} - None\n"
                log.warning("No data in the database - %s", ex)

        return record_string


class GlobalRecords:
    """
    A class that defines the screen with the global records for the game menu.

    This class displays the screen with the global records.
    The global records are retrieved from the database and displayed as a formatted string.
    """

    def __init__(self) -> None:
        log.info("Opening Global Records screen")
        self.global_records_screen()

    def global_records_screen(self) -> None:
        """
        Displays the screen with the global records.
        (main method of the class).

        The global records are retrieved from the database and displayed as a formatted string.

        :param: None
        :return: None
        """
        log.debug("Initializing Global Records UI")
        menu = pygame_menu.Menu(
            height=WindowSettings.DISPLAY_HEIGHT,
            width=WindowSettings.DISPLAY_WIDTH,
            theme=WindowSettings.THEME,
            title="Global records",
        )

        record_string = self.create_record_string()
        menu.add.label(record_string, font_size=25, font_color=(40, 40, 40))

        menu.add.button("Back", lambda: MenuManager().go_to_previous_screen())

        menu.mainloop(WindowSettings.DISPLAY)

    @staticmethod
    def create_record_string() -> str:
        """
        Creates a formatted string from the database record times.

        Retrieves the best record times and associated level numbers from the database and creates string from them.
        If there is no record time for a level, writes 'None' instead.

        :param: None
        :return: The formatted record string
        """
        number_of_levels = GlobalVariables.number_of_levels

        # Connect to the database
        records_database_path = ASSETS_DIR / "databases" / "records.db"
        log.debug("Building global best times from DB: %s", records_database_path)

        with sqlite3.connect(records_database_path) as conn:
            cursor = conn.cursor()
            best_times = []

            # Iterate over each level
            for level in range(1, number_of_levels + 1):
                # Construct the query to fetch the minimum time for the current level
                query = f"SELECT nick, level{level} FROM records WHERE level{level} = (SELECT MIN(level{level}) FROM records)"
                cursor.execute(query)
                # Fetch the time and nickname for the best record
                time_and_nick = cursor.fetchone()

                if time_and_nick:
                    nick, time = time_and_nick
                    # Add the best record for the current level to the list
                    best_times.append((level, time, nick))

        log.debug("Collected best times for %d levels, %d entries found", number_of_levels, len(best_times))

        # Create a formatted string representation of the best records
        record_string = "\n".join(
            [f"Level{level} - {convert_time(score)} - {nick}" for level, score, nick in best_times]
        )

        return record_string
