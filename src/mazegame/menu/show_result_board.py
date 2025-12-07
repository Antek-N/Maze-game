import logging
import sqlite3

import pygame_menu

from mazegame.menu.menu_manager.menu_manager import MenuManager
from mazegame.menu.window_settings import WindowSettings
from mazegame.utils.global_variables.global_variables import GlobalVariables
from mazegame.utils.paths.paths import base_dir
from mazegame.utils.save_records.save_records import SaveRecords
from mazegame.utils.time.convert_time import convert_time

log = logging.getLogger(__name__)

ASSETS_DIR = base_dir() / "assets"


class ShowResultBoard:
    """
    A class that defines the result board screen for the game menu.

    This class displays the result board screen, which shows the player's results from the current gameplay.
    """

    def __init__(self) -> None:
        log.info("Opening Result Board screen")
        self.result_board()

    def result_board(self) -> None:
        """
        Displays the result_board screen (a screen displayed at the end of the game, containing the player's results
        from the current gameplay)
        (main method of the class)

        :param: None
        :return: None
        """
        log.debug("Initializing Result Board UI")
        menu = pygame_menu.Menu(
            height=WindowSettings.DISPLAY_HEIGHT,
            width=WindowSettings.DISPLAY_WIDTH,
            theme=WindowSettings.THEME,
            title="Result board",
        )

        result_string = self.create_result_string()

        # Add a label to display the result string or a message if there are no results
        if result_string:
            menu.add.label(result_string, font_size=25, font_color=(40, 40, 40))
        else:
            log.info("No results to display on Result Board")
            menu.add.label("You have no results\n", font_size=25, font_color=(255, 0, 0))

        menu.add.button("Continue", lambda: MenuManager().go_to_screen("menu_when_login"))

        # Save the records to the database
        log.debug("Saving records to database")
        SaveRecords().save_records()

        # Reset the times list in the global variables
        log.debug("Resetting GlobalVariables.times_list")
        GlobalVariables.times_list = []

        menu.mainloop(WindowSettings.DISPLAY)

    @staticmethod
    def get_current_times() -> tuple:
        """
        Retrieves the current times from the database.

        :param: None
        :return: Current times from the database.
        """
        records_database_path = ASSETS_DIR / "databases" / "records.db"
        log.debug("Fetching current times for '%s' from DB: %s", GlobalVariables.nick, records_database_path)
        with sqlite3.connect(records_database_path) as conn:
            cursor = conn.cursor()

            nick = GlobalVariables.nick
            level_numbers = GlobalVariables.number_of_levels

            # Create query
            query = "SELECT "
            query += ", ".join([f"level{i}" for i in range(1, level_numbers + 1)])
            query += " FROM records WHERE nick=?"

            # Get current times
            cursor.execute(query, (nick,))
            current_times = cursor.fetchone()

            if current_times is None:
                log.warning("No current times found for user '%s'", nick)

            return current_times

    def create_result_string(self) -> str:
        """
        Creates a formatted result string, containing recorded times.

        :param: None
        :return: The formatted result string
        """
        times_list = GlobalVariables.times_list
        database_times_list = self.get_current_times()

        result_string = ""
        # Iterate over the times list and compare with the current times from the database
        for i, element in enumerate(times_list, start=1):
            if database_times_list[i - 1] is None or element < database_times_list[i - 1]:
                # If the time is a new record, mark it as such
                log.info("New record achieved on level %d: %s", i, convert_time(element))
                result_string += f"Level{i} - {convert_time(element)}    NEW RECORD\n"
            else:
                result_string += f"Level{i} - {convert_time(element)}\n"

        log.debug("Result string created successfully")
        return result_string
