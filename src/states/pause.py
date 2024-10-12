import pygame as pg
from src.state_enum import States
from src.states.base import BaseState
from src.constants import WIN_WIDTH
from src.button import Button


class Pause(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.title = Button(
            self.app,
            self.app.caption_font,
            "PAUSE",
            (255, 40, 10),
            (WIN_WIDTH // 2, 50),
        )
        self.resume_button = Button(
            self.app,
            self.app.button_font,
            "RESUME",
            (255, 255, 255),
            (WIN_WIDTH // 3, 125),
        )
        self.menu_button = Button(
            self.app,
            self.app.button_font,
            "MENU",
            (255, 255, 255),
            (WIN_WIDTH * 2 // 3, 125),
        )

    def handle_events(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.app.current_state = self.app.states[States.GAME]

    def draw(self):
        self.app.screen.blit(self.last_frame)
        self.app.screen.blit(self.surface_tint)
        self.title.draw()

        if self.resume_button.input():
            self.app.current_state = self.app.states[States.GAME]
        self.resume_button.draw()

        if self.menu_button.input():
            self.app.restart()
        self.menu_button.draw()
