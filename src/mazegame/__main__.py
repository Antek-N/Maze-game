import logging
import sys

from app import App
from logging_config import configure_logging


def main() -> int:
    """
    Main entry point:
    - configure logging
    - start the game
    - return exit code
    """
    configure_logging()
    log = logging.getLogger(__name__)
    log.debug("Logging configured")

    log.info("Launching DotMaze")
    return App().run()


if __name__ == "__main__":
    sys.exit(main())
