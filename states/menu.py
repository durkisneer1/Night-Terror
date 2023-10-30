import pygame as pg
from utils import import_folder
from constants import *
from button import Button
from state_enum import States
from states.base import BaseState


class Menu(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.anim = import_folder("assets/menu")
        self.anim.reverse()
        self.rot_anim = []
        self.pivot = (WIN_SIZE[0] // 2, WIN_SIZE[1] // 2)
        self.angle = 0

        self.title = Button(
            self.app, self.app.caption_font, "INTO THE PIT", (255, 40, 10), (WIN_SIZE[0] // 2, 50)
        )
        self.play_button = Button(
            self.app, self.app.text_font, "PLAY", (255, 255, 255), (WIN_SIZE[0] // 2, 145)
        )

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.app.done = True

    def update(self):
        self.angle = (self.angle + self.app.dt * 14) % 360
        self.rot_anim = [
            pg.transform.rotate(image, self.angle if index % 2 else -self.angle)
            for index, image
            in enumerate(self.anim)
        ]

    def draw(self):
        self.app.screen.fill((255, 255, 255))
        for image in self.rot_anim:
            rect = image.get_rect(center=self.pivot)
            self.app.screen.blit(image, rect)

        self.title.draw()

        if self.play_button.input():
            self.app.current_state = self.app.states[States.GAME]
        self.play_button.draw()
