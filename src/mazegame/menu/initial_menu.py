import pygame_menu

from mazegame.menu.window_settings import WindowSettings
from mazegame.menu.menu_manager.menu_manager import MenuManager


class InitialMenu:
    """
    A class that defines the initial screen for the game menu.

    This class displays the initial menu with options to sign in, sign up, or quit the game.
    It uses the `pygame_menu` library to create a menu with buttons for these options.
    """
    def __init__(self) -> None:
        self.initial_menu()

    @staticmethod
    def initial_menu() -> None:
        """
        Displays the initial menu of the DotMaze project.

        :param: None
        :return: None
        """
        menu = pygame_menu.Menu(height=WindowSettings.DISPLAY_HEIGHT,
                                width=WindowSettings.DISPLAY_WIDTH,
                                theme=WindowSettings.THEME,
                                title='Welcome to DotMaze project!')

        menu.add.button('Sign in', lambda: MenuManager().go_to_screen("login"))
        menu.add.button('Sign up', lambda: MenuManager().go_to_screen("register"))
        menu.add.button('Quit', pygame_menu.events.EXIT)

        menu.mainloop(WindowSettings.DISPLAY)
