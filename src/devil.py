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
        self.current_frame += self.game.app.dt * self.speed / 10

    def move(self, dest_x):
        if abs(dest_x - self.rect.centerx) < 1:
            return
        self.animate()

        if dest_x > self.rect.centerx:
            self.speed = (
                min(self.speed + self.game.app.dt * 70, self.max_speed)
            )
            self.image = pg.transform.flip(self.image, True, False)
        else:
            self.speed = (
                max(self.speed - self.game.app.dt * 70, -self.max_speed)
            )

        self.pos.x += self.speed * self.game.app.dt
        self.rect.bottomright = self.pos
        self.hit_rect.center = self.rect.center

    def draw(self):
        self.game.app.screen.blit(self.image, self.rect)
