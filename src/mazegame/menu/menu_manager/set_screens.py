import logging

from mazegame.menu.help import Help
from mazegame.menu.initial_menu import InitialMenu
from mazegame.menu.login import Login
from mazegame.menu.menu_manager.menu_manager import MenuManager
from mazegame.menu.menu_when_login import MenuWhenLogin
from mazegame.menu.pause import Pause
from mazegame.menu.records import GlobalRecords, MainRecords, MyRecords
from mazegame.menu.register import Register
from mazegame.menu.show_result_board import ShowResultBoard

log = logging.getLogger(__name__)


class SetScreens:
    """
    A class that responsible for setting up the screens dictionary for the menu manager.
    """

    @staticmethod
    def set_screens() -> None:
        """
        Sets the screens dictionary for the menu manager.

        :param: None
        :return: None
        """
        log.info("Setting up screens for MenuManager")
        MenuManager.screens = {
            "initial_menu": InitialMenu,
            "login": Login,
            "register": Register,
            "menu_when_login": MenuWhenLogin,
            "main_records": MainRecords,
            "my_records": MyRecords,
            "global_records": GlobalRecords,
            "help": Help,
            "show_result_board": ShowResultBoard,
            "pause": Pause,
        }
        log.debug("Screens configured: %s", list(MenuManager.screens.keys()))
