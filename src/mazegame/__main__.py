import logging
import sys

from mazegame.app import App
from mazegame.logging_config import configure_logging

log = logging.getLogger(__name__)


def main() -> int:
    """
    Main entry point:
    - configure logging
    - start the game
    - return exit code
    """
    try:
        configure_logging()
        log.debug("Logging configured successfully")

        log.info("Launching DotMaze")
        exit_code = App().run()

        log.info("Exited with code %s", exit_code)
        return exit_code

    except Exception as ex:
        log.exception("Unhandled exception occurred during game execution: %s", ex)
        return 1


if __name__ == "__main__":
    sys.exit(main())
