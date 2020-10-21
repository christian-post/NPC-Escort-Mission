import pygame as pg
import os

import settings as st


def images_from_strip(strip, number):
    img_w = strip.get_width() // number
    img_h = strip.get_height()

    images = []
    for i in range(number):
        s = strip.subsurface((i * img_w, 0, img_w, img_h))
        images.append(s)

    return images


class Loader:
    def __init__(self, game):
        self.game = game
        base_dir = game.base_dir
        self.graphics_folder = os.path.join(base_dir, 'assets', 'graphics')
        self.sounds_folder = os.path.join(base_dir, 'assets', 'sounds')
        self.sprite_folder = os.path.join(self.graphics_folder, 'sprites')
        self.tileset_folder = os.path.join(self.graphics_folder, 'tilesets')
        self.gui_image_folder = os.path.join(self.graphics_folder, 'GUI')
        self.font_folder = os.path.join(base_dir, 'assets', 'fonts')
            
        self.channel = None
        
        # TODO: dict comprehension?
        self.fonts = {
                'slkscr': os.path.join(self.font_folder, 'slkscr.ttf')
                }

        # sound libs stored as (filename, relative volume)
        self.music_lib = {}
        self.sfx_lib = {}
        
        
    def load_graphics(self):
        """load sprite image strips here"""
        files = os.listdir(self.sprite_folder)
        img_files = [os.path.join(self.sprite_folder, f)
                     for f in files if f[-3:] == 'png']

        knight_imgs = sorted(list(filter(lambda x: 'knight' in x, img_files)))
        elf_imgs = sorted(list(filter(lambda x: 'elf' in x, img_files)))
        tileset_img = os.path.join(self.tileset_folder,
                                   '0x72_DungeonTilesetII_v1.3.png')

        gfx_lib = {
                'knight': [pg.image.load(im).convert_alpha()
                           for im in knight_imgs],
                'elf': [pg.image.load(im).convert_alpha() for im in elf_imgs],
                'tileset0': pg.image.load(tileset_img).convert_alpha()
                }
        
        return gfx_lib
    
    
    def load_sounds(self):
        pg.mixer.init()
        
        music_files = []
        sfx_files = []

        music_objects = [os.path.join(self.sounds_folder, 'bgm', f)
                         for f in music_files]     
        sfx_objects = [pg.mixer.Sound(os.path.join(self.sounds_folder,
                                                   'sfx', f))
                       for f in sfx_files]

        
        
    def play_music(self, key, loop=True):
        if loop:
            loops = -1
        else:
            loops = 0
        pg.mixer.music.load(self.music_lib[key][0])
        pg.mixer.music.play(loops)
        volume = st.MUSIC_VOLUME * self.music_lib[key][1]
        pg.mixer.music.set_volume(volume)
        
          
    def play_sound(self, key):
        sound = self.sfx_lib[key][0]
        volume = st.SFX_VOLUME * self.sfx_lib[key][1]
        sound.set_volume(volume)
        # play the sound if it isn't already being played
        if self.channel is None:
            self.channel = sound.play()
        else:
            if self.channel.get_sound() == sound:
                if not self.channel.get_busy():
                    self.channel = sound.play()
            else:
                self.channel = sound.play()
