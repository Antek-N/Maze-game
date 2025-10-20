import pygame_menu
import logging

from mazegame.menu.window_settings import WindowSettings
from mazegame.menu.menu_manager.menu_manager import MenuManager

log = logging.getLogger(__name__)


class Help:
    """
    A class that defines the help screen for the game menu.

    This class displays the help menu with instructions on how to play the game. It uses the
    `pygame_menu` library to create a menu with a help message and a "Back" button.
    """
    def __init__(self) -> None:
        log.info("Opening Help screen")
        self.help()

    @staticmethod
    def help() -> None:
        """
        Displays the help menu with instructions on how to play the game.

        :param: None
        :return: None
        """
        log.debug("Initializing Help menu UI")
        help_message = """
        1. To control use arrows or WASD
        2. To pause game, click ESC button
        """
        menu = pygame_menu.Menu(height=WindowSettings.DISPLAY_HEIGHT,
                                width=WindowSettings.DISPLAY_WIDTH,
                                theme=WindowSettings.THEME,
                                title='Help')

        menu.add.label(help_message, font_size=25)
        menu.add.button('Back', lambda: MenuManager().go_to_previous_screen())

        menu.mainloop(WindowSettings.DISPLAY)
