from scripts.menu.menu_manager.menu_manager import MenuManager
from scripts.menu.initial_menu import InitialMenu
from scripts.menu.login import Login
from scripts.menu.register import Register
from scripts.menu.menu_when_login import MenuWhenLogin
from scripts.menu.records import MainRecords, MyRecords, GlobalRecords
from scripts.menu.help import Help
from scripts.menu.show_result_board import ShowResultBoard
from scripts.menu.pause import Pause


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
