import pygame as pg
from pytmx.util_pygame import load_pygame
from src.state_enum import States
from src.states.base import BaseState
from src.player import Player
from src.utils import load_tmx_layers, load_tmx_objects


class Game(BaseState):
    def __init__(self, app):
        super().__init__(app)

        room_tmx_data = load_pygame("assets/game/room/room.tmx")
        self.layer_tiles = load_tmx_layers(room_tmx_data)
        self.collision_tiles = load_tmx_objects(room_tmx_data, "Obstacle")
        self.interaction_tile = load_tmx_objects(room_tmx_data, "Intractable")
        self.player = Player(self, self.collision_tiles)

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.app.current_state = self.app.states[States.PAUSE]
                self.app.current_state.last_frame = self.app.screen.copy()
            elif event.key == pg.K_e:
                for intractable in self.interaction_tile:
                    if intractable.hovered:
                        if intractable.name == "Mirror":
                            self.app.current_state = self.app.states[States.MIRROR]
                        elif intractable.name == "Bed":
                            self.app.current_state = self.app.states[States.DREAM]
                        elif intractable.name == "Desk":
                            self.app.current_state = self.app.states[States.NOTE]
                        self.app.current_state.last_frame = self.app.screen.copy()

    def update(self):
        self.player.move()

    def draw(self):
        for layer in self.layer_tiles:
            layer.draw(self.app.screen)
        for intractable in self.interaction_tile:
            intractable.hovered = intractable.rect.colliderect(self.player.rect)
            intractable.draw(self.app.screen)

        self.player.draw()

        for collider in self.collision_tiles:
            collider.draw(self.app.screen)
