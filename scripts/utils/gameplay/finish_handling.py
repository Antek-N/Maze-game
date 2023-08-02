import time

import pygame

from scripts.menu.menu_manager.menu_manager import MenuManager

from scripts.utils.gameplay.open_new_level import OpenNewLevel
from scripts.utils.global_variables.global_variables import GlobalVariables


class FinishHandling:
    """
    A class that handles the finish of a level.

    This class checks if the player is out of maze bounds (if the player has
    finished the game) and performs actions accordingly.
    """
    def finish_handling(self) -> None:
        """
        Handles the finish of a level by checking if the player is out of bounds and performing actions accordingly.
        (main method of the class)

        :param: None
        :return: None
        """
        # Retrieve necessary variables
        current_level_number = GlobalVariables.current_level_number
        number_of_levels = GlobalVariables.number_of_levels
        level = GlobalVariables.level

        # Get display dimensions
        display_info = pygame.display.Info()
        display_width = display_info.current_w
        display_height = display_info.current_h

        # Get maze dimensions
        maze_width = level['maze_width']
        maze_height = level['maze_height']

        # Calculate display and maze offsets
        x_offset = (display_width - maze_width * 50) / 2
        y_offset = (display_height - maze_height * 50) / 2

        # Get player position
        player_x, player_y = GlobalVariables.player_instance.x, GlobalVariables.player_instance.y

        # Check if player is out of bounds
        is_player_out_of_bounds = (
                player_x <= 0 + x_offset
                or player_x >= maze_width * 50 - 10 + x_offset
                or player_y >= maze_height * 50 - 10 + y_offset
                or player_y <= 0 + y_offset)

        if is_player_out_of_bounds:
            if current_level_number < number_of_levels:
                # If the current level is not the last level in the game
                time.sleep(0.4)
                self.open_new_level()
                self.append_time_and_reset_clock()
            else:
                # If the current level is not the last level in the game
                time.sleep(0.4)
                self.append_time_and_reset_clock()
                self.reset_current_level_and_show_result_board()

    @staticmethod
    def open_new_level() -> None:
        """
        Opens a new level.

        :param: None
        :return: None
        """
        OpenNewLevel().open_new_level()

    @staticmethod
    def append_time_and_reset_clock() -> None:
        """
        Appends the current time to the global times list and resets the clock.

        :param: None
        :return: None
        """
        GlobalVariables.times_list.append(GlobalVariables.clock_instance.get_time())
        GlobalVariables.clock_instance.reset_and_stop_clock()

    @staticmethod
    def reset_current_level_and_show_result_board() -> None:
        """
        Resets the current global level number and navigates to the result board screen.

        :param: None
        :return: None
        """
        GlobalVariables.current_level_number = 0
        MenuManager().go_to_screen("show_result_board")
