import os     # to centre the screen
import sys    # to exit the program gracefully

import pygame as pg

from random import randrange

CAPTION = "Snake"
SCREEN_SIZE = (675, 375)
CELL_SIZE = 15
SPEED = 20

CHARCOAL = (54, 69, 79)
WHITE = (255, 255, 255)


class Snake(object):
    """
    A class to represent our Snake
    """
    def __init__(self):
        """
        Keep record of the direction, snake body coordinates, and
        scores;
        """
        self.dir = 'r'
        self.body_coords = []
        self.populate_body_coords()
        self.score = 0
        self.text, self.text_rect = self.setup_font()

    def populate_body_coords(self):
        """
        Create the snake body coordinates
        """
        x = randrange(3*CELL_SIZE, SCREEN_SIZE[0], CELL_SIZE)
        y = randrange(0, SCREEN_SIZE[1], CELL_SIZE)
        for i in range(3):
            self.body_coords.insert(0, (x + i * CELL_SIZE, y))

    def setup_font(self):
        """
        Preparing the text to show the score
        """
        font = pg.font.SysFont('timesnewroman', 30)
        text_str = "Score: " + str(self.score)
        text = font.render(text_str, True, WHITE)
        text_rect = text.get_rect()
        return text, text_rect

    def draw(self, surface):
        """
        Blit snake and text to the target surface (screen)
        :param surface:
        :return:
        """
        for coord in self.body_coords:
            snake_segment = self.get_rect_from_coord(coord)
            surface.fill(WHITE, snake_segment)
            surface.blit(self.text, self.text_rect)

    # noinspection PyMethodMayBeStatic
    def get_rect_from_coord(self, coord):
        """
        Returns a Rect for a coordinate
        :param coord: tuple
        :return: RectType
        """
        return pg.Rect(coord, (CELL_SIZE, CELL_SIZE))

    def update(self, keys, food, surface):
        """
        Make the snake follow the logic of the game.
        :param keys: list
        :param food: RectType
        :param surface: SurfaceType
        :return: None
        """
        self.update_dir(keys)
        self.follow_dir()
        self.make_continuous()

        # eat when in contact with food
        if food.food_particle.colliderect(self.get_rect_from_coord(self.body_coords[0])):
            food.isEaten = True
            self.score += 1
            self.text, self.text_rect = self.setup_font()

        # if eaten, draw
        # if not, pop the tail as usual
        if food.isEaten:
            food.respawn()
            food.draw(surface)
        else:
            self.body_coords.pop()

        self.kill_when_eats_itself()

    def update_dir(self, keys):
        """
        Update the direction with keypress
        """
        if keys[pg.K_UP] and self.dir != 'd':
            self.dir = 'u'
        elif keys[pg.K_DOWN] and self.dir != 'u':
            self.dir = 'd'
        elif keys[pg.K_LEFT] and self.dir != 'r':
            self.dir = 'l'
        elif keys[pg.K_RIGHT] and self.dir != 'l':
            self.dir = 'r'

    def follow_dir(self):
        """
        Keep the snake moving
        """
        if self.dir == 'u':
            Control(self).go_up()
        elif self.dir == 'd':
            Control(self).go_down()
        elif self.dir == 'l':
            Control(self).go_left()
        elif self.dir == 'r':
            Control(self).go_right()

    def make_continuous(self):
        """
        If the snake goes beyond the screen, make it appear from the opposite side
        """
        for i in range(len(self.body_coords)):
            if self.body_coords[i][0] > SCREEN_SIZE[0]:
                x, y = self.body_coords.pop(i)
                x = 0
                self.body_coords.insert(i, (x, y))
            elif self.body_coords[i][0] < 0:
                x, y = self.body_coords.pop(i)
                x = SCREEN_SIZE[0]
                self.body_coords.insert(i, (x, y))

            if self.body_coords[i][1] > SCREEN_SIZE[1]:
                x, y = self.body_coords.pop(i)
                y = 0
                self.body_coords.insert(i, (x, y))
            elif self.body_coords[i][1] < 0:
                x, y = self.body_coords.pop(i)
                y = SCREEN_SIZE[1]
                self.body_coords.insert(i, (x, y))

    def kill_when_eats_itself(self):
        """
        End game when the snake eats itself
        """
        body_coords_set = set(self.body_coords)
        if len(body_coords_set) != len(self.body_coords):
            pg.quit()
            sys.exit()


class Control(object):
    """
    A class to provide control methods for our snake
    """
    def __init__(self, snake):
        self.snake = snake
        self.body_coords = snake.body_coords

    def go_up(self):
        (x, y) = (self.body_coords[0][0], self.body_coords[0][1])
        y -= CELL_SIZE
        self.body_coords.insert(0, (x, y))

    def go_down(self):
        (x, y) = (self.body_coords[0][0], self.body_coords[0][1])
        y += CELL_SIZE
        self.body_coords.insert(0, (x, y))

    def go_left(self):
        (x, y) = (self.body_coords[0][0], self.body_coords[0][1])
        x -= CELL_SIZE
        self.body_coords.insert(0, (x, y))

    def go_right(self):
        (x, y) = (self.body_coords[0][0], self.body_coords[0][1])
        x += CELL_SIZE
        self.body_coords.insert(0, (x, y))


class Food(object):
    """
    A class that represents the tiny food particles that spawn randomly
    """
    def __init__(self):
        """
        Record the the food particle, its coordinate, and whether it got eaten
        """
        self.coord = self.get_random_coord()
        self.food_particle = pg.Rect(self.coord, (CELL_SIZE, CELL_SIZE))
        self.isEaten = False

    # noinspection PyMethodMayBeStatic
    def get_random_coord(self):
        """
        Produces a random coordinate tuple
        :return: tuple
        """
        x = randrange(0, SCREEN_SIZE[0] - CELL_SIZE, CELL_SIZE)
        y = randrange(0, SCREEN_SIZE[1] - CELL_SIZE, CELL_SIZE)
        return x, y  # tuple

    def draw(self, surface):
        """
        Draws the food particle to the target surface
        :param surface: SurfaceType
        """
        surface.fill(WHITE, self.food_particle)

    def respawn(self):
        """
        Spawn a new food particle when the old one gets eaten
        """
        self.coord = self.get_random_coord()
        self.food_particle = pg.Rect(self.coord, (CELL_SIZE, CELL_SIZE))
        self.isEaten = False


class App(object):
    """
    A class to manage our game loop, event, and overall program flow
    """
    def __init__(self):
        """
        Get a reference to the screen (created in main); define necessary
        attributes; and create our snake and a food particle
        """
        self.screen = pg.display.get_surface()  # just gives you the reference code
        self.clock = pg.time.Clock()
        self.fps = SPEED
        self.done = False
        self.keys = pg.key.get_pressed()
        self.color = CHARCOAL
        self.snake = Snake()
        self.food = Food()

    def main_loop(self):
        """
        This is the game loop
        """
        while not self.done:
            self.event_loop()
            self.snake.update(self.keys, self.food, self.screen)
            self.render()
            self.clock.tick(self.fps)

    def event_loop(self):
        """
        Checks for key presses and other events; provides necessary commands
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type in (pg.KEYUP, pg.KEYDOWN):
                self.keys = pg.key.get_pressed()

    def render(self):
        """
        All drawing goes here
        """
        self.screen.fill(self.color)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        pg.display.update()


def main():
    """
    Prepare the environment, create a display, and start the program
    """
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # centre screen
    pg.init()

    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)

    App().main_loop()

    pg.quit()
    sys.exit()  # fancy exit


if __name__ == "__main__":
    main()
