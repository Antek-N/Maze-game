import logging

import pygame

log = logging.getLogger(__name__)


class GetCollisionList:
    """
    A class that generates a list of collision ranges for barriers in the maze.

    This class provides a method to create a list of collision ranges for the barriers in the maze.
    Each collision range is represented as a tuple of four integers: (x_start, x_end, y_start, y_end).
    """

    @staticmethod
    def get_collisions_list(maze: list, maze_width: int, maze_height: int) -> list[tuple[float, float, float, float]]:
        """
        Generate a list of collision ranges for barriers in the maze.

        :param maze: The maze represented as a list of 0 and 1 (1 is a barrier).
        :param maze_width: The width of the maze.
        :param maze_height: The height of the maze.

        :return: A list of collision ranges for the barriers in the maze. Each collision range is represented
                 as a tuple of four integers: (x_start, x_end, y_start, y_end).
        """
        log.debug("Generating collision list for maze size %dx%d", maze_width, maze_height)
        # Get the current display resolution
        display_resolution = pygame.display.Info()
        display_width_full, display_height_full = display_resolution.current_w, display_resolution.current_h

        # Calculate the display offset based on the maze size
        display_offset_x = (display_width_full - maze_width * 50) / 2
        display_offset_y = (display_height_full - maze_height * 50) / 2

        list_of_barriers: list[tuple[float, float, float, float]] = []

        # Iterate over the maze blocks to add barriers to the list_of_barriers
        for index_y in range(maze_height):
            for index_x in range(maze_width):
                # Check if the maze block is a barrier.
                if maze[index_x + (index_y * maze_width)] == 1:
                    # Calculate the collision range for block
                    x_start = index_x * 50 - 10 + display_offset_x
                    x_end = (index_x + 1) * 50 + display_offset_x
                    y_start = index_y * 50 - 10 + display_offset_y
                    y_end = (index_y + 1) * 50 + display_offset_y

                    # Add the collision range to the list of blocks
                    list_of_barriers.append((x_start, x_end, y_start, y_end))

        log.debug("Generated %d collision ranges", len(list_of_barriers))
        return list_of_barriers
