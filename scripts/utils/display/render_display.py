import pygame

from scripts.maze_creator.draw_maze import DrawMaze

from scripts.utils.time.convert_time import convert_time
from scripts.utils.global_variables.global_variables import GlobalVariables


class RenderDisplay:
    """
    A class that renders the display for the game.

    This class draws the maze, counter of losses, timer, and player on the display.
    It updates the display to show the current state of the game.
    """
    @staticmethod
    def render_display() -> None:
        """
        Renders the display by drawing the maze, counter of losses, timer and player.
        Updates the display to show the current state of the game.

        :param: None
        :return: None
        """
        # Retrieve necessary variables
        display_info = pygame.display.Info()
        display_width = display_info.current_w

        level = GlobalVariables.level

        # Draw background
        GlobalVariables.display.fill(level['background_color'])

        # Draw maze
        DrawMaze.draw_maze(GlobalVariables.display, level['maze'], level['maze_color'], level['maze_width'], level['maze_height'])

        # Draw counter_of_loses and timer
        font_type = GlobalVariables.font_type
        font_color = tuple(255 - color for color in level['background_color'])
        timer_text = f"Time: {convert_time(GlobalVariables.clock_instance.get_time())}"
        loses_counter_text = f"Loses: {str(GlobalVariables.counter_of_loses)}"

        GlobalVariables.display.blit(font_type.render(loses_counter_text, True, font_color), (5, 0))
        GlobalVariables.display.blit(font_type.render(timer_text, True, font_color), (display_width - 275, 0))

        # Draw player
        pygame.draw.rect(GlobalVariables.display, (200, 200, 50), (GlobalVariables.player_instance.x, GlobalVariables.player_instance.y, 10, 10))

        # Update the display
        pygame.display.flip()
