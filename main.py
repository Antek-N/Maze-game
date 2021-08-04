from pygame.locals import *
import pygame
from sys import exit
import time


class Player:
    x = 70  # x start location
    y = 70  # y start location
    speed_of_movement = 0.4

    # Control settings
    def move_right(self):
        self.x += self.speed_of_movement

    def move_left(self):
        self.x -= self.speed_of_movement

    def move_up(self):
        self.y -= self.speed_of_movement

    def move_down(self):
        self.y += self.speed_of_movement


class MazeCreator:
    def __init__(self, width, height, maze):
        self.width = width
        self.height = height
        self.maze = maze
        self.index_y = 0
        self.index_x = 0
        self.list_of_blocks = []

    # Handle collisions
    def collisions(self):

        for i in range(0, self.width * self.height):
            if self.maze[self.index_x + (self.index_y * self.width)] == 1:
                self.list_of_blocks.append((self.index_x * 50 - 10,
                                           (self.index_x + 1) * 50,
                                            self.index_y * 50 - 10,
                                           (self.index_y + 1) * 50))

            self.index_x += 1
            if self.index_x > self.width - 1:
                self.index_x = 0
                self.index_y += 1

        return self.list_of_blocks

    # Drawing maze
    def draw(self, display_surf, image_surf, finish_block_surf):
        index_x = 0
        index_y = 0

        for i in range(0, self.width * self.height):

            if self.maze[index_x + (index_y * self.width)] == 1:
                display_surf.blit(image_surf, (index_x * 50, index_y * 50))

            display_surf.blit(finish_block_surf, ((9 - 1) * 50, (12 - 1) * 50))

            index_x = index_x + 1
            if index_x > self.width - 1:
                index_x = 0
                index_y = index_y + 1


class App:
    window_width = 800
    window_height = 600
    player = 0

    def __init__(self):
        self._display_surf = None
        self._image_surf = None
        self._block_surf = None
        self._finish_block_surf = None
        self.player = Player()
        maze_width = 16
        maze_height = 12
        self.maze = MazeCreator(maze_width, maze_height, maze=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                                               1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1,
                                                               1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1,
                                                               1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1,
                                                               1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1,
                                                               1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1,
                                                               1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1,
                                                               1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1,
                                                               1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1,
                                                               1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1,
                                                               1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1,
                                                               1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1])

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.window_width, self.window_height))

        pygame.display.set_icon(pygame.image.load('icon.png'))  # Set icon
        pygame.display.set_caption('DotGame')  # Set title
        self._image_surf = pygame.image.load("player.png").convert()
        self._block_surf = pygame.image.load("block.jpeg").convert()
        self._finish_block_surf = pygame.image.load("finish_block.jpeg").convert()

    def to_time(self, ms, actual):

        ms -= actual

        m = ms // 60000
        ms = ms - 60000 * m
        m = str(m)

        #  declare minutes /\

        s = ms // 1000
        ms = ms - 1000 * s
        s = str(s)
        if len(s) < 2:
            s = "0" + s

        #  declare seconds /\

        ms = round(ms / 100)
        ms = str(ms)
        if len(ms) < 2:
            ms = "0" + ms

        #  declare milliseconds /\

        return m + ":" + s + ":" + ms

    def on_render(self, counter_of_loses, timer):
        pygame.display.set_caption("DotGame")
        self._display_surf.fill((0, 35, 35))
        self._display_surf.blit(self._image_surf, (self.player.x, self.player.y))
        self.maze.draw(self._display_surf, self._block_surf, self._finish_block_surf)
        self._display_surf.blit(counter_of_loses, (50, 0))
        self._display_surf.blit(timer, (525, 0))
        pygame.display.flip()

    # Main part
    def on_execute(self):

        save_file = open("data.txt", "a+")
        counter_of_loses = 0
        self.on_init()
        collision_list = self.maze.collisions()
        font_color = (0, 0, 0)
        font_obj = pygame.font.Font(r"C:\Windows\Fonts\segoeprb.ttf", 30)
        actual = 0  # variable which take actual ticks when program must set time to 0

        while True:

            # TIME COUNTER

            milliseconds = pygame.time.get_ticks()

            # HANDLE EVENTS

            if 390 < self.player.x < 440 and 540 < self.player.y < 590:
                save_file.write("\n\n" + time.asctime() + ":" + "\n")
                message = App.to_time(self, milliseconds, actual) + "- Tries no. " + str(counter_of_loses + 1) + "\n"
                save_file.write(message)
                time.sleep(0.4)
                pygame.quit()
                exit()

            # Handling collision
            for i in collision_list:
                if i[0] <= self.player.x <= i[1] and i[2] <= self.player.y <= i[3]:
                    self.player.x = 70  # Back to start location
                    self.player.y = 70  # Back to start location
                    time.sleep(0.4)
                    counter_of_loses += 1
                    actual = pygame.time.get_ticks()

            # Handling exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Handling control
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_RIGHT]:
                self.player.move_right()

            if keys[K_LEFT]:
                self.player.move_left()

            if keys[K_UP]:
                self.player.move_up()

            if keys[K_DOWN]:
                self.player.move_down()

            if keys[K_ESCAPE]:
                pygame.quit()
                exit()

            # Handling display frame
            if self.player.x <= 0:
                self.player.x = 0
            elif self.player.x >= 790:  # 790 - ( display_width - 10 )
                self.player.x = 790  # 790 - ( display_width - 10 )
            if self.player.y >= 590:  # 590 - ( display-height - 10 )
                self.player.y = 590  # 590 - ( display-height - 10 )
            elif self.player.y <= 0:
                self.player.y = 0

            # RENDER DISPLAY AND MAZE

            timer = font_obj.render("Time: " + App.to_time(self, milliseconds, actual), True, font_color)
            text_obj = font_obj.render("Loses: " + str(counter_of_loses), True, font_color)
            self.on_render(text_obj, timer)


# Start program
if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
