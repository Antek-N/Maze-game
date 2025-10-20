import logging

import pygame

log = logging.getLogger(__name__)


class DrawMaze:
    """
    A class that provides a method to draw a maze on a given Pygame display surface.
    """

    @staticmethod
    def draw_maze(display: pygame.Surface, maze: list, maze_color: tuple, maze_width: int, maze_height: int) -> None:
        """
        Draws the maze on the display.

        :param display: The Pygame display surface to draw on.
        :param maze: The maze represented as a 1-dimensional list of 1 and 0.
        :param maze_color: The color of the maze walls (RGB tuple).
        :param maze_width: The width of the maze (number of columns).
        :param maze_height: The height of the maze (number of rows).

        :return: None
        """

        # Get display resolution
        display_resolution = pygame.display.Info()
        display_width_full, display_height_full = display_resolution.current_w, display_resolution.current_h

        # Calculate display offsets to center the maze
        display_offset_x = (display_width_full - maze_width * 50) / 2
        display_offset_y = (display_height_full - maze_height * 50) / 2

        # Iterate over maze coordinates
        for y in range(maze_height):
            for x in range(maze_width):
                # Check if maze cell is a wall (value of 1)
                if maze[y * maze_width + x] == 1:
                    # Calculate rectangle layout for wall cell
                    rect_layout = (x * 50 + display_offset_x, y * 50 + display_offset_y, 50, 50)
                    # Draw the wall cell on the display
                    pygame.draw.rect(display, maze_color, rect_layout)
