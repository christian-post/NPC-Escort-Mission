import pygame as pg
from pytmx import TiledTileLayer, TiledObjectGroup
from pytmx.util_pygame import load_pygame
import inspect

import sprites as spr

vec = pg.math.Vector2


class Map():
    def __init__(self, game, filename):
        self.game = game
        self.filename = filename
        
        # load map data
        self.tiled_map = load_pygame(self.filename)
        self.tilesize = vec(self.tiled_map.tilewidth, self.tiled_map.tileheight)
        self.size = vec(self.tiled_map.width * self.tilesize.x, 
                        self.tiled_map.height * self.tilesize.y)
        self.background_color = self.tiled_map.background_color
        self.layers = {}
        self.max_layer = 0
        self.rect = None
        
    
    def create_map(self):
        """ectracts tileset and object data from a tmx file"""
        # loop through all available layers
        for layer in self.tiled_map:
            if layer.properties.get('layer'):
                self.max_layer = max(self.max_layer,
                                     layer.properties.get('layer'))
            if isinstance(layer, TiledTileLayer) and layer.visible:
                bg_layer_img = pg.Surface(self.size).convert_alpha()
                # fill with transparent color
                bg_layer_img.fill((0, 0, 0, 0))
                self.rect = bg_layer_img.get_rect()
                # if layer is tileset data, blit the tile image
                # to the corresponding position on the map image
                for x, y, image in layer.tiles():
                    bg_layer_img.blit(image, (x * self.tilesize.x, 
                                              y * self.tilesize.y))
                self.layers[layer.properties.get('layer')] = bg_layer_img
            elif isinstance(layer, TiledObjectGroup) and layer.visible:
                # if layer is an object layer, fetch the corresponding sprite
                # from the sprites.py (spr) module
                sprites = dict(inspect.getmembers(spr, inspect.isclass))
                for obj in layer:
                    if obj.name in sprites:
                        # check if the sprite exists in sprites.py
                        # if so, instantiate the sprite
                        s = sprites[obj.name](self.game, obj.__dict__)
                        s.draw_layer = layer.properties.get('layer')
                    else:
                        print(f'No sprite "{obj.name}" found in sprites module')


