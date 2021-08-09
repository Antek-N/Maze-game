from pygame.locals import *
import pygame
from sys import exit
import time
import pygame_menu


class Player:
    def __init__(self, x, y):
        self.x = x * 50 - 30  # x start location
        self.y = y * 50 - 30  # y start location
        self.speed_of_movement = 2.5

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
    def draw(self, display_surf, maze_color):
        self.index_x = 0
        self.index_y = 0

        for i in range(0, self.width * self.height):

            if self.maze[self.index_x + (self.index_y * self.width)] == 1:
                pygame.draw.rect(display_surf, maze_color, (self.index_x * 50, self.index_y * 50, 50, 50))

            self.index_x += 1
            if self.index_x > self.width - 1:
                self.index_x = 0
                self.index_y += 1


def start_the_game():
    level1 = App(2, 2, 2, (0, 35, 35), 16, 12, (150, 0, 0), [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
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
    actual = pygame.time.get_ticks()

    level1.on_execute(actual)


class App:

    def __init__(self, level, player_x, player_y, background_color, maze_width, maze_height, maze_color, maze):
        self.level = level
        self.player_x = player_x  # player start position (x)
        self.player_y = player_y  # player start position (y)
        self.background_color = background_color
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.maze_color = maze_color
        self.maze = MazeCreator(maze_width, maze_height, maze)
        self.display = None
        self.player = Player(player_x, player_y)

    def on_init(self):
        pygame.init()
        if self.level == 1:
            self.display = pygame.display.set_mode((1520, 750))
        else:
            self.display = pygame.display.set_mode((self.maze_width * 50, self.maze_height * 50))  # Make display

    @staticmethod
    def to_time(ms, actual, is_start):

        ms -= actual

        # Declare minutes
        m = ms // 60000
        ms = ms - 60000 * m
        m = str(m)

        # Declare seconds
        s = ms // 1000
        ms = ms - 1000 * s
        s = str(s)
        if len(s) < 2:
            s = "0" + s

        # Declare milliseconds
        ms = round(ms / 100)
        ms = str(ms)
        if len(ms) < 2:
            ms = "0" + ms

        return m + ":" + s + ":" + ms if is_start == 1 else "0:00:00"

    def start(self):
        menu = pygame_menu.Menu(height=300,
                                theme=pygame_menu.themes.THEME_DARK,
                                title='Welcome to DotMaze project!',
                                width=1000)
        user_name = menu.add.text_input('Nick: ', default='', maxchar=16)
        menu.add.button('Play', start_the_game)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(self.display)

    def on_render(self, loses_counter, timer):
        self.display.fill(self.background_color)  # Drawing display
        self.maze.draw(self.display, self.maze_color)  # Drawing maze
        self.display.blit(loses_counter, (50, 0))  # Drawing counter of loses
        self.display.blit(timer, (self.maze_width * 50 - 275, 0))  # Drawing timer
        pygame.draw.rect(self.display, (200, 200, 50), (self.player.x, self.player.y, 10, 10))  # Drawing player
        pygame.display.flip()

    # Main part
    def on_execute(self, actual):

        pygame.display.set_caption("DotGame")  # Set title
        pygame.display.set_icon(pygame.image.load(r'img\icon.png'))  # Set icon
        data_file = open(r"data.txt", "a+")  # Open data file
        data_file.write("\n-------")
        counter_of_loses = 0
        collision_list = self.maze.collisions()
        font_color = (0, 0, 0)  # Set color of text
        self.on_init()
        font_obj = pygame.font.Font(r"C:\Windows\Fonts\segoeprb.ttf", 30)  # Set font type
        clock = pygame.time.Clock()
        fps = 120
        start_time = 0

        level1 = App(2, 2, 2, (0, 35, 35), 16, 12, (150, 0, 0),
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
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

        level2 = App(3, 11, 10, (0, 24, 20), 28, 15, (0, 100, 100),
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                      1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1,
                      1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1,
                      1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1,
                      1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1,
                      1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1,
                      1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1,
                      1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1,
                      1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,
                      1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1,
                      1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1,
                      1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1,
                      1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1,
                      1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

        while True:

            # TIME COUNTER

            milliseconds = pygame.time.get_ticks()

            # HANDLE EVENTS

            # Handling collision
            for i in collision_list:
                if i[0] <= self.player.x <= i[1] and i[2] <= self.player.y <= i[3]:
                    self.player.x = self.player_x * 50 - 30  # Back to start location
                    self.player.y = self.player_y * 50 - 30  # Back to start location
                    time.sleep(0.4)
                    counter_of_loses += 1
                    actual = pygame.time.get_ticks()
                    start_time = 0

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
                if start_time == 0:
                    actual = pygame.time.get_ticks()
                    start_time = 1

            if keys[K_LEFT]:
                self.player.move_left()
                if start_time == 0:
                    actual = pygame.time.get_ticks()
                    start_time = 1

            if keys[K_UP]:
                self.player.move_up()
                if start_time == 0:
                    actual = pygame.time.get_ticks()
                    start_time = 1

            if keys[K_DOWN]:
                self.player.move_down()
                if start_time == 0:
                    actual = pygame.time.get_ticks()
                    start_time = 1

            if keys[K_ESCAPE]:
                pygame.quit()
                exit()

            # Handling button
            if self.level == 1:
                self.start()

            # Handling finish (display frame)
            if self.player.x <= 0 \
               or self.player.x >= self.maze_width * 50 - 10 \
               or self.player.y >= self.maze_height * 50 - 10 \
               or self.player.y <= 0:
                data_file.write("\n\n" + time.asctime() + ":" + "\n")
                message = "{0}- Tries no. {1}\n ".format(App.to_time(milliseconds, actual, start_time),
                                                         str(counter_of_loses + 1))
                data_file.write(message)
                data_file = open(r"data.txt", "a+")
                time.sleep(0.4)
                if self.level == 0:
                    pass
                elif self.level == 1:
                    level1.on_execute(actual)
                elif self.level == 2:
                    level2.on_execute(actual)
                else:
                    pygame.quit()
                    exit()

            # RENDER DISPLAY AND MAZE

            timer = font_obj.render("Time: " + App.to_time(milliseconds, actual, start_time), True, font_color)
            loses_counter = font_obj.render("Loses: " + str(counter_of_loses), True, font_color)
            self.on_render(loses_counter, timer)
            clock.tick(fps)


# Start program
if __name__ == "__main__":
    # level = App(player_x, player_y, background_color, maze_width(blocks), maze_height(blocks), maze_color, maze_plan)
    TheApp = App(1, 0, 0, (0, 0, 0), 1, 1, (0, 0, 0), [1])

    TheApp.on_execute(0)
