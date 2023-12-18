import time
import pygame
from spritesheet import WALL_1, Spritesheet
from typing import Tuple, List
from block import Rect

class Entity:
    def __init__(self, window:pygame.Surface, pos:List[float], size:List[float], color:Tuple[int]=(255, 0, 255), sprite_id:int=None, spritesheet:Spritesheet=None, speed:int=3):
        self.window = window
        self.pos = [pos[0] - size[0] / 2, pos[1] - size[1] / 2]
        self.size = size
        self.color = color
        self.sprite_id = sprite_id
        self.spritesheet = spritesheet

        if sprite_id is not None:
            self.load_player_sprite()
        
        self.speed = speed
        self.walking = False
        self.direction = None
        self.default_sprite_id = sprite_id
        self.animation_time = time.time()

        self.middle = (self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.init_colliders()
        self.collided = None


    def init_colliders(self):
        self.colliders = []
        self.collider_up = Rect((self.pos[0] + 15, self.pos[1]), (self.size[0] - 30, 5), (255, 0, 0), 'up', self.window)
        self.collider_down = Rect((self.pos[0] + 15, self.pos[1] + self.size[1] - 5), (self.size[0] - 30, 5), (255, 0, 0), 'down', self.window)
        self.collider_left = Rect((self.pos[0] + 10, self.pos[1] + 5), (5, self.size[1] - 10), (255, 0, 0), 'left', self.window)
        self.collider_right = Rect((self.pos[0] - 15 + self.size[0], self.pos[1] + 5), (5, self.size[1] - 10), (255, 0, 0), 'right', self.window)

        self.colliders.append(self.collider_up)
        self.colliders.append(self.collider_down)
        self.colliders.append(self.collider_left)
        self.colliders.append(self.collider_right)
        
    
    def draw_colliders(self):
        for collider in self.colliders:
            #print(":A")
            collider.draw()

    def draw(self):
        if self.sprite != None:
            self.window.blit(self.sprite, self.pos)
        else:
            pygame.draw.rect(self.window, self.color, self.rect)

    
    def loop(self):
        self.init_colliders()
        self.middle = (self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2)
        if self.rect.x != self.pos[0]:
            self.rect.x = self.pos[0]
        if self.rect.y != self.pos[1]:
            self.rect.y = self.pos[1]

        if self.walking:
            self.handle_animation()
        else:
            self.sprite_id = self.default_sprite_id
            self.load_player_sprite()

    
    def handle_animation(self):
        if self.direction == "right":
            if time.time() - self.animation_time > 0.1:
                self.animation_time = time.time()
                self.sprite_id += 1
                if self.sprite_id > self.default_sprite_id + 3:
                    self.sprite_id = self.default_sprite_id + 1
                self.load_player_sprite()
        elif self.direction == "left":
            if time.time() - self.animation_time > 0.1:
                self.animation_time = time.time()
                if self.sprite_id < self.default_sprite_id + 3:
                    self.sprite_id = self.default_sprite_id + 4
                self.sprite_id += 1
                if self.sprite_id > self.default_sprite_id + 6:
                    self.sprite_id = self.default_sprite_id + 4
                self.load_player_sprite()
        elif self.direction == "up":
            if time.time() - self.animation_time > 0.1:
                self.animation_time = time.time()
                if self.sprite_id < self.default_sprite_id + 6:
                    self.sprite_id = self.default_sprite_id + 7
                self.sprite_id += 1
                if self.sprite_id > self.default_sprite_id + 9:
                    self.sprite_id = self.default_sprite_id + 7
                self.load_player_sprite()
        elif self.direction == "down":
            if time.time() - self.animation_time > 0.1:
                self.animation_time = time.time()
                if self.sprite_id < self.default_sprite_id + 9:
                    self.sprite_id = self.default_sprite_id + 10
                self.sprite_id += 1
                if self.sprite_id > self.default_sprite_id + 12:
                    self.sprite_id = self.default_sprite_id + 10
                self.load_player_sprite()

        
    def load_player_sprite(self, sprite_id:int=None):
        if sprite_id is None:
            sprite_id = self.sprite_id
        sprite = self.spritesheet.image(sprite_id)
        self.sprite = pygame.transform.scale(sprite, self.size)

    
    def collide_rect(self, rect:pygame.Rect, block_offset:tuple=(0, 0), collidable:bool=False, wall:bool=False):
        #block = pygame.Rect(self.pos[0] + block_offset[0], self.pos[1] + block_offset[1], self.size[0], self.size[1])

        #self.collided = None
        if wall:
            rect = pygame.Rect(rect.x + block_offset[0], rect.y + block_offset[1], rect.w, rect.h)
        for collider in self.colliders:
            if rect.colliderect(collider):
                if collidable:
                    self.collided = collider.type
                
                return collider.type is not None
        if collidable:
            self.collided = None
        return False