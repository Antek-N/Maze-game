import time

import pygame

from mazegame.utils.global_variables.global_variables import GlobalVariables


class CollisionHandling:
    """
    A class that handles collisions in the game.

    This class checks collision ranges and performs actions when a collision occurs.
    """
    def collision_handling(self) -> None:
        """
        Handle collisions by checking collision ranges and performing actions if collision occurs.
        (main method of the class)

        :param: None
        :return: None
        """
        # Get collision_list
        collision_list = GlobalVariables.collision_list

        # Iterate over the collision list to check for collisions
        for collision_range in collision_list:
            if self.check_if_collision(collision_range):
                self.do_if_collision()

    @staticmethod
    def check_if_collision(collision_range: tuple) -> bool:
        """
        Checks if the player's position is in the given collision range.

        :param collision_range: A tuple representing the collision range (x_start, x_end, y_start, y_end).
        :return: bool - 1 if collision occurred, 0 otherwise
        """
        player = GlobalVariables.player_instance

        x_start, x_end, y_start, y_end = collision_range
        return x_start <= player.x <= x_end and y_start <= player.y <= y_end

    def do_if_collision(self) -> None:
        """
        Performs actions when a collision occurs.

        :param: None
        :return: None
        """
        # Get the necessary variables
        player = GlobalVariables.player_instance
        level = GlobalVariables.level
        display_height, display_width = self.get_display_resolution()

        # Reset the clock
        GlobalVariables.clock_instance.reset_and_stop_clock()

        # Set the player position to the start
        player.x = level['x_start_position'] - 30 + (display_width - level['maze_width'] * 50) / 2
        player.y = level['y_start_position'] - 30 + (display_height - level['maze_height'] * 50) / 2

        time.sleep(0.4)

        # Increment counter of loses
        GlobalVariables.counter_of_loses += 1

    @staticmethod
    def get_display_resolution() -> tuple[float, float]:
        """
        Gets and returns the display resolution.

        :param: None
        :return: A tuple containing the display height and width as floats.
        """
        display_info = pygame.display.Info()
        display_width = display_info.current_w
        display_height = display_info.current_h

        return display_height, display_width
