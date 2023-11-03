import pygame as pg
from src.utils import import_folder
from src.constants import WIN_WIDTH, WIN_HEIGHT
from src.button import Button
from src.state_enum import States
from src.states.base import BaseState


class Menu(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.anim = import_folder("assets/menu")
        self.anim.reverse()
        self.rot_anim = []
        self.pivot = (WIN_WIDTH // 2, WIN_HEIGHT // 2)
        self.last_angle = 0
        self.angle = 0

        self.title = Button(
            self.app,
            self.app.caption_font,
            "NIGHT TERROR",
            (255, 40, 10),
            (WIN_WIDTH / 2, 50),
        )
        self.play_button = Button(
            self.app,
            self.app.button_font,
            "PLAY",
            (255, 255, 255),
            (WIN_WIDTH / 3, 145),
        )
        self.quit_button = Button(
            self.app,
            self.app.button_font,
            "QUIT",
            (255, 255, 255),
            (WIN_WIDTH * 2 / 3, 145),
        )

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.app.done = True

    def update(self):
        self.angle = (self.angle + self.app.dt * 14) % 360
        if (
            self.angle - self.last_angle > 0.1
        ):  # lazy way to prevent unnecessary rotation
            self.rot_anim = [
                pg.transform.rotate(image, self.angle if index % 2 else -self.angle)
                for index, image in enumerate(self.anim)
            ]
            self.last_angle = self.angle

    def draw(self):
        self.app.screen.fill((255, 255, 255))
        for image in self.rot_anim:
            rect = image.get_rect(center=self.pivot)
            self.app.screen.blit(image, rect)

        self.title.draw()

        if self.play_button.input():
            self.app.current_state = self.app.states[States.GAME]
        self.play_button.draw()

        if self.quit_button.input():
            self.app.done = True
        self.quit_button.draw()
