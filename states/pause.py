import pygame as pg
from src.state_enum import States
from states.base import BaseState
from src.constants import *
from src.button import Button


class Pause(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.surface_tint = pg.Surface(WIN_SIZE)
        self.surface_tint.fill((0, 0, 0))
        self.surface_tint.set_alpha(128)
        self.last_frame = None

        self.title = Button(
            self.app, self.app.caption_font, "PAUSE", (255, 40, 10), (WIN_SIZE[0] // 2, 50)
        )
        self.resume_button = Button(
            self.app, self.app.text_font, "RESUME", (255, 255, 255), (WIN_SIZE[0] // 3, 125)
        )
        self.menu_button = Button(
            self.app, self.app.text_font, "MENU", (255, 255, 255), (WIN_SIZE[0] * 2 // 3, 125)
        )

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.app.current_state = self.app.states[States.GAME]

    def update(self):
        pass

    def draw(self):
        self.app.screen.blit(self.last_frame, (0, 0))
        self.app.screen.blit(self.surface_tint, (0, 0))
        self.title.draw()

        if self.resume_button.input():
            self.app.current_state = self.app.states[States.GAME]
        self.resume_button.draw()

        if self.menu_button.input():
            self.app.current_state = self.app.states[States.MENU]
        self.menu_button.draw()
