import pygame as pg
from constants import *
from state_enum import States
from states.menu import Menu
from states.game import Game
from states.pause import Pause


class App:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode(WIN_SIZE, pg.SCALED)
        pg.display.set_caption("Into The Pit")
        self.clock = pg.time.Clock()
        self.caption_font = pg.font.Font("assets/fonts/Zombie.ttf", 24)
        self.text_font = pg.font.Font("assets/fonts/DePixelHalbfett.ttf", 9)
        self.done = False

        self.states = {
            States.MENU: Menu(self),
            States.GAME: Game(self),
            States.PAUSE: Pause(self),
        }
        self.current_state = self.states[States.MENU]

        self.dt = 0
        self.mouse_pos = ()
        self.mouse_input = ()
        self.keys = ()

    def run(self):
        while not self.done:
            self.dt = self.clock.tick() / 1000
            self.mouse_pos = pg.mouse.get_pos()
            self.mouse_input = pg.mouse.get_pressed()
            self.keys = pg.key.get_pressed()

            for event in pg.event.get():
                self.current_state.handle_events(event)
                if event.type == pg.QUIT:
                    self.done = True

            self.screen.fill((0, 0, 0))

            self.current_state.update()
            self.current_state.draw()

            pg.display.flip()


if __name__ == '__main__':
    app = App()
    app.run()
    pg.quit()
