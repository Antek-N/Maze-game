import pygame
import pygame_menu
import sqlite3
import main
import scripts.MazeCreator as MazeCreator


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
        MazeCreator.MazeCreator.level1().on_execute(0, [], [])

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
        conn = sqlite3.connect('databases/accounts.db')
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
        main.App.save_records(new_record_list)
        record_string = ""
        for index, i in enumerate(new_record_list):
            record_string += f"level{index+1}: {main.App.to_time(i, 0, 1)}\n"
        menu = pygame_menu.Menu(height=320,
                                theme=pygame_menu.themes.THEME_DARK,
                                title='Result board',
                                width=1000)
        if record_string:
            menu.add.label(record_string, max_char=-1, font_size=25, font_color=(255, 255, 255))
        else:
            menu.add.label("You have no results\n", max_char=-1, font_size=25, font_color=(255, 0, 0))
        menu.add.button('Continue', self.menu_when_login)
        menu.mainloop(self.display)

    @staticmethod
    def start(level, record_list, new_record_list):
        if level == 1:
            MazeCreator.MazeCreator.level1().on_execute(0, record_list, new_record_list)
        elif level == 2:
            MazeCreator.MazeCreator.level2().on_execute(0, record_list, new_record_list)
        elif level == 3:
            MazeCreator.MazeCreator.level3().on_execute(0, record_list, new_record_list)
        elif level == 4:
            MazeCreator.MazeCreator.level4().on_execute(0, record_list, new_record_list)
        elif level == 5:
            MazeCreator.MazeCreator.level5().on_execute(0, record_list, new_record_list)
        elif level == 6:
            MazeCreator.MazeCreator.level6().on_execute(0, record_list, new_record_list)

    def pause(self, level, record_list, new_record_list):
        menu = pygame_menu.Menu(height=320,
                                theme=pygame_menu.themes.THEME_DARK,
                                title='Pause',
                                width=1000)
        menu.add.button('Play again', self.start, level, record_list, new_record_list)
        menu.add.button('Back to menu', self.result_board, new_record_list)
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
        conn = sqlite3.connect('databases/records.db')
        c = conn.cursor()
        c.execute(
            f"""
                            SELECT * FROM records WHERE nick = "{nick}"
                            """)
        old_record_list = c.fetchall()
        record_string = ""
        for index, i in enumerate(old_record_list[0][1:]):
            record_string += f"level{index+1}: {main.App.to_time(i, 0, 1)}\n"

        menu = pygame_menu.Menu(height=320,
                                theme=pygame_menu.themes.THEME_DARK,
                                title='My records',
                                width=1000)
        menu.add.label(record_string, max_char=-1, font_size=25, font_color=(255, 255, 255))
        menu.add.button('Back', self.records)
        menu.mainloop(self.display)

    def global_records(self):
        conn = sqlite3.connect('databases/records.db')
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
            record_string += f"level{index+1}: {main.App.to_time(i, 0, 1)}\n"
        menu = pygame_menu.Menu(height=320,
                                theme=pygame_menu.themes.THEME_DARK,
                                title='My records',
                                width=1000)
        menu.add.label(record_string, max_char=-1, font_size=25, font_color=(255, 255, 255))

        menu.add.button('Back', self.records)
        menu.mainloop(self.display)

    def apply_register(self):
        conn = sqlite3.connect('databases/accounts.db')
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

        conn = sqlite3.connect('databases/accounts.db')
        c = conn.cursor()
        c.execute(f'INSERT INTO accounts VALUES ("{nick}", "{password}")')
        conn.commit()
        conn.close()

        conn = sqlite3.connect('databases/records.db')
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

    @staticmethod
    def nick():
        return nick
