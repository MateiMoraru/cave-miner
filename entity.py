import time
import pygame
from spritesheet import Spritesheet
from typing import Tuple, List

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

    def draw(self):
        if self.sprite != None:
            self.window.blit(self.sprite, self.pos)
        else:
            pygame.draw.rect(self.window, self.color, self.rect)

    
    def loop(self):
        self.middle = (self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2)
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