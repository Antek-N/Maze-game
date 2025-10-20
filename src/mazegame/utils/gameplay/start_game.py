import pygame

from mazegame.utils.gameplay.events_handling import EventsHandling
from mazegame.utils.collisions.collision_handling import CollisionHandling
from mazegame.utils.display.render_display import RenderDisplay
from mazegame.utils.gameplay.open_new_level import OpenNewLevel
from mazegame.utils.gameplay.finish_handling import FinishHandling
from mazegame.utils.display.create_display import create_display
from mazegame.utils.global_variables.global_variables import GlobalVariables
from mazegame.utils.paths.paths import base_dir

ASSETS_DIR = base_dir() / "assets"

class Game:
    """
    The Game class manages the game loop and various game events.

    The Game class is responsible for handling the game loop and processing game events such as
    collision detection, player movement, rendering the display, and handling the finish condition.
    It initializes the basic settings and variables, creates the display, sets the font type,
    and opens the first level. The main game loop is executed continuously until the game is exited.
    """
    @staticmethod
    def on_execute() -> None:
        """
        Initializes the basic settings and variables, and executes the main loop

        Creates the display, sets the font type, initializes the clock and FPS rate,
        opens the first level, and runs the game loop.

        :param: None
        :return: None
        """
        # Create display and set font type
        GlobalVariables.display = create_display()
        font_path = ASSETS_DIR / "fonts" / "segoeprb.ttf"
        GlobalVariables.font_type = pygame.font.Font(font_path, 30)

        # Set tick clock and fps rate
        tick_clock = pygame.time.Clock()
        fps = 220

        # Open first level
        OpenNewLevel().open_new_level()

        # Execute game mainloop
        while True:
            # Update the game clock
            GlobalVariables.clock_instance.update()

            # Handle collision detection
            CollisionHandling().collision_handling()

            # Handle events
            EventsHandling().events_handling()

            # Render the game display
            RenderDisplay().render_display()

            # Handle the game finish condition
            FinishHandling().finish_handling()

            # Limit the frame rate to the specified FPS
            tick_clock.tick(fps)
