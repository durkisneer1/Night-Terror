import pygame as pg
from pytmx.util_pygame import load_pygame
from src.state_enum import States
from src.states.base import BaseState
from src.player import Player
from src.utils import load_tmx_layers, load_tmx_objects, import_image
from src.constants import WIN_SIZE
from src.devil import Devil


class Game(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.parents = import_image("assets/game/room/parents.png")

        self.paper_sfx = pg.mixer.Sound("assets/audio/desk/paper.ogg")
        self.paper_sfx.set_volume(0.3)
        self.knife_sfx = pg.mixer.Sound("assets/audio/desk/knife.ogg")
        self.knife_sfx.set_volume(0.35)

        self.swing_sfx = pg.mixer.Sound("assets/audio/knife/swing.ogg")
        self.swing_sfx.set_volume(0.25)
        self.hit_sfx = pg.mixer.Sound("assets/audio/knife/hit.ogg")
        self.hit_sfx.set_volume(0.25)

        self.knife_grabbed = False

        room_tmx_data = load_pygame("assets/game/room/room.tmx")
        self.layer_tiles = load_tmx_layers(room_tmx_data)
        self.collision_tiles = load_tmx_objects(room_tmx_data, "Obstacle")
        self.interaction_tile = load_tmx_objects(room_tmx_data, "Intractable")

        self.player = Player(self, self.collision_tiles)
        self.devil = Devil(self)

        self.desk_cover_positions = ((129, 121), (145, 121))  # Left and right desks
        self.desk_cover_rect = pg.Surface((14, 6))
        self.desk_cover_rect.fill((197, 145, 84))

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

        # Level progression
        self.mirror_done = False
        self.desk_done = False

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.app.current_state = self.app.states[States.PAUSE]
                self.app.current_state.last_frame = self.app.screen.copy()

            elif event.key == pg.K_e:
                if (
                    self.app.current_act > 3
                    and self.devil.health > 0
                    and self.knife_grabbed
                ):
                    self.swing_sfx.play(0)
                    if self.player.rect.colliderect(self.devil.hit_rect):
                        self.hit_sfx.play(0)
                        self.devil.speed = -self.devil.max_speed * 2
                        self.devil.hit()
                    return

                for intractable in self.interaction_tile:
                    if intractable.hovered:
                        if intractable.name == "Mirror":
                            if not self.mirror_done:
                                self.mirror_done = True
                            self.app.current_state = self.app.states[States.MIRROR]
                            self.app.current_state.normal_state = (
                                not self.devil.health > 0
                            )

                        elif intractable.name == "Desk" and (
                            not self.knife_grabbed or not self.devil.health > 0
                        ):
                            if not self.desk_done:
                                self.desk_done = True
                            self.app.current_state = self.app.states[States.NOTE]
                            self.app.current_state.normal_state = (
                                not self.devil.health > 0
                            )
                            if (
                                self.app.current_act < 3
                                or self.app.current_state.normal_state
                            ):
                                self.paper_sfx.play(0)
                            elif self.app.current_act < 4:
                                self.knife_sfx.play(0)
                                self.knife_grabbed = True
                                self.player.anim_states = self.player.knife_anim

                        elif (
                            intractable.name == "Bed"
                            and self.desk_done
                            and self.mirror_done
                        ):
                            if self.app.current_act > 4:
                                self.app.current_state = self.app.states[States.MENU]
                                self.app.restart = True
                                return

                            self.desk_done = False
                            self.mirror_done = False
                            self.app.current_state = self.app.states[States.DREAM]
                            pg.mixer.music.pause()
                            self.app.current_state.sounds[self.app.current_act].play(0)

                        self.app.current_state.last_frame = self.app.screen.copy()

    def update(self):
        self.player.move()
        if self.app.current_act > 3 and self.devil.health > 0:
            self.devil.move()

    def draw(self):
        for layer in self.layer_tiles:
            layer.draw(self.app.screen)
        for intractable in self.interaction_tile:
            intractable.hovered = intractable.rect.colliderect(self.player.rect)
            intractable.draw(self.app.screen)

        if not self.knife_grabbed or not self.devil.health > 0:
            self.app.screen.blit(
                self.desk_cover_rect,
                self.desk_cover_positions[
                    (self.app.current_act < 3 or not self.devil.health > 0)
                ],
            )
        else:
            for pos in self.desk_cover_positions:
                self.app.screen.blit(self.desk_cover_rect, pos)

        if self.app.current_act == 5:
            self.app.screen.blit(self.parents, (232, 127))

        self.player.draw()
        if self.app.current_act > 2 and self.devil.health > 0:
            self.devil.draw()

        for collider in self.collision_tiles:
            collider.draw(self.app.screen)

        if 0 < self.app.current_act < 5:
            self.filter_layer.fill((40,) * 4)

            if self.app.current_act != 4:
                filter_center = self.player.rect.center - self.light_size / 2
                self.filter_layer.blit(
                    self.base_light, filter_center, special_flags=pg.BLEND_RGBA_ADD
                )
            self.app.screen.blit(
                self.filter_layer, (0, 0), special_flags=pg.BLEND_RGBA_MULT
            )
