from mazegame.maze_creator.levels import Levels


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
        level_number = 1
        while hasattr(Levels, f"level{level_number}"):
            level_number += 1

        return level_number - 1
