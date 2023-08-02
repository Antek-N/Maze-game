import logging


class MenuManager:
    """
    A class that manages the navigation between screens in a menu.
    The list of available screens is declared in the menu_manager/set_screens.py file

    :cvar list stack: A list representing the screen navigation stack.
    :cvar dict screens: A dictionary containing screen classes. It is initialized in the set_screens.py file.
    """
    stack = ["previous_screen", "current_screen"]
    screens = {}

    def go_to_screen(self, screen: str) -> None:
        """
        Opens the specified screen.

        :param screen: The name of the screen to navigate to
        :return: None
        """
        if screen in self.screens:
            self.stack[0], self.stack[1] = self.stack[1], screen
            screen_method = self.screens[screen]
            screen_method()
        # If the screen does not exist in the screens list
        else:
            logging.warning(f"The '{screen}' screen doesn't exist in set_screen.py")

    def go_to_previous_screen(self) -> None:
        """
        Opens the previous screen if it's exists

        :param: None
        :return: None
        """
        if self.stack[0] in self.screens:
            self.stack[0], self.stack[1] = self.stack[1], self.stack[0]
            screen_method = self.screens[self.stack[1]]
            screen_method()
        # If the previous screen does not exist
        else:
            logging.warning("The previous screen doesn't exist")
