import pygame as pg
from src.constants import WIN_SIZE
from src.state_enum import States
from src.states.menu import Menu
from src.states.game import Game
from src.states.pause import Pause
from src.states.mirror import Mirror
from src.states.dream import Dream
from src.states.desk import Note
from src.eyes import eye_positions


class App:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode(WIN_SIZE, pg.SCALED | pg.FULLSCREEN)
        pg.display.set_caption("Night Terror")
        pg.display.set_icon(pg.image.load("assets/icon.png"))
        self.clock = pg.time.Clock()

        self.caption_font = pg.font.Font("assets/fonts/Zombie.ttf", 24)
        self.button_font = pg.font.Font("assets/fonts/DePixelHalbfett.ttf", 9)
        self.note_font = pg.font.Font("assets/fonts/dogicapixel.ttf", 8)

        pg.mixer.music.load("assets/audio/theme.ogg")
        pg.mixer.music.set_volume(0.5)

        self.done = False
        self.dt: float

        self.restart()

    def run(self):
        while not self.done:
            self.dt = self.clock.tick(60) / 1000

            for event in pg.event.get():
                self.current_state.handle_events(event)
                if event.type == pg.QUIT:
                    self.done = True

            self.screen.fill((21, 18, 37))

            self.current_state.update()
            self.current_state.draw()

            if self.current_state == self.states[States.GAME] and self.current_act > 2:
                for i in range(self.current_state.devil.health):
                    pg.draw.circle(self.screen, (255, 0, 0), eye_positions[i], 1)

            pg.display.flip()

    def restart(self):
        self.states = {
            States.MENU: Menu(self),
            States.GAME: Game(self),
            States.PAUSE: Pause(self),
            States.MIRROR: Mirror(self),
            States.DREAM: Dream(self),
            States.NOTE: Note(self),
        }
        pg.mixer.music.play(-1, fade_ms=1000)
        self.current_state = self.states[States.MENU]
        self.current_act = 1  # Max 5


if __name__ == "__main__":
    App().run()
    pg.quit()
