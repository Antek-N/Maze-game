from sys import exit
import time
import pygame
from pygame.locals import *
import sqlite3
import scripts.Player as Player
import scripts.Menu as Menu
import scripts.MazeCreator as MazeCreator


class App:

    def __init__(self, next_level: int, player_x: int, player_y: int, background_color: tuple[int, int, int],
                 maze_width: int, maze_height: int, maze_color: tuple[int, int, int], maze: list[int]) -> None:
        self.next_level = next_level
        self.player_x = player_x  # player start position (x)
        self.player_y = player_y  # player start position (y)
        self.background_color = background_color
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.maze_color = maze_color
        self.maze = MazeCreator.MazeCreator(maze_width, maze_height, maze)
        self.display = None
        self.player = Player.Player(player_x, player_y, self.maze_width, self.maze_height)
        display_resolution = pygame.display.Info()
        self.display_width, self.display_height = display_resolution.current_w, display_resolution.current_h

    # CREATE DISPLAY
    def create_display(self) -> None:
        self.display = pygame.display.set_mode((self.display_width, self.display_height))

    @staticmethod
    def save_records(new_record_list: list[int]) -> list[str]:
        is_new_record_list = []
        # database start
        conn = sqlite3.connect('databases/records.db')
        c = conn.cursor()
        c.execute(
            f"""
                    SELECT * FROM records WHERE nick = "{Menu.Menu.nick()}"
                    """)
        old_record_list = c.fetchall()
        record_list = []
        for i in old_record_list[0][1:]:
            record_list.append(i)
        for i in range(len(new_record_list)):
            if int(new_record_list[i]) < record_list[i]:
                record_list[i] = int(new_record_list[i])
                is_new_record_list.append("   NEW RECORD")
            else:
                is_new_record_list.append("")

        c.execute(f"""UPDATE records SET nick = '{Menu.Menu.nick()}',
                                         level1 = {record_list[0]},
                                         level2 = {record_list[1]},
                                         level3 = {record_list[2]},
                                         level4 = {record_list[3]},
                                         level5 = {record_list[4]},
                                         level6 = {record_list[5]},
                                         level7 = {record_list[6]},
                                         level8 = {record_list[7]} WHERE nick = '{Menu.Menu.nick()}';""")
        conn.commit()
        conn.close()
        # database end

        return is_new_record_list

    # CONVERT MS TO M:SS:MS FORMAT
    @staticmethod
    def to_time(ms: int, current_time: int, is_start: int) -> str:
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
            ms = "00" + ms
        elif len(ms) < 3:
            ms = "0" + ms

        return f"{m}:{s}:{ms}" if is_start else "0:00:000"

    def collision_handling(self, collision_list: list[tuple[int, int, int]], counter_of_loses: int, current_time: int,
                           start_time: int) -> [int, int, int]:
        for i in collision_list:
            if i[0] <= self.player.x <= i[1] and i[2] <= self.player.y <= i[3]:
                # Back to start location \/
                self.player.x = self.player_x - 30 + (self.display_width - self.maze_width * 50) / 2
                self.player.y = self.player_y - 30 + (self.display_height - self.maze_height * 50) / 2
                time.sleep(0.4)
                counter_of_loses += 1
                current_time = pygame.time.get_ticks()
                start_time = 0
        return counter_of_loses, current_time, start_time

    def events_handling(self, current_time: int, start_time: int, new_record_list: list[int],
                        record_list: list[int]) -> [int, int]:
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
            is_new_record_list = self.save_records(new_record_list)
            Menu.Menu.pause(Menu.Menu(), self.next_level-1, record_list, new_record_list, is_new_record_list)
        return current_time, start_time

    def render_display(self, counter_of_loses: int, current_time: int, font_color: tuple[int, int, int], font_type,
                       milliseconds: int, start_time: int) -> None:
        timer = font_type.render(f"Time: {App.to_time(milliseconds, current_time, start_time)}", True, font_color)
        loses_counter = font_type.render(f"Loses: {str(counter_of_loses)}", True, font_color)
        self.display.fill(self.background_color)  # Drawing display
        self.maze.draw(self.display, self.maze_color)  # Drawing maze
        self.display.blit(loses_counter, (50, 0))  # Drawing counter of loses
        self.display.blit(timer, (self.display_width - 275, 0))  # Drawing timer
        pygame.draw.rect(self.display, (200, 200, 50), (self.player.x, self.player.y, 10, 10))  # Drawing player
        pygame.display.flip()

    def finish_handling(self, current_time: int, milliseconds: int, new_record_list: list[int],
                        record_list: list[int]) -> None:
        if self.player.x <= 0 + (self.display_width - self.maze_width * 50) / 2 \
                or self.player.x >= self.maze_width * 50 - 10 + (self.display_width - self.maze_width * 50) / 2 \
                or self.player.y >= self.maze_height * 50 - 10 + (self.display_height - self.maze_height * 50) / 2 \
                or self.player.y <= 0 + (self.display_height - self.maze_height * 50) / 2:
            time.sleep(0.4)
            # Open new level
            self.open_new_level(current_time, milliseconds, new_record_list,
                                record_list)

    def open_new_level(self, current_time: int, milliseconds: int, new_record_list: list[int],
                       record_list: list[int]) -> None:
        if self.next_level == 2:
            new_record_list.append(milliseconds - current_time)
            MazeCreator.MazeCreator.level2().on_execute(current_time, record_list, new_record_list)
        if self.next_level == 3:
            new_record_list.append(milliseconds - current_time)
            MazeCreator.MazeCreator.level3().on_execute(current_time, record_list, new_record_list)
        if self.next_level == 4:
            new_record_list.append(milliseconds - current_time)
            MazeCreator.MazeCreator.level4().on_execute(current_time, record_list, new_record_list)
        if self.next_level == 5:
            new_record_list.append(milliseconds - current_time)
            MazeCreator.MazeCreator.level5().on_execute(current_time, record_list, new_record_list)
        if self.next_level == 6:
            new_record_list.append(milliseconds - current_time)
            MazeCreator.MazeCreator.level6().on_execute(current_time, record_list, new_record_list)
        if self.next_level == 7:
            new_record_list.append(milliseconds - current_time)
            MazeCreator.MazeCreator.level7().on_execute(current_time, record_list, new_record_list)
        if self.next_level == 8:
            new_record_list.append(milliseconds - current_time)
            MazeCreator.MazeCreator.level8().on_execute(current_time, record_list, new_record_list)
        else:
            new_record_list.append(milliseconds - current_time)
            if_new_record_list = self.save_records(new_record_list)
            Menu.Menu.result_board(Menu.Menu(), new_record_list, if_new_record_list)

    # MAIN PART
    def on_execute(self, current_time: int, record_list: list[int], new_record_list: list[int], start_time=0) -> None:
        counter_of_loses = 0
        collision_list = self.maze.collisions()  # Set color of text
        self.create_display()
        font_type = pygame.font.Font(r"C:\Windows\Fonts\segoeprb.ttf", 30)  # Set font type
        font_color = (255 - self.background_color[0], 255 - self.background_color[1], 255 - self.background_color[2])
        clock = pygame.time.Clock()
        fps = 120

        while True:

            milliseconds = pygame.time.get_ticks()  # get current program time

            counter_of_loses, current_time, start_time = self.collision_handling(collision_list, counter_of_loses,
                                                                                 current_time, start_time)

            current_time, start_time = self.events_handling(current_time, start_time, new_record_list, record_list)

            self.render_display(counter_of_loses, current_time, font_color, font_type, milliseconds, start_time)

            self.finish_handling(current_time, milliseconds, new_record_list, record_list)

            clock.tick(fps)


# Start program
if __name__ == "__main__":
    pygame.init()
    start = Menu.Menu()
    start.menu("")
