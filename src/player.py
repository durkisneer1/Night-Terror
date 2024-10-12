from enum import IntEnum, auto
import pygame as pg
from src.utils import import_folder


class Axis(IntEnum):
    X = auto()
    Y = auto()


class Player:
    def __init__(self, game, collision_tiles):
        self.game = game
        self.collision_tiles = collision_tiles

        self.steps_sfx = [
            pg.mixer.Sound(f"assets/audio/walk/{i}.ogg") for i in range(5)
        ]
        [sfx.set_volume(0.25) for sfx in self.steps_sfx]
        self.sound_index = 0
        self.max_step_tick = 0.5
        self.step_tick = self.max_step_tick

        self.knife_anim = {
            "idle": import_folder("assets/game/player/idle_knife"),
            "walk": import_folder("assets/game/player/walk_knife"),
        }
        self.torch_anim = {
            "idle": import_folder("assets/game/player/idle"),
            "walk": import_folder("assets/game/player/walk"),
        }
        self.anim_states = self.torch_anim
        self.current_frame = 0
        self.frame_list = self.anim_states["idle"]
        self.image = self.frame_list[self.current_frame]
        self.pos = pg.Vector2(48, 120)
        self.rect = self.image.get_rect()

        self.velocity = pg.Vector2(0)
        self.x_direction = 0
        self.move_speed = 45
        self.anim_speed = 5
        self.gravity = 980

        self.facing_right = True
        self.on_ground = False

    def animate(self):
        self.current_frame %= len(self.frame_list)
        if self.facing_right:
            self.image = self.frame_list[int(self.current_frame)]
        else:
            self.image = pg.transform.flip(
                self.frame_list[int(self.current_frame)], True, False
            )
        self.current_frame += self.anim_speed * self.game.app.dt

    def move(self):
        keys = pg.key.get_pressed()

        self.step_tick = min(self.step_tick + self.game.app.dt, self.max_step_tick)
        if self.on_ground:
            if keys[pg.K_SPACE] or keys[pg.K_UP]:
                self.velocity.y = -200
                self.on_ground = False
        else:
            self.velocity.y += self.gravity * self.game.app.dt

        self.x_direction = 0
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.x_direction -= 1
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.x_direction += 1

        if self.x_direction:
            self.frame_list = self.anim_states["walk"]

            if self.x_direction > 0:
                self.facing_right = True
            elif self.x_direction < 0:
                self.facing_right = False

            if self.step_tick == self.max_step_tick:
                self.steps_sfx[self.sound_index].play()
                self.sound_index = (self.sound_index + 1) % 5
                self.step_tick = 0
        else:
            self.frame_list = self.anim_states["idle"]
        self.velocity.x = self.x_direction * self.move_speed

        self.pos.x += self.velocity.x * self.game.app.dt
        self.rect.x = self.pos.x
        self.handle_collision(Axis.X)
        self.pos.y += self.velocity.y * self.game.app.dt
        self.rect.y = self.pos.y
        self.handle_collision(Axis.Y)

    def handle_collision(self, axis: Axis):
        for tile in self.collision_tiles:
            if self.rect.colliderect(tile.rect):
                if axis == Axis.X:
                    if self.velocity.x > 0:
                        self.rect.right = tile.rect.left
                    elif self.velocity.x < 0:
                        self.rect.left = tile.rect.right
                    self.pos.x = self.rect.x
                elif axis == Axis.Y:
                    if self.velocity.y > 0:
                        self.rect.bottom = tile.rect.top
                        self.on_ground = True
                    elif self.velocity.y < 0:
                        self.rect.top = tile.rect.bottom
                    self.velocity.y = 0
                    self.pos.y = self.rect.y
                break

    def draw(self):
        self.animate()
        self.game.app.screen.blit(self.image, self.pos)
