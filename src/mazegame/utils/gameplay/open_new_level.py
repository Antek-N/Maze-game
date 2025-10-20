import pygame
import logging

from mazegame.maze_creator.levels import Levels

from mazegame.utils.global_variables.global_variables import GlobalVariables
from mazegame.utils.collisions.get_collision_list import GetCollisionList

log = logging.getLogger(__name__)


class OpenNewLevel:
    """
    A class that opens a new game level.

    This class increments the current level number, resets the counter of losses,
    retrieves the new level data, updates the global variables with the new level data,
    and sets the player's position based on the new level data and display dimensions.
    """
    def open_new_level(self) -> None:
        """
        Opens a new game level.
        (main method of the class)

        Increments the current level number, resets the counter of losses,
        retrieves the new level data, updates the global variables with the new level data,
        and sets the player's position based on the new level data and display dimensions.

        :param: None
        :return: None
        """
        # Increment the current level number and reset the counter of losses
        GlobalVariables.current_level_number += 1
        GlobalVariables.counter_of_loses = 0
        log.info("Opening new level %d", GlobalVariables.current_level_number)

        # Get the new level data
        new_level = self.get_new_level_data()
        log.debug("New level data retrieved successfully")

        # Update the global variables with the new level data
        self.update_level(new_level)
        self.update_collision_list(new_level)
        log.debug("Global variables updated for level %d", GlobalVariables.current_level_number)

        # Set player position based on the new level data and display dimensions
        display_width, display_height = self.get_display_dimensions()
        maze_width, maze_height = new_level['maze_width'], new_level['maze_height']
        x_start_position, y_start_position = new_level['x_start_position'], new_level['y_start_position']

        self.set_player_position(display_width, display_height, maze_width, maze_height, x_start_position,
                                 y_start_position)
        log.info("Player positioned at start of level %d (x=%.2f, y=%.2f)",
                 GlobalVariables.current_level_number,
                 GlobalVariables.player_instance.x,
                 GlobalVariables.player_instance.y)

    @staticmethod
    def get_new_level_data() -> dict:
        """
        Retrieves and returns the data for the new level.

        :param: None
        :return: The data for the new level
        """
        log.debug("Retrieving level data for level %d", GlobalVariables.current_level_number)
        level_method = getattr(Levels, f"level{GlobalVariables.current_level_number}")
        return level_method()

    @staticmethod
    def update_level(level: dict) -> None:
        """
        Updates the global level variable with the new level data.

        :param level: The new level data
        :return: None
        """
        GlobalVariables.level = level
        log.debug("GlobalVariables.level updated")

    @staticmethod
    def update_collision_list(level: dict) -> None:
        """
        Updates the global collision list variable with the collision list for the new level.

        :param level: The new level data
        :return: None
        """
        log.debug("Updating collision list for level %d", GlobalVariables.current_level_number)
        GlobalVariables.collision_list = GetCollisionList.get_collisions_list(level['maze'],
                                                                              level['maze_width'],
                                                                              level['maze_height'])
        log.debug("Collision list updated (%d items)", len(GlobalVariables.collision_list))

    @staticmethod
    def get_display_dimensions() -> tuple[int, int]:
        """
        Retrieves and returns the current display dimensions.

        :param: None
        :return: The current display width and height
        """
        display_info = pygame.display.Info()
        log.debug("Fetched display dimensions: %dx%d", display_info.current_w, display_info.current_h)
        return display_info.current_w, display_info.current_h

    @staticmethod
    def set_player_position(display_width: float, display_height: float, maze_width: int, maze_height: int,
                            x_start_position: int, y_start_position: int) -> None:
        """
        Sets the player's position based on the display dimensions, maze dimensions, and start positions.

        :param display_width: The width of the display
        :param display_height: The height of the display
        :param maze_width: The width of the maze
        :param maze_height: The height of the maze
        :param x_start_position: The x player's start position
        :param y_start_position: The y player's start position
        :return: None
        """
        player = GlobalVariables.player_instance
        player.x = x_start_position - 30 + (display_width - maze_width * 50) / 2
        player.y = y_start_position - 30 + (display_height - maze_height * 50) / 2
        log.debug("Player position set to (%.2f, %.2f)", player.x, player.y)