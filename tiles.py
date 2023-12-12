import time
from typing import Tuple
import pygame
from block import *
from spritesheet import Spritesheet

class Tiles:
    def __init__(self, window:pygame.Surface, window_size:Tuple[int, int], spritesheet: Spritesheet, tile_size: Tuple[int, int]):
        self.window = window
        self.window_size = window_size
        self.spritesheet = spritesheet
        self.tile_size = tile_size

        self.tiles = []

        self.developer = True
        self.selected_tile = 0
        self.current_tile = 0
        self.change_tile_time = time.time()
        self.generate_tiles()

    
    def loop(self, in_camera_bounds, offset):
        mouse = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for i in range(0, len(self.tiles)):
            tile = self.tiles[i]

            if in_camera_bounds(tile, offset):
                tile.draw(offset)

                if tile.collide_point(mouse, offset):
                    self.selected_tile = i
                    pygame.draw.rect(self.window, (255, 0, 0), (tile.pos[0] + offset[0], tile.pos[1] + offset[1], self.tile_size[0], self.tile_size[1]), 1)

        if self.developer:
            tex = self.spritesheet.image(self.current_tile)
            self.window.blit(tex, (0, 0))

            if mouse_pressed[1] and time.time() - self.change_tile_time > 0.2:
                self.change_tile_time = time.time()
                self.current_tile += 1
                if self.current_tile > 35:
                    self.current_tile = 0
            

            self.add_tiles_mode(mouse_pressed)

    
    def generate_tiles(self):
        for i in range(-self.window_size[0] * 2, self.window_size[0] * 2, self.tile_size[0]):
            for j in range(-self.window_size[1] * 2, self.window_size[1] * 2, self.tile_size[1]):
                self.tiles.append(Rect((i, j), self.tile_size, (0, 0, 0), 'air', self.window))

    
    def add_tiles_mode(self, mouse_press: Tuple[bool, bool, bool]):
        if mouse_press[0]:
            self.tiles[self.selected_tile].set_texture(self.spritesheet.image(self.current_tile))
        elif mouse_press[2]:
            self.tiles[self.selected_tile].rm_texture()
        