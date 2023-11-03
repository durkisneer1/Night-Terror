import pygame as pg
from src.state_enum import States
from src.states.base import BaseState
from src.constants import WIN_SIZE, WIN_WIDTH, WIN_HEIGHT
from math import sin, radians
from src.utils import generate_static, import_image
from random import randint


class Dream(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.vignette = import_image("assets/menu/0.png")
        self.rot_vignette = self.vignette.copy()

        self.base = pg.Surface(WIN_SIZE, pg.SRCALPHA)
        self.base.fill((21, 18, 37, 0))
        self.angle = 0
        self.opacity_offset = 0
        self.circle_tick = 0

        self.static_anim = [generate_static(WIN_SIZE) for _ in range(20)]
        self.static_anim = [pg.transform.grayscale(frame) for frame in self.static_anim]
        [frame.set_alpha(8) for frame in self.static_anim]
        self.frame_index = 0
        self.current_frame = self.static_anim[self.frame_index]

        self.sounds = (
            pg.mixer.Sound("assets/audio/dream/first.ogg"),
            pg.mixer.Sound("assets/audio/dream/second.ogg"),
            pg.mixer.Sound("assets/audio/dream/third.ogg"),
            pg.mixer.Sound("assets/audio/dream/fourth.ogg"),
            pg.mixer.Sound("assets/audio/dream/fifth.ogg"),
        )

    def update(self):
        self.frame_index = (self.frame_index + self.app.dt * 10) % len(self.static_anim)
        self.current_frame = self.static_anim[int(self.frame_index)]

        self.angle = (self.angle + self.app.dt * 50) % 360
        unit_y = sin(radians(self.angle))
        self.opacity_offset = (unit_y / 2 + 0.25) * 255
        self.rot_vignette = pg.transform.rotate(self.vignette, unit_y * 180)

        self.circle_tick += self.app.dt * 100

        if self.sounds[self.app.current_act].get_num_channels() == 0:
            self.app.current_state = self.app.states[States.GAME]
            self.app.current_act += 1
            if self.app.current_act < 5:
                pg.mixer.music.play(-1, fade_ms=500)

    def draw(self):
        if 0 < self.app.current_act < 4 and self.circle_tick > 1:
            rand_x = randint(0, WIN_WIDTH)
            rand_y = randint(0, WIN_HEIGHT)
            pg.draw.circle(
                self.app.screen,
                (255, 0, 0),
                (rand_x, rand_y),
                randint(1, 3),
            )
            self.circle_tick = 0

        rect = self.rot_vignette.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))
        self.app.screen.blit(self.rot_vignette, rect)
        self.app.screen.blit(self.current_frame, (0, 0))

        for i in range(1, 256, 8):
            pg.draw.circle(
                self.base,
                (32, 27, 56, min(max(0, int(i - self.opacity_offset)), 255)),
                (WIN_WIDTH / 2, WIN_HEIGHT / 2),
                128 - i // 2,
            )
        self.app.screen.blit(self.base, (0, 0))
