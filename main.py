from pygame.locals import *
import pygame
from sys import exit


class Player:
    x = 70  # x start location
    y = 64  # y start location
    speed_of_movement = 0.2

    def Move_right(self):
        self.x += self.speed_of_movement

    def Move_left(self):
        self.x -= self.speed_of_movement

    def Move_up(self):
        self.y -= self.speed_of_movement

    def Move_down(self):
        self.y += self.speed_of_movement


class Maze_creator:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.maze = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 0, 1, 0, 1, 0, 1, 0, 1, 1,
                     1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                     1, 0, 1, 1, 0, 1, 1, 1, 0, 1,
                     1, 0, 1, 0, 0, 0, 0, 1, 0, 1,
                     1, 1, 1, 0, 1, 0, 1, 1, 0, 1,
                     1, 0, 0, 0, 1, 1, 1, 0, 1, 1,
                     1, 0, 1, 1, 1, 0, 0, 0, 0, 1,
                     1, 0, 0, 0, 0, 0, 1, 0, 0, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 0, 1]

    def colisions(self):

        self.index_y = 0
        self.index_x = 0
        self.list_of_blocks = []

        for i in range(0, self.width * self.height):
            if self.maze[self.index_x + (self.index_y * self.width)] == 1:
                self.list_of_blocks.append((self.index_x * 50 - 10, (self.index_x + 1) * 50, self.index_y * 50 - 10, (self.index_y + 1) * 50))

            self.index_x += 1
            if self.index_x > self.width - 1:
                self.index_x = 0
                self.index_y += 1

        return self.list_of_blocks


    def draw(self, display_surf, image_surf):
        index_x = 0
        index_y = 0

        for i in range(0, self.width * self.height):

            if self.maze[index_x + (index_y * self.width)] == 1:
                display_surf.blit(image_surf, (index_x * 50, index_y * 50))

            index_x = index_x + 1
            if index_x > self.width - 1:
                index_x = 0
                index_y = index_y + 1


class App:
    window_width = 800
    window_height = 600
    player = 0

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._block_surf = None
        self.player = Player()
        self.maze = Maze_creator()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.window_width, self.window_height), pygame.HWSURFACE)

        pygame.display.set_caption('DotGame')
        self._running = True
        self._image_surf = pygame.image.load("player.png").convert()
        self._block_surf = pygame.image.load("block.jpeg").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self._display_surf.blit(self._image_surf, (self.player.x, self.player.y))
        self.maze.draw(self._display_surf, self._block_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        end = False
        colision_list = self.maze.colisions()
        while (self._running):

            for i in colision_list:
                if (i[0] <= self.player.x <= i[1] and i[2] <= self.player.y <= i[3]):
                    end = True
                    print("you lose!")

            if (end == True):
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[K_RIGHT]):
                self.player.Move_right()

            if (keys[K_LEFT]):
                self.player.Move_left()

            if (keys[K_UP]):
                self.player.Move_up()

            if (keys[K_DOWN]):
                self.player.Move_down()

            if (keys[K_ESCAPE]):
                self._running = False

            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
