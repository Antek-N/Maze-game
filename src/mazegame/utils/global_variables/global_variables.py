from mazegame.maze_creator.get_number_of_levels import GetNumberOfLevels

from mazegame.player.player import Player

from mazegame.utils.time import clock


class GlobalVariables:
    """
    A class that holds global variables used in the game.

    :cvar str NICK: The player's nickname.
    :cvar pygame.Surface display: The Pygame display surface.
    :cvar dict level: The current level data.
    :cvar int current_level_number: The number of the current level.
    :cvar int counter_of_losses: The counter of losses.
    :cvar list collision_list: A list of collision ranges.
    :cvar list times_list: A list of recorded times.
    :cvar clock_instance: The clock instance.
    :cvar player_instance: The player instance.
    :cvar int number_of_levels: The number of levels in the game.
    :cvar pygame.font.Font font_type: The font type used in the game.
    """
    nick = ""
    display = None
    level = None
    current_level_number = 0
    counter_of_loses = 0
    collision_list = []
    times_list = []
    clock_instance = clock.Clock()
    player_instance = Player()
    number_of_levels = GetNumberOfLevels.get_number()
    font_type = None
