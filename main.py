from pygame.locals import *
import pygame
from sys import exit
import time
import pygame_menu
import tkinter as tk


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

    # CREATE DISPLAY
    def on_init(self):
        pygame.init()
        if self.level == 1:
            self.display = pygame.display.set_mode((1520, 750))  # If menu
        else:
            self.display = pygame.display.set_mode((self.maze_width * 50, self.maze_height * 50))  # If maze

    # DEFINE MENU
    def menu(self):
        menu = pygame_menu.Menu(height=300,
                                theme=pygame_menu.themes.THEME_DARK,
                                title='Welcome to DotMaze project!',
                                width=1000)
        menu.add.button('Play', self.start_the_game)
        menu.add.button('Records', self.records)
        menu.add.button('Help', self.start_the_game)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(self.display)

    # OPEN FIRST LEVEL
    @staticmethod
    def start_the_game():
        level1.on_execute(0, [], [])

    # COMPARE CURRENT TIME WITH RECORD
    @staticmethod
    def is_record(level, milliseconds, current_time, new_record_list, record_list):
        level = level - 2

        if milliseconds - current_time < int(record_list[level]):
            print("New record - " + str(milliseconds - current_time))
            new_record_list.append(milliseconds - current_time)
        else:
            print("Your time - " + str(milliseconds - current_time) + "\nRecord - " + record_list[level])
            new_record_list.append(record_list[level])

        return new_record_list

    # LOAD TKINTER DISPLAY WITH RECORDS LIST
    @staticmethod
    def records():
        record_list = ""
        record_read = open("records.txt", "r")
        for index, i in enumerate(record_read):
            i = i.strip()
            i = App.to_time(int(i), 0, 1)
            record_list += f"level {str(index + 1)} - {i}\n"
        window = tk.Tk()
        greeting = tk.Label(text=record_list)
        greeting.pack()
        window.mainloop()

    # CONVERT MS TO M:SS:MS FORMAT
    @staticmethod
    def to_time(ms, current_time, is_start):
        ms -= current_time

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

        return f"{m}:{s}:{ms}" if is_start else "0:00:00"

    # LOAD TKINTER DISPLAY WITH INSTRUCTION
    def help(self):
        pass

    # RENDER DISPLAY
    def on_render(self, loses_counter, timer):
        self.display.fill(self.background_color)  # Drawing display
        self.maze.draw(self.display, self.maze_color)  # Drawing maze
        self.display.blit(loses_counter, (50, 0))  # Drawing counter of loses
        self.display.blit(timer, (self.maze_width * 50 - 275, 0))  # Drawing timer
        pygame.draw.rect(self.display, (200, 200, 50), (self.player.x, self.player.y, 10, 10))  # Drawing player
        pygame.display.flip()

    @staticmethod
    def define_levels():
        global level1
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
        level2 = App(3, 15, 9, (20, 70, 20), 16, 15, (70, 70, 70),
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
                      1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1,
                      1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1,
                      1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1,
                      1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1,
                      1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0,
                      1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1,
                      1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1,
                      1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1,
                      1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1,
                      1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1,
                      1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1,
                      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1,
                      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        level3 = App(4, 2, 2, (150, 70, 20), 22, 10, (35, 35, 35),
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1,
                      1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1,
                      1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1,
                      1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1,
                      1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1,
                      1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1,
                      1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1,
                      1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0,
                      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        level4 = App(5, 12, 10, (150, 40, 150), 20, 13, (0, 0, 100),
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                      1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1,
                      1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1,
                      1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1,
                      1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1,
                      1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1,
                      1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1,
                      1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1,
                      1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1,
                      1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1,
                      1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1,
                      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        level5 = App(6, 11, 10, (0, 24, 20), 28, 15, (0, 100, 100),
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
        return level2, level3, level4, level5

    def open_new_level(self, current_time, level2, level3, level4, level5, milliseconds, new_record_list, record_list):
        if self.level == 2:
            new_record_list = self.is_record(self.level, milliseconds, current_time, new_record_list, record_list)
            level2.on_execute(current_time, record_list, new_record_list)
        if self.level == 3:
            new_record_list = self.is_record(self.level, milliseconds, current_time, new_record_list, record_list)
            level3.on_execute(current_time, record_list, new_record_list)
        if self.level == 4:
            new_record_list = self.is_record(self.level, milliseconds, current_time, new_record_list, record_list)
            level4.on_execute(current_time, record_list, new_record_list)
        if self.level == 5:
            new_record_list = self.is_record(self.level, milliseconds, current_time, new_record_list, record_list)
            level5.on_execute(current_time, record_list, new_record_list)
        else:
            new_record_list = self.is_record(self.level, milliseconds, current_time, new_record_list, record_list)
            record_write = open("records.txt", "w")
            for i in new_record_list:
                record_write.write(str(i) + "\n")
            print("You win, congratulations!")
            pygame.quit()
            exit()

    # MAIN PART
    def on_execute(self, current_time, record_list, new_record_list):
        pygame.display.set_caption("DotGame")  # Set title
        pygame.display.set_icon(pygame.image.load(r'img\icon.png'))  # Set icon
        data_file = open(r"data.txt", "a+")  # Open data file
        counter_of_loses = 0
        collision_list = self.maze.collisions()
        font_color = (0, 0, 0)  # Set color of text
        self.on_init()
        font_obj = pygame.font.Font(r"C:\Windows\Fonts\segoeprb.ttf", 30)  # Set font type
        clock = pygame.time.Clock()
        fps = 120
        start_time = 0
        if self.level == 2:
            record_read = open("records.txt", "r")
            record_list = [line.strip() for line in record_read]

        # DEFINE LEVELS
        level2, level3, level4, level5 = self.define_levels()

        while True:

            # OPEN MENU
            if self.level == 1:
                self.menu()

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
                    current_time = pygame.time.get_ticks()
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
                    current_time = pygame.time.get_ticks()
                    start_time = 1

            if keys[K_LEFT]:
                self.player.move_left()
                if start_time == 0:
                    current_time = pygame.time.get_ticks()
                    start_time = 1

            if keys[K_UP]:
                self.player.move_up()
                if start_time == 0:
                    current_time = pygame.time.get_ticks()
                    start_time = 1

            if keys[K_DOWN]:
                self.player.move_down()
                if start_time == 0:
                    current_time = pygame.time.get_ticks()
                    start_time = 1

            if keys[K_ESCAPE]:
                pygame.quit()
                exit()

            # Handling finish (display frame)
            if self.player.x <= 0 \
                    or self.player.x >= self.maze_width * 50 - 10 \
                    or self.player.y >= self.maze_height * 50 - 10 \
                    or self.player.y <= 0:
                data_file.write(f"\n\n{time.asctime()}:\n{App.to_time(milliseconds, current_time, start_time)} - "
                                f"Tries no. {str(counter_of_loses + 1)}")
                data_file = open(r"data.txt", "a+")
                time.sleep(0.4)
                # Open new level
                self.open_new_level(current_time, level2, level3, level4, level5, milliseconds, new_record_list,
                                    record_list)

            # RENDER DISPLAY AND MAZE

            timer = font_obj.render(f"Time: {App.to_time(milliseconds, current_time, start_time)}", True, font_color)
            loses_counter = font_obj.render(f"Loses: {str(counter_of_loses)}", True, font_color)
            self.on_render(loses_counter, timer)
            clock.tick(fps)


# Start program
if __name__ == "__main__":
    App(1, 0, 0, (0, 0, 0), 1, 1, (0, 0, 0), [1]).on_execute(0, [], [])
