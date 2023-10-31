import pygame as pg


class Tile:
    def __init__(self, pos, image, name):
        self.name = name
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.hovered = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.hovered:
            pg.draw.rect(screen, (255, 255, 0), self.rect, 1)
