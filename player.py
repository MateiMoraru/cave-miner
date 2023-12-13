import pygame
from entity import Entity
from spritesheet import *
from typing import List, Tuple

class Player(Entity):
    def __init__(self, window:pygame.Surface, pos:List[float], tile_size:Tuple[int, int], sprite_id:int=None, spritesheet:Spritesheet=None):
        super().__init__(window, pos, tile_size, (0, 0, 0), sprite_id, spritesheet, tile_size[0] / 15)
        self.offset = [0, 0]

    
    def draw(self):
        super().draw()


    def loop(self):
        super().loop()
        self.handle_keys()

    
    def handle_keys(self):
        keys = pygame.key.get_pressed()

        walked = False

        if keys[pygame.K_w]:
            self.offset[1] += self.speed
            walked = True
            self.direction = "up"
        elif keys[pygame.K_s]:
            self.offset[1] -= self.speed
            walked = True
            self.direction = "down"
        if keys[pygame.K_a]:
            self.offset[0] += self.speed
            walked = True
            self.direction = "left"
        elif keys[pygame.K_d]:
            self.offset[0] -= self.speed
            walked = True
            self.direction = "right"
        
        if not walked:
            self.direction = None
        self.walking = walked