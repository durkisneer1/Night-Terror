import pygame as pg
from src.state_enum import States
from src.states.base import BaseState


class Dream(BaseState):
    def __init__(self, app):
        super().__init__(app)

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.app.current_state = self.app.states[States.GAME]
