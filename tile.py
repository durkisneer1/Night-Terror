import pygame as pg


class Tile:
    def __init__(self, game, label, pos):
        self.game = game
        self.label = label
        self.pos = pg.Vector2(pos)
        self.rect = pg.Rect(self.pos, (16, 16))

    def draw(self, texture):
        self.game.app.screen.blit(texture, self.pos + self.game.map_offset)
