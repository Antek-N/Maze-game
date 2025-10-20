import logging

import pygame

from mazegame.menu.menu_manager.menu_manager import MenuManager
from mazegame.menu.menu_manager.set_screens import SetScreens
from mazegame.menu.window_settings import WindowSettings
from mazegame.utils.global_variables.global_variables import GlobalVariables

log = logging.getLogger(__name__)


class App:
    """Main class of the DotMaze application."""

    def __init__(self) -> None:
        pygame.init()
        log.debug("Pygame initialized")

        self._initialize_game()

    @staticmethod
    def _initialize_game() -> None:
        """Initialize window settings, screens, globals, and launch the menu."""
        log.info("Initializing DotMaze environment")
        WindowSettings().initialize_settings()
        log.debug("Window settings initialized")

        SetScreens.set_screens()
        log.debug("Screens registered")

        GlobalVariables()
        log.debug("Global variables initialized")

        log.info("Launching initial menu screen")
        MenuManager().go_to_screen("initial_menu")

    def run(self) -> int:
        """Run the application (placeholder for future main loop)."""
        log.info("DotMaze started successfully")
        return 0
