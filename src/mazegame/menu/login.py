import sqlite3

import pygame_menu

from mazegame.menu.menu_manager.menu_manager import MenuManager
from mazegame.menu.window_settings import WindowSettings

from mazegame.utils.databases.records_database import RecordsDatabase
from mazegame.utils.global_variables.global_variables import GlobalVariables

from mazegame.utils.paths.paths import base_dir

ASSETS_DIR = base_dir() / "assets"

class Login:
    """
    A class that defines the login screen for the game menu.

    This class displays the login screen, where the user can enter their nickname and password.
    It checks the given data against the database using the `authenticate()` method.
    If the authentication is successful, it performs actions using the `login_success()` method.
    """
    def __init__(self) -> None:
        self.login_screen()

    def login_screen(self, error_text="") -> None:
        """
        Displays the login screen.
        (main method of the class)

        :param error_text: Error message to display on the screen. Defaults to ""
        :return: None
        """
        menu = pygame_menu.Menu(height=WindowSettings.DISPLAY_HEIGHT,
                                width=WindowSettings.DISPLAY_WIDTH,
                                theme=WindowSettings.THEME,
                                title='Sign in')

        menu.add.label(error_text, font_size=15, font_color=(200, 0, 0))

        nick_field = menu.add.text_input('nick: ', maxchar=16)
        password_field = menu.add.text_input('Password: ', maxchar=32, password=True)

        menu.add.button('Continue', lambda: self.check_login(nick_field.get_value(), password_field.get_value()))
        menu.add.button('Back', lambda: MenuManager().go_to_previous_screen())

        menu.mainloop(WindowSettings.DISPLAY)

    def check_login(self, nick: str, password: str) -> None:
        """
        Checks if the entered data are correct.

        :param nick: The nick entered by the user
        :param password: The password entered by the user
        :return: None
        """
        if not nick:
            self.login_screen('Field "Nick" is required')
            return

        if not password:
            self.login_screen('Field "Password" is required')
            return

        if self.authenticate(nick, password):
            self.login_success(nick)
        else:
            self.login_screen("Incorrect nick or password")

    @staticmethod
    def authenticate(nick: str, password: str) -> bool:
        """
        Checks if the provided nickname and password match any records in the database.

        :param nick: The nick entered by the user
        :param password: The password entered by the user
        :return: True if the authentication is successful, False otherwise
        """
        query = 'SELECT * FROM accounts WHERE nick=? AND password=?'
        params = (nick, password)

        ac_database_path = ASSETS_DIR / "databases" / "accounts.db"
        with sqlite3.connect(ac_database_path) as conn:
            c = conn.cursor()
            c.execute(query, params)
            return c.fetchone() is not None

    @staticmethod
    def login_success(nick: str) -> None:
        """
        Performs actions when a user successfully logs in.

        :param nick: The nick entered by the user
        :return: None
        """
        GlobalVariables.nick = nick
        RecordsDatabase().check_and_adjust_columns_number()
        MenuManager().go_to_screen("menu_when_login")
