from os import walk
import numpy as np
import pygame as pg
from src.tile import Tile
import inspect
import os

debugging = False  # Set to True for logs

image_load = pg.image.load
pg_surface = pg.Surface
pg_mixer_sound = pg.mixer.Sound

MAP_OFFSET = pg.Vector2(32, 24)


def import_folder(
    path: str,
    is_alpha: bool = True,
    scale: float = 1,
    highlight: bool = False,
    blur: bool = False,
) -> list[pg.Surface]:
    surf_list = []
    for _, __, img_file in walk(path):
        for image in img_file:
            full_path = path + "/" + image
            surface = import_image(full_path, is_alpha, scale, highlight, blur)
            surf_list.append(surface)
    return surf_list


def import_image(
    path: str,
    is_alpha: bool = True,
    scale: float = 1,
    highlight: bool = False,
    blur: bool = False,
) -> pg.Surface:
    image_surf = (
        pg.image.load(path).convert_alpha()
        if is_alpha
        else pg.image.load(path).convert()
    )

    if scale != 1 and scale > 0:
        image_surf = pg.transform.scale_by(image_surf, scale)
    if highlight:
        image_surf.fill((40, 40, 40, 0), special_flags=pg.BLEND_RGB_ADD)
    if blur:
        template_surf = pg.Surface(
            (image_surf.get_width() + 20, image_surf.get_height() + 20), pg.SRCALPHA
        )
        template_surf.fill((0, 0, 0, 0))
        image_rect = image_surf.get_rect(
            center=(template_surf.get_width() / 2, template_surf.get_height() / 2)
        )
        template_surf.blit(image_surf, image_rect)
        image_surf = pg.transform.gaussian_blur(template_surf, 5)

    return image_surf


def load_tmx_layers(data) -> list[Tile]:
    tiles = []
    for layer in data.visible_layers:
        if hasattr(layer, "data"):
            for x, y, surface in layer.tiles():
                pos = (x * 16, y * 16) + MAP_OFFSET
                tiles.append(Tile(pos, surface, layer.name))
    return tiles


def load_tmx_objects(data, tile_type) -> list[Tile]:
    tiles = []
    for obj in data.objects:
        if obj.type == tile_type:
            pos = (obj.x, obj.y) + MAP_OFFSET
            if obj.image:
                tiles.append(Tile(pos, obj.image, obj.name))
    return tiles


def generate_static(size: tuple | pg.Vector2) -> pg.Surface:
    array = np.random.randint(0, 255, (size[0], size[1], 3)).astype(np.uint8)
    surface = pg.surfarray.make_surface(array)
    return surface


def new_image_load(*args, **kwargs):
    if debugging:
        print("Image loaded:", args[0])
    return image_load(*args, **kwargs)


def new_surface(*args, **kwargs):
    if debugging:
        calling_file = inspect.currentframe().f_back.f_globals["__file__"]
        calling_file = os.path.basename(calling_file)
        print(f"Surface created in {calling_file}")
    return pg_surface(*args, **kwargs)


def new_mixer_sound(*args, **kwargs):
    if debugging:
        print("Sound loaded:", args[0])
    return pg_mixer_sound(*args, **kwargs)


pg.image.load = new_image_load
pg.Surface = new_surface
pg.mixer.Sound = new_mixer_sound
