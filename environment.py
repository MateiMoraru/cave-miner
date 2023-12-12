import math
import pygame
from block import Rect
from spritesheet import *
from player import Player
import random

from tiles import Tiles

class Environment:
    def __init__(self, window:pygame.Surface, window_size:tuple, spritesheet:Spritesheet, tiles:Spritesheet, font:pygame.Font):
        self.window = window
        self.window_size = window_size
        self.spritesheet = spritesheet
        self.tiles_spritesheet = tiles
        self.sprite_size = (64, 64)
        self.font = font
        self.player = Player(self.window, (self.window_size[0] / 2, self.window_size[1] / 2), self.spritesheet.image(PLAYER), spritesheet)
        self.light_sources = []
        
        self.tiles = Tiles(self.window, self.window_size, self.tiles_spritesheet, self.sprite_size)
    
    def loop(self):
        self.player.loop()


    def draw(self):
        self.tiles.loop(self.in_camera_bounds, self.player.offset)
        self.player.draw()
    
    def in_camera_bounds(self, rect:Rect, rect_offset:tuple=(0, 0)):
        pos = [rect.pos[0] + rect_offset[0], rect.pos[1] + rect_offset[1]]

        in_bounds = pos[0] > -self.sprite_size[0] and pos[0] < self.window_size[0] + self.sprite_size[0] * 2# and pos[1] > -self.sprite_size[1] * 5 and pos[1] < self.window_size[1] + 5 * self.sprite_size[1]
        return in_bounds
        
    
    def dist_Rect(self, point:tuple, rect:Rect):
        dx = abs(point[0] - (rect.rect.x + rect.rect.w / 2)) ** 2
        dy = abs(point[1] - (rect.rect.y + rect.rect.h / 2)) ** 2

        return math.sqrt(dx + dy) 
    
    
    def dist_point(self, point:tuple, point2:tuple):
        dx = abs(point[0] - point2[0]) ** 2
        dy = abs(point[1] - point2[1]) ** 2

        return math.sqrt(dx + dy) 