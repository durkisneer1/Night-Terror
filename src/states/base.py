import pygame as pg
from src.constants import WIN_SIZE


class BaseState:
    def __init__(self, app):
        self.app = app

        self.surface_tint = pg.Surface(WIN_SIZE)
        self.surface_tint.fill((0, 0, 0))
        self.surface_tint.set_alpha(128)
        self.last_frame = None

    def handle_events(self, event):
        ...

    def update(self):
        ...

    def draw(self):
        ...
