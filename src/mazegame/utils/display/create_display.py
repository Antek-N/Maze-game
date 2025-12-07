import logging

import pygame

log = logging.getLogger(__name__)


def create_display() -> pygame.Surface:
    """
    Creates a Pygame display object with the current display resolution.

    :param: None
    :return: A Pygame display object with the current display resolution
    """
    log.debug("Fetching display resolution")
    display_resolution = pygame.display.Info()
    display_width, display_height = display_resolution.current_w, display_resolution.current_h
    log.info("Creating display surface with resolution %dx%d", display_width, display_height)
    display = pygame.display.set_mode((display_width, display_height))

    return display
