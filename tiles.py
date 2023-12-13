import time
from typing import Tuple
import pygame
from block import *
from spritesheet import Spritesheet

class Tiles:
    def __init__(self, window:pygame.Surface, window_size:Tuple[int, int], spritesheet: Spritesheet, sprite_size: Tuple[int, int]):
        self.window = window
        self.window_size = window_size
        self.spritesheet = spritesheet
        self.sprite_size = sprite_size

        self.tiles = []

        self.developer = True
        self.selected_tile = 0
        self.current_tile = 0
        self.change_tile_time = time.time()
        self.generate_tiles()

    
    def loop(self, in_camera_bounds, offset, player_mid):
        mouse = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for i in range(0, len(self.tiles)):
            tile = self.tiles[i]

            if in_camera_bounds(tile, offset):
                tile_pos = (tile.pos[0] + offset[0], tile.pos[1] + offset[1])
                dist = dist_point(player_mid, tile_pos)

                if dist < 4 * self.sprite_size[0]:
                    tile.draw(offset)
                    alpha = (5 * self.sprite_size[0] - dist) / 10
                    rect(self.window, tile_pos, tile.size, (255, 255, 255, alpha))
                elif dist < 7 * self.sprite_size[0]:
                    tile.draw(offset)
                    alpha = dist - 4 * self.sprite_size[0]
                    alpha = (5 * alpha) / 5
                    if alpha > 255:
                        alpha = 255
                    rect(self.window, tile_pos, tile.size, (0, 5, 13, alpha))
                

                if tile.collide_point(mouse, offset):
                    self.selected_tile = i
                    pygame.draw.rect(self.window, (255, 0, 0), (tile.pos[0] + offset[0], tile.pos[1] + offset[1], self.sprite_size[0], self.sprite_size[1]), 1)

        if self.developer:
            

            if mouse_pressed[1] and time.time() - self.change_tile_time > 0.2:
                self.change_tile_time = time.time()
                self.current_tile += 1
                if self.current_tile > 35:
                    self.current_tile = 0
            

            self.add_tiles_mode(mouse_pressed)

    
    def generate_tiles(self):
        for i in range(-self.window_size[0] * 2, self.window_size[0] * 2, int(self.sprite_size[0])):
            for j in range(-self.window_size[1] * 2, self.window_size[1] * 2, int(self.sprite_size[1])):
                self.tiles.append(Rect((i, j), self.sprite_size, (0, 0, 0), 'air', self.window))

    
    def add_tiles_mode(self, mouse_press: Tuple[bool, bool, bool]):
        tex = self.spritesheet.image(self.current_tile)
        tex = pygame.transform.scale(tex, self.sprite_size)
        self.window.blit(tex, (0, 0))
        if mouse_press[0]:
            self.tiles[self.selected_tile].set_texture(self.spritesheet.image(self.current_tile))
        elif mouse_press[2]:
            self.tiles[self.selected_tile].rm_texture()

    
    def save_tilemap(self):
        str_map = ""

        for tile in self.tiles:
            tile_id = tile.type

            str_map += tile_id
        
        fout = open("data/map.data", 'r')
        fout.write(str_map)
        fout.close()
        