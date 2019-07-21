import os       # to centre the screen
import sys      # to exit the program gracefully

import pygame as pg
from random import randrange

CAPTION = "Sit back, and watch snowfall"
SCREEN_SIZE = (1366,768)

WHITE = (255, 255, 255)
CHARCOAL = (54, 69, 79)

class Snow(object):
    def __init__(self):
        self.snow_density = 600
        self.snow_list = []
        self.populate_snow_list()


    def populate_snow_list(self):
        for i in range(600):
            x = randrange(0, SCREEN_SIZE[0])
            y = randrange(0, SCREEN_SIZE[1])
            self.snow_list.append([x, y])

    def update(self):
        for coord in self.snow_list:
            coord[1] += 2
            if coord[1] > 768:
                coord[0] = randrange(0, SCREEN_SIZE[0])
                coord[1] = randrange(-50, 0)

    def draw(self, screen):
        for coord in self.snow_list:
            pg.draw.circle(screen, WHITE, coord, 5)


class App(object):
    def __init__(self):
        self.screen = pg.display.get_surface() # just gives you the reference code
        self.clock = pg.time.Clock()
        self.fps = 60
        self.done = False
        self.keys = pg.key.get_pressed()
        self.color = CHARCOAL
        self.snow = Snow()

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def render(self):
        self.screen.fill(self.color)
        self.snow.draw(self.screen)
        pg.display.update()

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.snow.update()
            self.render()
            self.clock.tick(self.fps)

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1' # centre screen
    pg.init()

    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)

    App().main_loop()

    pg.quit()
    sys.exit() # fancy exit

if __name__ == "__main__":
    main()
