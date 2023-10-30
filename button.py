import pygame as pg


class Button:
    def __init__(self, app, font, text, color, pos):
        self.app = app
        self.surf = font.render(text, False, color)
        self.shadow = font.render(text, False, (0, 0, 0))
        self.rect = self.surf.get_rect(center=pos)
        self.hovered = False

    def input(self):
        self.hovered = self.rect.collidepoint(self.app.mouse_pos)
        return self.hovered and self.app.mouse_input[0]

    def draw(self):
        self.app.screen.blit(self.shadow, self.rect.move(2, 2))
        if self.hovered:
            pg.draw.rect(self.app.screen, (255, 255, 140), self.rect, 1)
        self.app.screen.blit(self.surf, self.rect)
