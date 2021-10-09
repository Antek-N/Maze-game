import pygame


class Player:
    def __init__(self, x: int, y: int, maze_width: int, maze_height: int) -> None:
        display_resolution = pygame.display.Info()
        display_width, display_height = display_resolution.current_w, display_resolution.current_h
        display_width -= maze_width * 50
        display_height -= maze_height * 50
        display_width /= 2
        display_height /= 2
        self.x = x - 30 + display_width  # x start location
        self.y = y - 30 + display_height  # y start location
        self.speed_of_movement = 2.5

    # Control settings
    def move_right(self) -> None:
        self.x += self.speed_of_movement

    def move_left(self) -> None:
        self.x -= self.speed_of_movement

    def move_up(self) -> None:
        self.y -= self.speed_of_movement

    def move_down(self) -> None:
        self.y += self.speed_of_movement
