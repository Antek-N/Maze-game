import pygame

from scripts.menu.window_settings import WindowSettings
from scripts.menu.menu_manager.menu_manager import MenuManager
from scripts.menu.menu_manager.set_screens import SetScreens

from scripts.utils.global_variables.global_variables import GlobalVariables


class App:
    """
    Main class of the application
    """
    def __init__(self) -> None:
        self.initialize_game()

    @staticmethod
    def initialize_game() -> None:
        """
        Initializes the game.

        Initializes the window settings, sets up screens for the menu manager,
        initializes global variables, and launches the initial menu screen.

        :param: None
        :return: None
        """
        # Initialize window settings
        WindowSettings().initialize_settings()

        # Initialize screens for menu manager
        SetScreens.set_screens()

        # Initialize global variables
        GlobalVariables()

        # Launch the initial menu screen
        MenuManager().go_to_screen("initial_menu")


# PROGRAM START
if __name__ == "__main__":
    pygame.init()
    App()
