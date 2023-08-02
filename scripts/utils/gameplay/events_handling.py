import pygame
from pygame.locals import *

from scripts.menu.menu_manager.menu_manager import MenuManager

from scripts.utils.global_variables.global_variables import GlobalVariables


class EventsHandling:
    """
    A class that handles events in the game.

    This class checks for event types, such as quitting and key presses, and performs corresponding actions.
    """
    def events_handling(self) -> None:
        """
        Handles events, such as quitting and key presses.
        Checks for event types and key presses, and performs corresponding actions.
        (main method of the class)

        :param: None
        :return: None
        """
        # Handle exit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Handle key-events
        pygame.event.pump()
        keys = pygame.key.get_pressed()

        # Handle player movement based on pressed keys
        if keys[K_RIGHT] or keys[K_d]:
            GlobalVariables.player_instance.move_right()
            self.start_clock()
        if keys[K_LEFT] or keys[K_a]:
            GlobalVariables.player_instance.move_left()
            self.start_clock()
        if keys[K_UP] or keys[K_w]:
            GlobalVariables.player_instance.move_up()
            self.start_clock()
        if keys[K_DOWN] or keys[K_s]:
            GlobalVariables.player_instance.move_down()
            self.start_clock()

        # Handle the ESC key to go to the pause screen
        if keys[K_ESCAPE]:
            self.handle_escape()

    @staticmethod
    def start_clock() -> None:
        """
        Starts the clock if it's not already running.

        :param: None
        :return: None
        """
        if not GlobalVariables.clock_instance.get_is_running():
            GlobalVariables.clock_instance.start_clock()

    @staticmethod
    def handle_escape() -> None:
        """
        Handles the ESC key press by navigating to the pause screen.

        :param: None
        :return: None
        """
        MenuManager().go_to_screen("pause")
