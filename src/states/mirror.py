import pygame as pg
from src.state_enum import States
from src.states.base import BaseState


class Mirror(BaseState):
    def __init__(self, app):
        super().__init__(app)

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.app.current_state = self.app.states[States.GAME]

    def draw(self):
        self.app.screen.blit(self.last_frame, (0, 0))
        self.app.screen.blit(self.surface_tint, (0, 0))
