from mazegame.menu.menu_manager.menu_manager import MenuManager
from mazegame.menu.initial_menu import InitialMenu
from mazegame.menu.login import Login
from mazegame.menu.register import Register
from mazegame.menu.menu_when_login import MenuWhenLogin
from mazegame.menu.records import MainRecords, MyRecords, GlobalRecords
from mazegame.menu.help import Help
from mazegame.menu.show_result_board import ShowResultBoard
from mazegame.menu.pause import Pause


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
        MenuManager.screens = {'initial_menu': InitialMenu,
                               'login': Login,
                               'register': Register,
                               'menu_when_login': MenuWhenLogin,
                               'main_records': MainRecords,
                               'my_records': MyRecords,
                               'global_records': GlobalRecords,
                               'help': Help,
                               'show_result_board': ShowResultBoard,
                               'pause': Pause
                               }
