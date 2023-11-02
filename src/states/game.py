import pygame as pg
from pytmx.util_pygame import load_pygame
from src.state_enum import States
from src.states.base import BaseState
from src.player import Player
from src.utils import load_tmx_layers, load_tmx_objects
from src.constants import WIN_SIZE


class Game(BaseState):
    def __init__(self, app):
        super().__init__(app)

        room_tmx_data = load_pygame("assets/game/room/room.tmx")
        self.layer_tiles = load_tmx_layers(room_tmx_data)
        self.collision_tiles = load_tmx_objects(room_tmx_data, "Obstacle")
        self.interaction_tile = load_tmx_objects(room_tmx_data, "Intractable")
        self.player = Player(self, self.collision_tiles)

        # Candlelight
        self.filter_layer = pg.Surface(WIN_SIZE, pg.SRCALPHA)
        self.base_light = pg.Surface(WIN_SIZE, pg.SRCALPHA)
        self.light_color = (255, 229, 125, 0)
        self.light_size = pg.Vector2(128)

        for i in range(1, 256):
            circle = pg.Surface(self.light_size, pg.SRCALPHA)
            pg.draw.circle(circle, (1, 1, 1, 1), self.light_size / 2, i / 4)
            self.base_light.blit(circle, (0, 0), special_flags=pg.BLEND_RGBA_ADD)
        self.base_light.fill(self.light_color, special_flags=pg.BLEND_RGBA_MULT)

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
                            pg.mixer.music.pause()
                            self.app.current_state.sounds[self.app.current_act].play(0)
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

        self.filter_layer.fill((40,)*4)
        filter_center = self.player.rect.center - self.light_size / 2
        self.filter_layer.blit(self.base_light, filter_center, special_flags=pg.BLEND_RGBA_ADD)
        self.app.screen.blit(self.filter_layer, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
