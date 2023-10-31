import pygame as pg
from src.utils import import_folder
from src.constants import WIN_WIDTH, WIN_HEIGHT


class Player:
    def __init__(self, game, collision_tiles):
        self.game = game
        self.collision_tiles = collision_tiles

        self.anim_states = {
            "idle": import_folder("assets/game/player/idle"),
            "walk": import_folder("assets/game/player/walk"),
        }
        self.current_frame = 0
        self.frame_list = self.anim_states["idle"]
        self.image = self.frame_list[self.current_frame]
        self.pos = pg.Vector2(WIN_WIDTH / 2, WIN_HEIGHT / 2)
        self.rect = self.image.get_rect()

        self.velocity = pg.Vector2()
        self.direction = pg.Vector2()
        self.move_speed = 70
        self.anim_speed = 4.5
        self.gravity = 0.6

        self.facing_right = True
        self.on_ground = False

    def animate(self):
        self.current_frame %= len(self.frame_list)
        if self.facing_right:
            self.image = self.frame_list[int(self.current_frame)]
        else:
            self.image = pg.transform.flip(
                self.frame_list[int(self.current_frame)],
                True, False
            )
        self.current_frame += self.anim_speed * self.game.app.dt

    def move(self):
        if self.on_ground:
            if self.game.app.keys[pg.K_SPACE]:
                self.velocity.y = -0.15
                self.on_ground = False
        else:
            self.velocity.y += self.gravity * self.game.app.dt

        self.direction.xy = (0, 0)
        if self.game.app.keys[pg.K_a]:
            self.direction.x = -1
        if self.game.app.keys[pg.K_d]:
            self.direction.x = 1

        if self.direction:
            self.direction.normalize_ip()
            if self.direction.x > 0:
                self.facing_right = True
            elif self.direction.x < 0:
                self.facing_right = False
            self.frame_list = self.anim_states["walk"]
        else:
            self.frame_list = self.anim_states["idle"]
        self.velocity.x = self.direction.x * self.move_speed * self.game.app.dt

        self.pos.x += self.velocity.x
        self.rect.x = self.pos.x
        self.h_collision()
        self.pos.y += self.velocity.y
        self.rect.y = self.pos.y
        self.v_collision()

    def h_collision(self):
        for tile in self.collision_tiles:
            if self.rect.colliderect(tile.rect):
                if self.velocity.x > 0:
                    self.rect.right = tile.rect.left
                if self.velocity.x < 0:
                    self.rect.left = tile.rect.right
                self.pos.x = self.rect.x

    def v_collision(self):
        for tile in self.collision_tiles:
            if self.rect.colliderect(tile.rect):
                if self.velocity.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.on_ground = True
                if self.velocity.y < 0:
                    self.rect.top = tile.rect.bottom
                self.pos.y = self.rect.y

    def draw(self):
        self.animate()
        self.game.app.screen.blit(self.image, self.pos)
