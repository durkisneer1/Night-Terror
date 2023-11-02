import pygame as pg
from src.constants import WIN_SIZE
from src.state_enum import States
from src.states.menu import Menu
from src.states.game import Game
from src.states.pause import Pause
from src.states.mirror import Mirror
from src.states.dream import Dream
from src.states.note import Note


class App:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode(WIN_SIZE, pg.SCALED)
        pg.display.set_caption("Night Terror")
        self.clock = pg.time.Clock()

        self.caption_font = pg.font.Font("assets/fonts/Zombie.ttf", 24)
        self.button_font = pg.font.Font("assets/fonts/DePixelHalbfett.ttf", 9)
        self.note_font = pg.font.Font("assets/fonts/dogicapixel.ttf", 8)

        pg.mixer.music.load("assets/audio/theme.ogg")
        pg.mixer.music.play(-1)

        self.current_act = 0  # Max 5
        self.states = {
            States.MENU: Menu(self),
            States.GAME: Game(self),
            States.PAUSE: Pause(self),
            States.MIRROR: Mirror(self),
            States.DREAM: Dream(self),
            States.NOTE: Note(self),
        }
        self.current_state = self.states[States.MENU]

        self.done = False
        self.dt = 0
        self.mouse_pos = ()
        self.mouse_input = ()
        self.keys = ()

    def run(self):
        while not self.done:
            self.dt = min(self.clock.tick() / 1000, 0.1)
            self.mouse_pos = pg.mouse.get_pos()
            self.mouse_input = pg.mouse.get_pressed()
            self.keys = pg.key.get_pressed()

            for event in pg.event.get():
                self.current_state.handle_events(event)
                if event.type == pg.QUIT:
                    self.done = True

            self.screen.fill((21, 18, 37))

            self.current_state.update()
            self.current_state.draw()

            pg.display.flip()


if __name__ == "__main__":
    app = App()
    app.run()
    pg.quit()
