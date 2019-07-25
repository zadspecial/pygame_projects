import os     # to centre the screen
import sys    # to exit the program gracefully

import pygame as pg

CAPTION = "Snake"
SCREEN_SIZE = (480, 800)

CHARCOAL = (54, 69, 79)
WHITE = (255, 255, 255)

DIRECT_DICT = {
    'i': (1, 0),  # iniial
    'u': (0, -1),
    'd': (0, 1),
    'l': (-1, 0),
    'r': (1, 0)
}

class Snake(object):
    INITIAL_SNAKE_SIZE = (60, 5)

    def __init__(self):
        self.rect = pg.Rect((0, 0), self.INITIAL_SNAKE_SIZE)
        self.rect.center = tuple(i//2 for i in SCREEN_SIZE)
        self.speed = 2
        self.dir = 'i'
        # self.image

    def draw(self, surface):
        surface.fill(WHITE, self.rect)

    # def start_moving(self):
    #     self.rect.x += self.speed

    def bound_rect(self, surface):
        """Prevents the snake from going beyond the screen. Called in update()"""
        bounding_rect = surface.get_bounding_rect()
        self.rect.clamp_ip(bounding_rect)

    # def move_up(self):
    #     if self.dir in ('i', 'r'):
    #         self.rect.y = self.rect.width - self.rect.height
    #         self.rect.y += self.speed
    #     self.dir = 'u'

    def update(self, surface, keys):
        self.bound_rect(surface)
        # if self.dir == 'i':
        #     self.start_moving()

        # code for turning

        if keys[pg.K_UP]:
            if self.dir not in ('u', 'd'):
                Control(self, self.speed).turn_up()
        elif keys[pg.K_DOWN]:
            if self.dir not in ('u', 'd'):
                Control(self, self.speed).turn_down()
        elif keys[pg.K_LEFT]:
            if self.dir not in ('i', 'l', 'r'):
                Control(self, self.speed).turn_left()
        elif keys[pg.K_RIGHT]:
            if self.dir not in ('i', 'l', 'r'):
                Control(self, self.speed).turn_right()

        # code to keep it moving
        for dir in DIRECT_DICT:
            if self.dir == dir:
                (x, y) = (i * self.speed for i in DIRECT_DICT[dir])
                self.rect.move_ip(x, y)


    # def make_continuous(self):
    #     if self.rect.x > SCREEN_SIZE[0] - self.rect.width:
    #         self.rect.x = 0
    #
    #     if self.rect.y > SCREEN_SIZE[1]:
    #         self.rect.y = 0


class Control(object):
    def __init__(self, snake, speed):
        self.snake = snake
        self.speed = speed

    def turn_up(self):
        if self.snake.dir in ('i', 'r'):
            self.snake.rect.x += self.snake.rect.width - self.snake.rect.height
        # elif self.snake.dir == 'l':
            # (self.snake.rect.width, self.snake.rect.height) = (self.snake.rect.height, self.snake.rect.width)
        (self.snake.rect.width, self.snake.rect.height) = (self.snake.rect.height, self.snake.rect.width)
        self.snake.dir = 'u'

    def turn_down(self):
        if self.snake.dir in ('i', 'r'):
            self.snake.rect.x -= (self.snake.rect.height - self.snake.rect.width)
            self.snake.rect.y += (self.snake.rect.height - self.snake.rect.width)
        elif self.snake.dir == 'l':
            self.snake.rect.y += (self.snake.rect.height - self.snake.rect.width)
        (self.snake.rect.width, self.snake.rect.height) = (self.snake.rect.height, self.snake.rect.width)
        self.snake.dir = 'd'

    def turn_left(self):
        if self.snake.dir == 'd':
            self.snake.rect.y += (self.snake.rect.height - self.snake.rect.width)
        (self.snake.rect.width, self.snake.rect.height) = (self.snake.rect.height, self.snake.rect.width)
        self.snake.dir = 'l'


    def turn_right(self):
        if self.snake.dir == 'u':
            self.snake.rect.x -= (self.snake.rect.height - self.snake.rect.width)

        elif self.snake.dir == 'd':
            self.snake.rect.x -= (self.snake.rect.height - self.snake.rect.width)
            self.snake.rect.y += (self.snake.rect.height - self.snake.rect.width)
        (self.snake.rect.width, self.snake.rect.height) = (self.snake.rect.height, self.snake.rect.width)
        self.snake.dir = 'r'



class App(object):
    def __init__(self):
        self.screen = pg.display.get_surface()  # just gives you the reference code
        self.clock = pg.time.Clock()
        self.fps = 60
        self.done = False
        self.keys = pg.key.get_pressed()
        self.color = CHARCOAL
        self.snake = Snake()

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type in (pg.KEYUP, pg.KEYDOWN):
                self.keys = pg.key.get_pressed()

    def render(self):
        self.screen.fill(self.color)
        # all drawing goes here
        self.snake.draw(self.screen)
        pg.display.update()

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.snake.update(self.screen, self.keys)
            self.render()
            self.clock.tick(self.fps)


def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # centre screen
    pg.init()

    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)

    App().main_loop()

    pg.quit()
    sys.exit()  # fancy exit


if __name__ == "__main__":
    main()
