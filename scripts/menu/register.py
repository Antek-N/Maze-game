import sqlite3

import pygame_menu

from scripts.menu.window_settings import WindowSettings
from scripts.menu.menu_manager.menu_manager import MenuManager

from scripts.utils.databases.records_database import RecordsDatabase
from scripts.utils.global_variables.global_variables import GlobalVariables


class Register:
    """
    A class that defines the registration screen for the game menu.

    This class displays the registration screen and handles the user registration process.
    """
    def __init__(self) -> None:
        self.register_screen()

    def register_screen(self, error_text="") -> None:
        """
        Displays the registration screen.
        (main method of the class)

        :param error_text: Error message to display on the screen. Defaults to ""
        :return: None
        """
        menu = pygame_menu.Menu(height=WindowSettings.DISPLAY_HEIGHT,
                                width=WindowSettings.DISPLAY_WIDTH,
                                theme=WindowSettings.THEME,
                                title='Sign up')

        menu.add.label(error_text, font_size=15, font_color=(200, 0, 0))

        nick_field = menu.add.text_input('nick: ', maxchar=16)
        password_field = menu.add.text_input('Password: ', maxchar=32, password=True)
        repeat_password_field = menu.add.text_input('Repeat password: ', maxchar=32, password=True)

        menu.add.button('Continue', lambda: self.apply_register(nick_field.get_value(), password_field.get_value(),
                                                                repeat_password_field.get_value()))
        menu.add.button('Back', lambda: MenuManager().go_to_previous_screen())

        menu.mainloop(WindowSettings.DISPLAY)

    def apply_register(self, nick: str, password: str, repeated_password: str) -> None:
        """
        Applies the registration process.
        
        :param nick: The nick entered by the user
        :param password: The password entered by the user
        :param repeated_password: The repeated password entered by the user
        :return: None
        """
        # Validate the user input data before registration
        if not self.validate_data(nick, password, repeated_password):
            return

        # Insert the account into the accounts database
        self.insert_account_to_database(nick, password)

        # Insert a default record for the user into the records database
        self.insert_default_record_to_database(nick)

        # Go back to the initial menu screen
        MenuManager().go_to_screen("initial_menu")

    def validate_data(self, nick: str, password: str, repeated_password: str) -> bool:
        """
        Validates the user input data for registration.
        
        :param nick: The nick entered by the user
        :param password: The password entered by the user
        :param repeated_password: The repeated password entered by the user
        :return: True if the data is valid, False otherwise
        """
        if not nick:
            self.register_screen('Field "Nick" is required')
            return False

        if not password:
            self.register_screen('Field "Password" is required')
            return False

        if not repeated_password:
            self.register_screen('Field "Repeat password" is required')
            return False

        if len(password) <= 4:
            self.register_screen('Password must be at least 5 characters long')
            return False

        if password != repeated_password:
            self.register_screen("Passwords do not match")
            return False

        if self.check_account_exists(nick):
            self.register_screen('User already exists')
            return False

        return True

    @staticmethod
    def check_account_exists(nick: str) -> bool:
        """
        Checks if an account with the given nick exists in the accounts-database.

        :param nick: The nick entered by the user
        :return: True if the account exists, False otherwise
        """
        with sqlite3.connect('databases/accounts.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM accounts WHERE nick=?", (nick,))
            return c.fetchone() is not None

    @staticmethod
    def insert_account_to_database(nick: str, password: str) -> None:
        """
        Inserts an account with the given nick and password into the accounts' database.

        :param nick: The nick entered by the user
        :param password: The password entered by the user
        :return: None
        """
        with sqlite3.connect('databases/accounts.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO accounts VALUES (?, ?)", (nick, password))
            conn.commit()

    @staticmethod
    def insert_default_record_to_database(nick: str) -> None:
        """
        Inserts a default record for the user into the records' database.

        :param nick: The nick entered by the user
        :return: None
        """
        RecordsDatabase().check_and_adjust_columns_number()
        number_of_levels = GlobalVariables.number_of_levels

        with sqlite3.connect('databases/records.db') as conn:
            c = conn.cursor()

            # Create a list of null values for each level
            null_values = [None] * number_of_levels

            # Create query
            placeholders = ", ".join("NULL" for _ in null_values)
            query = f"INSERT INTO records VALUES (?, {placeholders})"

            # Insert default records
            c.execute(query, (nick,))
            conn.commit()
