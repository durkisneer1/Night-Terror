import pygame as pg
from src.utils import import_folder


class Devil:
    def __init__(self, game):
        self.game = game
        self.anim = import_folder("assets/game/devil/anim", scale=1.5)
        self.pos = pg.Vector2(272, 136)
        self.rect = self.anim[0].get_rect(bottomright=self.pos)
        self.hit_rect = self.rect.inflate(8, 8)

        self.current_frame = 0
        self.image = self.anim[self.current_frame]

        self.max_speed = 20
        self.speed = 0
        self.health = 26

    def hit(self):
        self.health -= 2
        if self.health <= 0:
            pg.mixer.music.stop()

    def animate(self):
        self.current_frame %= len(self.anim)
        self.image = self.anim[int(self.current_frame)]
        self.current_frame += 2 * self.game.app.dt

    def move(self, dest_x):
        self.speed = min(self.speed + self.game.app.dt * 70, self.max_speed) * self.game.app.dt
        self.pos.x += self.speed * (-1 if dest_x < self.pos.x else 1)
        self.rect.bottomright = self.pos
        self.hit_rect.center = self.rect.center

        self.animate()

    def draw(self):
        self.game.app.screen.blit(self.image, self.rect)
