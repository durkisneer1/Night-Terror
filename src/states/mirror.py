import pygame as pg
from src.state_enum import States
from src.states.base import BaseState
from src.utils import import_image, generate_static
from src.constants import WIN_WIDTH, WIN_HEIGHT


class Mirror(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.mirror_image = import_image("assets/mirror/frame.png", scale=2)
        self.mirror_rect = self.mirror_image.get_rect(
            center=(WIN_WIDTH / 2, WIN_HEIGHT / 2)
        )

        self.normal_face = import_image("assets/mirror/normal.png", scale=2)
        self.blurred_normal_face = import_image("assets/mirror/normal.png", scale=2, blur=True)
        self.distorted_face = import_image("assets/mirror/distorted.png", scale=2)
        self.blurred_distorted_face = import_image("assets/mirror/distorted.png", scale=2, blur=True)

        self.face_rect = self.normal_face.get_rect(
            center=(WIN_WIDTH / 2, WIN_HEIGHT / 2)
        )
        self.blur_rect = self.blurred_normal_face.get_rect(
            center=(WIN_WIDTH / 2, WIN_HEIGHT / 2)
        )

        self.static_anim = [
            generate_static(self.mirror_image.get_size()) for i in range(20)
        ]
        self.static_anim = [pg.transform.grayscale(frame) for frame in self.static_anim]
        [frame.set_alpha(30) for frame in self.static_anim]
        self.frame_index = 0
        self.current_frame = self.static_anim[self.frame_index]

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.app.current_state = self.app.states[States.GAME]
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == pg.BUTTON_LEFT:
                if not self.mirror_rect.collidepoint(event.pos):
                    self.app.current_state = self.app.states[States.GAME]

    def update(self):
        self.frame_index = (self.frame_index + self.app.dt * 10) % len(self.static_anim)
        self.current_frame = self.static_anim[int(self.frame_index)]

    def draw(self):
        self.app.screen.blit(self.last_frame, (0, 0))
        self.app.screen.blit(self.surface_tint, (0, 0))

        pg.draw.rect(self.app.screen, (20, 20, 20), self.mirror_rect)
        self.app.screen.blit(self.current_frame, self.mirror_rect)
        self.app.screen.blit(self.mirror_image, self.mirror_rect)

        if self.app.current_act > 2:
            self.app.screen.blit(self.blurred_distorted_face, self.blur_rect)
            self.app.screen.blit(self.distorted_face, self.face_rect)

            pg.draw.rect(self.app.screen, (255, 0, 0), (120, 61, 2, 2))
            pg.draw.rect(self.app.screen, (255, 0, 0), (134, 61, 2, 2))
            pg.draw.rect(self.app.screen, (255, 0, 0), (180, 31, 2, 2))
            pg.draw.rect(self.app.screen, (255, 0, 0), (197, 31, 2, 2))
        else:
            self.app.screen.blit(self.blurred_normal_face, self.blur_rect)
            self.app.screen.blit(self.normal_face, self.face_rect)
