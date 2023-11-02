import pygame as pg
from src.state_enum import States
from src.states.base import BaseState
from src.utils import import_image
from src.constants import WIN_WIDTH, WIN_HEIGHT, WIN_SIZE


class Note(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.normal_note = import_image("assets/note/note.png")
        self.cursed_note = import_image("assets/note/cursed_note.png")
        self.note_rect = self.normal_note.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

        self.normal_text = self.app.note_font.render(
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
            False,
            (21, 18, 37),
        )
        self.text_rect = self.normal_text.get_rect(
            center=(WIN_WIDTH / 2 - 26, WIN_HEIGHT / 2 + 10)
        )

        self.cursed_text = self.app.note_font.render(
            """
            I am here.\n
            I am here.\n
            I am here.\n
            I am here.\n
            I am here.\n
            I am here.\n
            I am here.\n
            I am here.\n
            I am here.\n
            """,
            False,
            (21, 18, 37),
        )
        self.cursed_text_rect = self.cursed_text.get_rect(
            center=(WIN_WIDTH / 2 - 26, WIN_HEIGHT / 2 + 10)
        )

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.app.current_state = self.app.states[States.GAME]
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == pg.BUTTON_LEFT:
                if not self.note_rect.collidepoint(event.pos):
                    self.app.current_state = self.app.states[States.GAME]

    def draw(self):
        self.app.screen.blit(self.last_frame, (0, 0))
        self.app.screen.blit(self.surface_tint, (0, 0))

        if self.app.current_act < 2:
            self.app.screen.blit(self.normal_note, self.note_rect)
            self.app.screen.blit(self.normal_text, self.text_rect)
        else:
            self.app.screen.blit(self.cursed_note, self.note_rect)
            self.app.screen.blit(self.cursed_text, self.cursed_text_rect)
