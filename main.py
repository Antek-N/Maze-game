# DotMaze project
# 08.09.2021
# Antek-N

from pygame.locals import *
import pygame
from sys import exit
import time
import pygame_menu
import sqlite3


class Player:
    def __init__(self, x, y, maze_width, maze_height):
        display_resolution = pygame.display.Info()
        display_width, display_height = display_resolution.current_w, display_resolution.current_h
        display_width -= maze_width * 50
        display_height -= maze_height * 50
        display_width /= 2
        display_height /= 2
        self.x = x * 50 - 30 + display_width  # x start location
        self.y = y * 50 - 30 + display_height  # y start location
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


class Menu:

    def __init__(self):
        display_resolution = pygame.display.Info()
        width, height = display_resolution.current_w, display_resolution.current_h
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption("DotGame")  # Set title
        pygame.display.set_icon(pygame.image.load(r'img\icon.png'))

    @staticmethod
    def check_nick(value):
        global nick
        nick = value

    @staticmethod
    def check_password(value):
        global password
        password = value

    @staticmethod
    def check_nickname(value):
        global nick
        nick = value

    # OPEN FIRST LEVEL
    @staticmethod
    def start_the_game():
        level1 = MazeCreator.define_levels(if_level1=True)
        level1.on_execute(0, [], [])

    def menu_when_login(self, text=""):
        menu = pygame_menu.Menu(height=320,
                                theme=pygame_menu.themes.THEME_DARK,
                                title='Welcome to DotMaze project!',
                                width=1000)
        text = text
        menu.add.label(text, max_char=-1, font_size=15, font_color=(255, 255, 255))
        menu.add.button('Play', self.start_the_game)
        menu.add.button('Records', self.records)
        menu.add.button('Help', self.help)
        menu.add.button('Log out', self.menu)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(self.display)

    def login(self, text=""):
        global nick, password
        password = ""
        nick = ""
        menu = pygame_menu.Menu(height=320,
                                theme=pygame_menu.themes.THEME_DARK,
                                title='Sign in',
                                width=1000)
        menu.add.label(text, max_char=-1, font_size=15, font_color=(200, 0, 0))
        menu.add.text_input('nick: ', default="", onchange=self.check_nick, maxchar=16)
        menu.add.text_input('Password: ', default="", onchange=self.check_password, maxchar=32, password=True)
        menu.add.button('Continue', self.apply_login)
        menu.add.button('Back', self.menu)
        menu.mainloop(self.display)

    def apply_login(self):
        conn = sqlite3.connect('accounts.db')
        c = conn.cursor()
        c.execute(
            """
            SELECT nick FROM accounts
            """)
        nick_list = c.fetchall()
        # database end
        new_nick_list = []
        for i in nick_list:
            for a in i:
                new_nick_list.append(a)

        c.execute(
            f"""
            SELECT password FROM accounts WHERE nick = "{nick}"
            """)
        db_password = c.fetchall()

        if not nick:
            self.login("Nick is required")
        if not password:
            self.login("Password is required")
        if nick not in new_nick_list:
            self.login("Incorrect nick")
        if password != db_password[0][0]:
            self.login("Incorrect nick or password")
        self.menu_when_login()

    def register(self, text=""):
        menu = pygame_menu.Menu(height=320,
                                theme=pygame_menu.themes.THEME_DARK,
                                title='Sign up',
                                width=1000)
        global nick, password
        password = ""
        nick = ""
        text = text
        menu.add.label(text, max_char=-1, font_size=15, font_color=(200, 0, 0))
        menu.add.text_input('nick: ', default="", onchange=self.check_nick, maxchar=16)
        menu.add.text_input('Password: ', default="", onchange=self.check_password, maxchar=32, password=True)
        menu.add.button('Continue', self.apply_register)
        menu.add.button('Back', self.menu)
        menu.mainloop(self.display)

    def result_board(self, new_record_list):
        record_string = ""
        for index, i in enumerate(new_record_list):
            record_string += f"level{index+1}: {App.to_time(i, 0, 1)}\n"
        menu = pygame_menu.Menu(height=320,
                                theme=pygame_menu.themes.THEME_DARK,
                                title='Welcome to DotMaze project!',
                                width=1000)
        menu.add.label(record_string, max_char=-1, font_size=25, font_color=(255, 255, 255))
        menu.add.button('Continue', self.menu_when_login)
        menu.mainloop(self.display)

    def records(self):

        menu = pygame_menu.Menu(height=320,
                                theme=pygame_menu.themes.THEME_DARK,
                                title='Records',
                                width=1000)
        menu.add.button('My records', self.my_records)
        menu.add.button('Global records', self.global_records)
        menu.add.button('Back', self.menu_when_login)
        menu.mainloop(self.display)

    def my_records(self):
        conn = sqlite3.connect('records.db')
        c = conn.cursor()
        c.execute(
            f"""
                            SELECT * FROM records WHERE nick = "{nick}"
                            """)
        old_record_list = c.fetchall()
        record_string = ""
        for index, i in enumerate(old_record_list[0][1:]):
            record_string += f"level{index+1}: {App.to_time(i, 0, 1)}\n"

        menu = pygame_menu.Menu(height=320,
                                theme=pygame_menu.themes.THEME_DARK,
                                title='My records',
                                width=1000)
        menu.add.label(record_string, max_char=-1, font_size=25, font_color=(255, 255, 255))
        menu.add.button('Back', self.records)
        menu.mainloop(self.display)

    def global_records(self):
        conn = sqlite3.connect('records.db')
        c = conn.cursor()
        c.execute(
            f"""
                            SELECT MIN(level1),
                            MIN(level2), 
                            MIN(level3), 
                            MIN(level4), 
                            MIN(level5), 
                            MIN(level6) FROM records
                            """)
        old_record_list = c.fetchall()
        record_string = ""
        for index, i in enumerate(old_record_list[0]):
            record_string += f"level{index+1}: {App.to_time(i, 0, 1)}\n"
        menu = pygame_menu.Menu(height=320,
                                theme=pygame_menu.themes.THEME_DARK,
                                title='My records',
                                width=1000)
        menu.add.label(record_string, max_char=-1, font_size=25, font_color=(255, 255, 255))

        menu.add.button('Back', self.records)
        menu.mainloop(self.display)

    def apply_register(self):
        conn = sqlite3.connect('accounts.db')
        c = conn.cursor()
        c.execute(
            """
            SELECT nick FROM accounts
            """)
        nick_list = c.fetchall()
        conn.commit()
        conn.close()
        # database end
        new_nick_list = []
        for i in nick_list:
            for a in i:
                new_nick_list.append(a)
        if not nick:
            self.register("Nick is required")
        if not password:
            self.register("Password is required")
        if nick in new_nick_list:
            self.register("Nick is in usage")

        conn = sqlite3.connect('accounts.db')
        c = conn.cursor()
        c.execute(f'INSERT INTO accounts VALUES ("{nick}", "{password}")')
        conn.commit()
        conn.close()

        conn = sqlite3.connect('records.db')
        c = conn.cursor()
        c.execute(
            f"""
            INSERT INTO records VALUES ("{nick}", 999999999, 999999999, 999999999, 999999999, 999999999, 999999999)
            """)
        conn.commit()
        conn.close()
        self.menu("You may login")

    def help(self):
        help_message = """1. To control use arrows or WSAD
        """
        menu = pygame_menu.Menu(height=320,
                                theme=pygame_menu.themes.THEME_DARK,
                                title='Help',
                                width=1000)
        menu.add.label(help_message, max_char=-1, font_size=25, font_color=(255, 255, 255))
        menu.add.button('Back', self.menu_when_login)
        menu.mainloop(self.display)

    def menu(self, text=""):
        menu = pygame_menu.Menu(height=320,
                                theme=pygame_menu.themes.THEME_DARK,
                                title='Welcome to DotMaze project!',
                                width=1000)
        global nick
        nick = ""
        text = text
        menu.add.label(text, max_char=-1, font_size=15, font_color=(255, 255, 255))
        menu.add.button('Sign in', self.login)
        menu.add.button('Sign up', self.register)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(self.display)


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
        display_resolution = pygame.display.Info()
        display_width, display_height = display_resolution.current_w, display_resolution.current_h
        display_width -= self.width * 50
        display_height -= self.height * 50
        display_width /= 2
        display_height /= 2
        for i in range(0, self.width * self.height):
            if self.maze[self.index_x + (self.index_y * self.width)] == 1:
                self.list_of_blocks.append((self.index_x * 50 - 10 + display_width,
                                            (self.index_x + 1) * 50 + display_width,
                                            self.index_y * 50 - 10 + display_height,
                                            (self.index_y + 1) * 50 + display_height))

            self.index_x += 1
            if self.index_x > self.width - 1:
                self.index_x = 0
                self.index_y += 1

        return self.list_of_blocks

    # Drawing maze
    def draw(self, display_surf, maze_color):
        display_resolution = pygame.display.Info()
        display_width, display_height = display_resolution.current_w, display_resolution.current_h
        self.index_x = 0
        self.index_y = 0
        display_width -= self.width * 50
        display_height -= self.height * 50
        display_width /= 2
        display_height /= 2

        for i in range(0, self.width * self.height):

            if self.maze[self.index_x + (self.index_y * self.width)] == 1:
                rect_layout = self.index_x * 50 + display_width, self.index_y * 50 + display_height, 50, 50
                pygame.draw.rect(display_surf, maze_color, rect_layout)

            self.index_x += 1
            if self.index_x > self.width - 1:
                self.index_x = 0
                self.index_y += 1

    @staticmethod
    def define_levels(if_level1):
        level1 = App(2, 2, 2, (35, 35, 35), 16, 12, (150, 0, 0),
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
        level5 = App(6, 2, 2, (40, 150, 40), 22, 14, (70, 0, 70),
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1,
                      1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1,
                      1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1,
                      1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1,
                      1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1,
                      1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1,
                      1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1,
                      1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1,
                      1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1,
                      1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1,
                      1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1,
                      1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1,
                      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1])
        level6 = App(7, 11, 10, (0, 24, 20), 28, 15, (0, 100, 100),
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
        if if_level1:
            return level1
        else:
            return level2, level3, level4, level5, level6


class App:

    def __init__(self, next_level, player_x, player_y, background_color, maze_width, maze_height, maze_color, maze):
        self.next_level = next_level
        self.player_x = player_x  # player start position (x)
        self.player_y = player_y  # player start position (y)
        self.background_color = background_color
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.maze_color = maze_color
        self.maze = MazeCreator(maze_width, maze_height, maze)
        self.display = None
        self.player = Player(player_x, player_y, self.maze_width, self.maze_height)
        display_resolution = pygame.display.Info()
        self.display_width, self.display_height = display_resolution.current_w, display_resolution.current_h

    # CREATE DISPLAY
    def create_display(self):
        self.display = pygame.display.set_mode((self.display_width, self.display_height))

    @staticmethod
    def save_records(new_record_list):
        # database start
        conn = sqlite3.connect('records.db')
        c = conn.cursor()
        c.execute(
            f"""
                    SELECT * FROM records WHERE nick = "{nick}"
                    """)
        old_record_list = c.fetchall()
        record_list = []
        for i in old_record_list[0][1:]:
            record_list.append(i)
        for i in range(len(new_record_list)):
            if int(new_record_list[i]) < record_list[i]:
                record_list[i] = int(new_record_list[i])

        c.execute(f"""UPDATE records SET nick = '{nick}',
                                         level1 = {record_list[0]},
                                         level2 = {record_list[1]},
                                         level3 = {record_list[2]},
                                         level4 = {record_list[3]},
                                         level5 = {record_list[4]},
                                         level6 = {record_list[5]} WHERE nick = '{nick}';""")
        conn.commit()
        conn.close()
        # database end

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
        ms = str(ms)
        if len(ms) < 2:
            ms = "0" + ms

        return f"{m}:{s}:{ms}" if is_start else "0:00:00"

    def collision_handling(self, collision_list, counter_of_loses, current_time, start_time):
        for i in collision_list:
            if i[0] <= self.player.x <= i[1] and i[2] <= self.player.y <= i[3]:
                # Back to start location \/
                self.player.x = self.player_x * 50 - 30 + (self.display_width - self.maze_width * 50) / 2
                self.player.y = self.player_y * 50 - 30 + (self.display_height - self.maze_height * 50) / 2
                time.sleep(0.4)
                counter_of_loses += 1
                current_time = pygame.time.get_ticks()
                start_time = 0
        return counter_of_loses, current_time, start_time

    def events_handling(self, current_time, start_time, new_record_list):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_records(new_record_list)
                pygame.quit()
                exit()
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT] or keys[K_d]:
            self.player.move_right()
            if start_time == 0:
                current_time = pygame.time.get_ticks()
                start_time = 1
        if keys[K_LEFT] or keys[K_a]:
            self.player.move_left()
            if start_time == 0:
                current_time = pygame.time.get_ticks()
                start_time = 1
        if keys[K_UP] or keys[K_w]:
            self.player.move_up()
            if start_time == 0:
                current_time = pygame.time.get_ticks()
                start_time = 1
        if keys[K_DOWN] or keys[K_s]:
            self.player.move_down()
            if start_time == 0:
                current_time = pygame.time.get_ticks()
                start_time = 1
        if keys[K_ESCAPE]:
            self.save_records(new_record_list)
            start.result_board(new_record_list)
        return current_time, start_time

    def finish_handling(self, counter_of_loses, current_time, milliseconds,
                        new_record_list, record_list, start_time):
        if self.player.x <= 0 + (self.display_width - self.maze_width * 50) / 2 \
                or self.player.x >= self.maze_width * 50 - 10 + (self.display_width - self.maze_width * 50) / 2 \
                or self.player.y >= self.maze_height * 50 - 10 + (self.display_height - self.maze_height * 50) / 2 \
                or self.player.y <= 0 + (self.display_height - self.maze_height * 50) / 2:
            data_file = open(r"data.txt", "a+")
            data_file.write(f"\n\n{time.asctime()}:\n{App.to_time(milliseconds, current_time, start_time)} - "
                            f"Tries no. {str(counter_of_loses + 1)}")
            time.sleep(0.4)
            # Open new level
            self.open_new_level(current_time, milliseconds, new_record_list,
                                record_list)

    def render_display(self, counter_of_loses, current_time, font_color, font_type, milliseconds, start_time):
        timer = font_type.render(f"Time: {App.to_time(milliseconds, current_time, start_time)}", True, font_color)
        loses_counter = font_type.render(f"Loses: {str(counter_of_loses)}", True, font_color)
        self.display.fill(self.background_color)  # Drawing display
        self.maze.draw(self.display, self.maze_color)  # Drawing maze
        self.display.blit(loses_counter, (50, 0))  # Drawing counter of loses
        self.display.blit(timer, (self.display_width - 275, 0))  # Drawing timer
        pygame.draw.rect(self.display, (200, 200, 50), (self.player.x, self.player.y, 10, 10))  # Drawing player
        pygame.display.flip()

    def open_new_level(self, current_time, milliseconds, new_record_list, record_list):
        level2, level3, level4, level5, level6 = MazeCreator.define_levels(if_level1=False)
        if self.next_level == 2:
            new_record_list.append(milliseconds - current_time)
            level2.on_execute(current_time, record_list, new_record_list)
        if self.next_level == 3:
            new_record_list.append(milliseconds - current_time)
            level3.on_execute(current_time, record_list, new_record_list)
        if self.next_level == 4:
            new_record_list.append(milliseconds - current_time)
            level4.on_execute(current_time, record_list, new_record_list)
        if self.next_level == 5:
            new_record_list.append(milliseconds - current_time)
            level5.on_execute(current_time, record_list, new_record_list)
        if self.next_level == 6:
            new_record_list.append(milliseconds - current_time)
            level6.on_execute(current_time, record_list, new_record_list)
        else:
            new_record_list.append(milliseconds - current_time)
            self.save_records(new_record_list)
            print("You win, congratulations!")
            start.result_board(new_record_list)

    # MAIN PART
    def on_execute(self, current_time, record_list, new_record_list):

        counter_of_loses = 0
        collision_list = self.maze.collisions()  # Set color of text
        self.create_display()
        font_type = pygame.font.Font(r"C:\Windows\Fonts\segoeprb.ttf", 30)  # Set font type
        font_color = (255 - self.background_color[0], 255 - self.background_color[1], 255 - self.background_color[2])
        clock = pygame.time.Clock()
        fps = 120
        start_time = 0

        while True:

            milliseconds = pygame.time.get_ticks()  # get current program time

            counter_of_loses, current_time, start_time = self.collision_handling(collision_list, counter_of_loses,
                                                                                 current_time, start_time)

            current_time, start_time = self.events_handling(current_time, start_time, new_record_list)

            self.finish_handling(counter_of_loses, current_time, milliseconds, new_record_list, record_list, start_time)

            self.render_display(counter_of_loses, current_time, font_color, font_type, milliseconds, start_time)

            clock.tick(fps)


# Start program
if __name__ == "__main__":
    pygame.init()
    start = Menu()
    start.menu("")
