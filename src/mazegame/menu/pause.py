import pygame_menu
import logging

from mazegame.menu.window_settings import WindowSettings
from mazegame.menu.menu_manager.menu_manager import MenuManager

from mazegame.utils.global_variables.global_variables import GlobalVariables
from mazegame.utils.gameplay.start_game import Game

log = logging.getLogger(__name__)


class Pause:
    """
    A class that defines the pause menu.

    This class displays the pause menu when the player clicks the 'ESC' key during the game to pause it.
    The pause menu offers options to play again or go back to the main menu.
    """
    def __init__(self) -> None:
        log.info("Opening Pause menu")
        self.pause()

    def pause(self) -> None:
        """
        Displays the pause menu.
        (main method of the class)

        :param: None
        :return: None
        """
        log.debug("Initializing Pause menu UI")
        menu = pygame_menu.Menu(height=WindowSettings.DISPLAY_HEIGHT,
                                width=WindowSettings.DISPLAY_WIDTH,
                                theme=WindowSettings.THEME,
                                title='Pause')

        menu.add.button('Play again', lambda: self.play_again())
        menu.add.button('Back to menu', lambda: self.show_results())

        menu.mainloop(WindowSettings.DISPLAY)

    @staticmethod
    def show_results() -> None:
        """
        Goes to the show_result_board screen.

        :param: None
        :return: None
        """
        log.info("Returning to main menu from Pause screen")
        GlobalVariables.current_level_number = 0
        GlobalVariables.clock_instance.reset_and_stop_clock()
        MenuManager().go_to_screen("show_result_board")

    @staticmethod
    def play_again() -> None:
        """
        Restarts the game from the current level.

        :param: None
        :return: None
        """
        log.info("Restarting game from current level")
        GlobalVariables.current_level_number -= 1
        GlobalVariables.clock_instance.reset_and_stop_clock()
        Game().on_execute()
