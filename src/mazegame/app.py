import logging
import pygame

from mazegame.menu.window_settings import WindowSettings
from mazegame.menu.menu_manager.menu_manager import MenuManager
from mazegame.menu.menu_manager.set_screens import SetScreens
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
        WindowSettings().initialize_settings()
        SetScreens.set_screens()
        GlobalVariables()
        MenuManager().go_to_screen("initial_menu")

    def run(self) -> int:
        """Run the application (placeholder for future main loop)."""
        log.info("DotMaze started successfully")
        return 0
