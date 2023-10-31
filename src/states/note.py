import pygame as pg
from src.state_enum import States
from src.states.base import BaseState
from src.utils import import_image
from src.constants import WIN_WIDTH, WIN_HEIGHT, WIN_SIZE


class Note(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.image = import_image("assets/note/note.png", is_alpha=False)
        self.rect = self.image.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))
        self.text = self.app.note_font.render(
            """
            Your dad and I\n
            are going out\n
            of town. Take\n
            care of the\n
            house while\n
            we're gone.\n
            \n
            Love,\n
            Mom and Dad.
            """,
            False, (0, 0, 0)
        )
        self.text_rect = self.text.get_rect(center=(WIN_WIDTH / 2 - 26, WIN_HEIGHT / 2 + 10))

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.app.current_state = self.app.states[States.GAME]
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == pg.BUTTON_LEFT:
                if not self.rect.collidepoint(event.pos):
                    self.app.current_state = self.app.states[States.GAME]

    def draw(self):
        self.app.screen.blit(self.last_frame, (0, 0))
        self.app.screen.blit(self.surface_tint, (0, 0))

        self.app.screen.blit(self.image, self.rect)
        self.app.screen.blit(self.text, self.text_rect)
