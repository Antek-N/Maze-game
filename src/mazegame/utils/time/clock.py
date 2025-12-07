import logging
import time

log = logging.getLogger(__name__)


class Clock:
    """
    A class representing the game clock.
    """

    def __init__(self) -> None:
        self.start_time: float | None = None
        self.elapsed_time = 0.0
        self.is_running = False
        log.debug("Clock instance created")

    def start_clock(self) -> None:
        """
        Starts the time countdown.

        :param: None
        :return: None
        """
        self.start_time = time.time()
        self.is_running = True
        log.info("Clock started at %.3f", self.start_time)

    def stop_clock(self) -> None:
        """
        Stops the time countdown.

        :param: None
        :return: None
        """
        self.is_running = False
        log.info("Clock stopped at elapsed time %.3f", self.elapsed_time)

    def reset_and_stop_clock(self) -> None:
        """
        Resets the clock (stops it and sets time to 0.0).

        :param: None
        :return: None
        """
        self.start_time = None
        self.elapsed_time = 0.0
        self.is_running = False
        log.info("Clock reset and stopped")

    def update(self) -> None:
        """
        Updates the elapsed_time value based on the current time.

        :param: None
        :return: None
        """
        if self.start_time is not None and self.is_running:
            self.elapsed_time = time.time() - self.start_time

    def get_time(self) -> float:
        """
        Gets and returns the current elapsed time.

        :param: None
        :return: The current elapsed time in seconds
        """
        return self.elapsed_time

    def get_is_running(self) -> bool:
        """
        Checks if the clock is running and returns the answer.

        :param: None
        :return: True if the clock is running, False otherwise.
        """
        return self.is_running
