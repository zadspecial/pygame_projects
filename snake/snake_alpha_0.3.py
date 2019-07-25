import os     # to centre the screen
import sys    # to exit the program gracefully

import pygame as pg

from random import randrange

CAPTION = "Snake"
SCREEN_SIZE = (700, 400)
GRID_SIZE = 15
SPEED = 20

CHARCOAL = (54, 69, 79)
WHITE = (255, 255, 255)

class Snake(object):
    def __init__(self):
        self.dir = 'r'
        self.body_coords = []
        self.populate_body_coords()

    def get_rect(self, coord):
        return pg.Rect(coord, (GRID_SIZE, GRID_SIZE))

    def populate_body_coords(self):
        x = randrange(3*GRID_SIZE, SCREEN_SIZE[0], GRID_SIZE)
        y = randrange(0, SCREEN_SIZE[1], GRID_SIZE)
        for i in range(3):
            self.body_coords.append((x + i * GRID_SIZE, y))

    def draw(self, surface):
        for coord in self.body_coords:
            snake_segment = self.get_rect(coord)
            surface.fill(WHITE, snake_segment)

    def update_dir(self, keys):
        """Code to update self.dir"""
        if keys[pg.K_UP] and self.dir != 'u':
            self.dir = 'u'
        elif keys[pg.K_DOWN] and self.dir != 'd':
            self.dir = 'd'
        elif keys[pg.K_LEFT] and self.dir != 'l':
            self.dir = 'l'
        elif keys[pg.K_RIGHT] and self.dir != 'r':
            self.dir = 'r'

    def follow_dir(self):
        """Code to keep the snake moving"""
        if self.dir == 'u':
            Control(self).go_up()
        elif self.dir == 'd':
            Control(self).go_down()
        elif self.dir == 'l':
            Control(self).go_left()
        elif self.dir == 'r':
            Control(self).go_right()

    def update(self, keys, food, surface):
        self.update_dir(keys)
        self.follow_dir()

        # eat
        if food.food_particle.colliderect(self.get_rect(self.body_coords[0])):
            food.isEaten = True

        # if eaten, draw
        # if not, pop the tail as usual
        if food.isEaten:
            food.respawn()
            food.draw(surface)
        else:
            self.body_coords.pop()


class Control(object):
    def __init__(self, snake):
        self.snake = snake
        self.body_coords = snake.body_coords

    def go_up(self):
        (x, y) = (self.body_coords[0][0], self.body_coords[0][1])
        y -= GRID_SIZE
        self.body_coords.insert(0, (x, y))

    def go_down(self):
        (x, y) = (self.body_coords[0][0], self.body_coords[0][1])
        y += GRID_SIZE
        self.body_coords.insert(0, (x, y))

    def go_left(self):
        (x, y) = (self.body_coords[0][0], self.body_coords[0][1])
        x -= GRID_SIZE
        self.body_coords.insert(0, (x, y))

    def go_right(self):
        (x, y) = (self.body_coords[0][0], self.body_coords[0][1])
        x += GRID_SIZE
        self.body_coords.insert(0, (x, y))


class Food(object):
    def __init__(self):
        self.coord = self.get_random_coord()
        self.food_particle = pg.Rect(self.coord, (GRID_SIZE, GRID_SIZE))
        self.isEaten = False

    def get_random_coord(self):
        x = randrange(0, SCREEN_SIZE[0] - GRID_SIZE, GRID_SIZE)
        y = randrange(0, SCREEN_SIZE[1] - GRID_SIZE, GRID_SIZE)
        return (x, y)

    def draw(self, surface):
        # print(self.food_particle.center)
        # print(self.food_particle.size)
        surface.fill(WHITE, self.food_particle)

    def respawn(self):
        self.coord = self.get_random_coord()
        self.food_particle = pg.Rect(self.coord, (GRID_SIZE, GRID_SIZE))
        self.isEaten = False

    # def redraw(self):
    #     self = Food()
    #     self.draw()


class App(object):
    def __init__(self):
        self.screen = pg.display.get_surface()  # just gives you the reference code
        self.clock = pg.time.Clock()
        self.fps = SPEED
        self.done = False
        self.keys = pg.key.get_pressed()
        self.color = CHARCOAL
        self.snake = Snake()
        self.food = Food()

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
        self.food.draw(self.screen)  # might create problems with isEaten since render is after update
        pg.display.update()

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.snake.update(self.keys, self.food, self.screen)
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
