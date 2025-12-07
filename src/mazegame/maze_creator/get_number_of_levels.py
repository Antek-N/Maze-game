import logging

from mazegame.maze_creator.levels import Levels

log = logging.getLogger(__name__)


class GetNumberOfLevels:
    """
    A class that provides a method to get the number of levels available in a game.
    """

    @staticmethod
    def get_number() -> int:
        """
        Gets and returns the number of levels.

        Retrieves the number of levels available by iterating over the `Levels` class in maze_creator/levels file
        and checking the existence of level attributes. It starts with `level_number = 1`
        and increments it until no more level attributes are found.

        :param: None
        :return: The number of levels.
        """
        log.debug("Checking number of available levels...")
        level_number = 1
        while hasattr(Levels, f"level{level_number}"):
            level_number += 1

        total_levels = level_number - 1
        log.debug("Detected %d levels", total_levels)
        return total_levels
