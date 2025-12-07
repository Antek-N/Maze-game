import logging

import pygame_menu

from mazegame.menu.menu_manager.menu_manager import MenuManager
from mazegame.menu.window_settings import WindowSettings
from mazegame.utils.gameplay.start_game import Game

log = logging.getLogger(__name__)


class MenuWhenLogin:
    """
    A class that defines the menu shown after the user is logged in (menu_when_login).

    This class displays the menu_when_login with buttons to play the game, view records,
    get help, log out, and quit the game.
    """

    def __init__(self) -> None:
        log.info("Opening menu for logged-in user")
        self.menu_when_login()

    @staticmethod
    def menu_when_login() -> None:
        """
        Displays the menu_when_login (menu shown after the user is logged in).

        :param: None
        :return: None
        """
        menu = pygame_menu.Menu(
            height=WindowSettings.DISPLAY_HEIGHT,
            width=WindowSettings.DISPLAY_WIDTH,
            theme=WindowSettings.THEME,
            title="Welcome to DotMaze project!",
        )

        menu.add.button("Play", lambda: Game().on_execute())
        menu.add.button("Records", lambda: MenuManager().go_to_screen("main_records"))
        menu.add.button("Help", lambda: MenuManager().go_to_screen("help"))
        menu.add.button("Log out", lambda: MenuManager().go_to_screen("initial_menu"))
        menu.add.button("Quit", pygame_menu.events.EXIT)

        menu.mainloop(WindowSettings.DISPLAY)
