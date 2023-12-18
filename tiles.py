import os
import time
from typing import Tuple
import pygame
from block import *
from spritesheet import WALL_1, Spritesheet
from player import Player

class Tiles:
    map_save_file = "data/map.data"
    def __init__(self, window:pygame.Surface, window_size:Tuple[int, int], spritesheet: Spritesheet, sprite_size: Tuple[int, int]):
        self.window = window
        self.window_size = window_size
        self.spritesheet = spritesheet
        self.sprite_size = sprite_size

        self.tiles = []
        self.walls = []

        self.developer = True
        self.selected_tile = WALL_1
        self.current_tile = WALL_1
        self.change_tile_time = time.time()
        self.generate_tiles()

        if os.path.exists(self.map_save_file):
            self.load_map(self.map_save_file)

    
    def loop(self, in_camera_bounds, player:Player):
        offset = player.offset
        player_mid = player.middle
        self.offset = offset
        mouse = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        draw_array = self.tiles + self.walls

        for i in range(0, len(draw_array)):
            tile = draw_array[i]

            if in_camera_bounds(tile, offset):
                tile_pos = (tile.pos[0] + offset[0], tile.pos[1] + offset[1])
                dist = dist_point(player_mid, tile_pos)

                if dist < 4 * self.sprite_size[0]:
                    tile.draw(offset)
                    alpha = (5 * self.sprite_size[0] - dist) / 10
                    if tile.type == WALL_1:
                        alpha /= 2
                    rect(self.window, tile_pos, tile.size, (255, 255, 255, alpha))
                elif dist < 8 * self.sprite_size[0]:
                    tile.draw(offset)
                    alpha = dist - 4 * self.sprite_size[0]
                    alpha = (5 * alpha) / 3
                    if alpha > 255:
                        alpha = 255
                    rect(self.window, tile_pos, tile.size, (0, 5, 13, alpha))

                if draw_array[i].type == WALL_1:
                    player.collide_rect(tile.rect, offset, True, True)
                

                if tile.collide_point(mouse, offset) and tile.type is not WALL_1:
                    self.selected_tile = i
                    pygame.draw.rect(self.window, (255, 0, 0), (tile.pos[0] + offset[0], tile.pos[1] + offset[1], self.sprite_size[0], self.sprite_size[1]), 1)
        # for wall in self.walls:
        #     if in_camera_bounds(wall, offset):
        #         wall_pos = (wall.pos[0] + offset[0], wall.pos[1] + offset[1])
        #         dist = dist_point(player_mid, wall_pos)

        #         if dist < 4 * self.sprite_size[0]:
        #             wall.draw(offset)
        #             alpha = (5 * self.sprite_size[0] - dist) / 20
        #             rect(self.window, wall_pos, wall.size, (255, 255, 255, alpha))
        #         elif dist < 8 * self.sprite_size[0]:
        #             wall.draw(offset)
        #             alpha = dist - 4 * self.sprite_size[0]
        #             alpha = (5 * alpha) / 3
        #             if alpha > 255:
        #                 alpha = 255
        #             rect(self.window, wall_pos, wall.size, (0, 5, 13, alpha))


        for wall in self.walls:
            if player.collide_rect(wall.rect, offset, True, True):
                return
                
        if self.developer:
            key = pygame.key.get_pressed()
            if time.time() - self.change_tile_time > 0.2:
                if key[pygame.K_RIGHT]:
                    self.change_tile_time = time.time()
                    self.current_tile += 1
                    if self.current_tile > 100:
                        self.current_tile = 0
                    print(self.current_tile)
                if key[pygame.K_LEFT]:
                    self.change_tile_time = time.time()
                    self.current_tile -= 1
                    if self.current_tile < 0:
                        self.current_tile = 99
                    print(self.current_tile)
            

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
            if self.current_tile == WALL_1:
                pos = self.tiles[self.selected_tile].pos
                sprite = self.spritesheet.image(WALL_1)
                sprite = pygame.transform.scale(sprite, (self.sprite_size[0], self.sprite_size[1] * 2))
                wall = Rect(pos, (self.sprite_size[0], self.sprite_size[1] * 2), (0, 0, 0, 0), WALL_1, self.window, sprite)
                
                for w in self.walls:
                    if w.collide_rect(wall.rect):
                        return
                self.walls.append(wall)
                #for wall in self.walls:
                #    dist = dist_block(self.walls[-1].pos, wall)
                #    if dist < self.sprite_size[0] * 3:
                #        self.rotate_wall(wall)
                #print("_" * 10)

            else:
                self.tiles[self.selected_tile].set_type(self.current_tile)
                self.tiles[self.selected_tile].set_texture(self.spritesheet.image(self.current_tile))
        elif mouse_press[2]:
            self.tiles[self.selected_tile].rm_texture()

    
    def rotate_wall(self, wall:Rect):
        pos1 = self.walls[-1].pos
        pos2 = wall.pos
        direction = ""
        angle = 0
        if pos2[1] < pos1[1]:
            direction = "up"
            angle = 90
        elif pos2[1] > pos1[0] + self.sprite_size[0]:
            direction = "right"
        elif pos2[1] > pos1[1] + self.sprite_size[1]:
            direction = "down" 
            angle = 90
        elif pos2[0] < pos1[0]:
            direction = "left"
        print(direction, angle)
        tex = wall.texture
        tex = pygame.transform.rotate(tex, angle)
        wall.set_texture(tex)
        return angle

    
    def save_tilemap(self):
        str_map = ""
    	
        idx = 0
        for tile in self.tiles:
            tile_id = tile.type
            if tile_id is not "air":
                print(tile_id)
                tile_data = f"{tile_id} {idx}|"

                str_map += tile_data
            idx += 1

        for wall in self.walls:
            wall_id = wall.type
            if wall_id is WALL_1:
                wall_data = f"{wall_id} {wall.pos[0]} {wall.pos[1]}|"

                str_map += wall_data
            idx += 1
        
        fout = open("data/map.data", 'w')
        fout.write(str_map)
        fout.close()

    
    def load_map(self, file_name: str):
        fin = open(file_name, 'r').readline()
        data = fin.split('|')    

        for tile in data:
            tile_data = tile.split(' ')    
            if len(tile_data) > 1:
                idx = int(tile_data[1])
                id = int(tile_data[0])
                if id == WALL_1:
                    x = int(tile_data[1])
                    try:
                        y = int(tile_data[2])
                    except IndexError:
                        print(f"{tile_data} failed to load")
                        break
                    sprite = self.spritesheet.image(WALL_1)
                    sprite = pygame.transform.scale(sprite, (self.sprite_size[0], self.sprite_size[1] * 2))
                    self.walls.append(Rect((x, y), (self.sprite_size[0], self.sprite_size[1] * 2), (0, 0, 0, 0), WALL_1, self.window, sprite))
                else:
                    self.tiles[idx].set_type(id)
                    self.tiles[idx].set_texture(self.spritesheet.image(id))