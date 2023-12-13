import pygame
from entity import Entity
from spritesheet import *
from typing import List, Tuple
from light import Light

class Player(Entity):
    def __init__(self, window:pygame.Surface, pos:List[float], tile_size:Tuple[int, int], sprite:pygame.Surface=None, spritesheet:Spritesheet=None):
        self.tile_size = tile_size
        super().__init__(window, pos, tile_size, (0, 0, 0), sprite)
        self.offset = [0, 0]
        self.spritesheet = spritesheet
        light_tex =  pygame.image.load("assets/light.png")
        self.light = Light(self.size[0] * 5, self.middle, light_tex)

    
    def draw(self):
        super().draw()


    def loop(self):
        super().loop()
        self.handle_keys()

    
    def handle_keys(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.offset[1] += self.speed
        if keys[pygame.K_a]:
            self.offset[0] += self.speed
        if keys[pygame.K_s]:
            self.offset[1] -= self.speed
        if keys[pygame.K_d]:
            self.offset[0] -= self.speed