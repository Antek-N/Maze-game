import pygame


def create_display():
    """
    Creates a Pygame display object with the current display resolution.

    :param: None
    :return: A Pygame display object with the current display resolution
    """
    display_resolution = pygame.display.Info()
    display_width, display_height = display_resolution.current_w, display_resolution.current_h
    display = pygame.display.set_mode((display_width, display_height))

    return display
