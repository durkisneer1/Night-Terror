import pygame as pg
from state_enum import States
from states.base import BaseState
from player import Player
from tile import Tile
from constants import *


class Game(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.tiles = [Tile(self, "test", (0, 0))]
        self.tile_surf = pg.Surface((16, 16))
        self.tile_surf.fill((255, 255, 255))
        self.player = Player(self, self.tiles)
        self.map_center = pg.Vector2(WIN_WIDTH / 2, WIN_HEIGHT / 2)
        self.map_offset = self.map_center - self.player.pos

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.app.current_state = self.app.states[States.PAUSE]
                self.app.current_state.last_frame = self.app.screen.copy()

    def update(self):
        self.player.move()
        self.map_offset = self.map_center - self.player.pos

    def draw(self):
        self.player.draw()
        for tile in self.tiles:
            tile.draw(self.tile_surf)
