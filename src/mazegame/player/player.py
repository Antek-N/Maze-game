import logging

log = logging.getLogger(__name__)


class Player:
    """
    A class representing a player in the game.
    """

    def __init__(self) -> None:
        """
        Initializes a player object.

        :param: None
        :return: None
        """
        self.x = 0.0  # x start location
        self.y = 0.0  # y start location
        self.speed_of_movement = 1.45
        self.speed_of_movement = 1.45
        log.info("Player initialized at position (%.2f, %.2f) with speed %.2f", self.x, self.y, self.speed_of_movement)

    # Control settings
    def move_right(self) -> None:
        """
        Moves the player one unit rightwards.

        :param: None
        :return: None
        """
        self.x += self.speed_of_movement

    def move_left(self) -> None:
        """
        Moves the player one unit leftwards.

        :param: None
        :return: None
        """
        self.x -= self.speed_of_movement

    def move_up(self) -> None:
        """
        Moves the player one unit upwards.

        :param: None
        :return: None
        """
        self.y -= self.speed_of_movement

    def move_down(self) -> None:
        """
        Moves the player one unit downwards.

        :param: None
        :return: None
        """
        self.y += self.speed_of_movement
