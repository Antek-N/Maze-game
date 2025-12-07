import logging
from collections.abc import Callable
from typing import Any

log = logging.getLogger(__name__)


class MenuManager:
    """
    A class that manages the navigation between screens in a menu.
    The list of available screens is declared in the menu_manager/set_screens.py file

    :cvar list stack: A list representing the screen navigation stack.
    :cvar dict screens: A dictionary containing screen classes. It is initialized in the set_screens.py file.
    """

    stack = ["previous_screen", "current_screen"]
    screens: dict[str, Callable[[], Any]] = {}

    def go_to_screen(self, screen: str) -> None:
        """
        Opens the specified screen.

        :param screen: The name of the screen to navigate to
        :return: None
        """
        if screen in self.screens:
            log.info("Navigating to screen: %s", screen)
            self.stack[0], self.stack[1] = self.stack[1], screen
            screen_method = self.screens[screen]
            screen_method()
            log.debug("Screen '%s' opened successfully", screen)
        # If the screen does not exist in the screens list
        else:
            log.warning("The '%s' screen doesn't exist in set_screen.py", screen)

    def go_to_previous_screen(self) -> None:
        """
        Opens the previous screen if it's exists

        :param: None
        :return: None
        """
        if self.stack[0] in self.screens:
            log.info("Returning to previous screen: %s", self.stack[0])
            self.stack[0], self.stack[1] = self.stack[1], self.stack[0]
            screen_method = self.screens[self.stack[1]]
            screen_method()
            log.debug("Returned to screen '%s'", self.stack[1])
        # If the previous screen does not exist
        else:
            log.warning("The previous screen doesn't exist")
