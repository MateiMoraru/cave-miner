import pygame
from entity import Entity
from spritesheet import *
from typing import List, Tuple
from light import LIGHT

class Player(Entity):
    def __init__(self, window:pygame.Surface, pos:List[float], sprite:pygame.Surface=None, spritesheet:Spritesheet=None):
        super().__init__(window, pos, (70, 70), (0, 0, 0), sprite)
        self.offset = [0, 0]
        self.spritesheet = spritesheet
        self.light = LIGHT(128, self.spritesheet.image(SHADOW))

    
    def draw(self):
        super().draw()


    def loop(self):
        super().loop()
        self.handle_keys()

    
    def handle_keys(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.pos[1] -= self.speed
        if keys[pygame.K_a]:
            self.pos[0] -= self.speed
        if keys[pygame.K_s]:
            self.pos[1] += self.speed
        if keys[pygame.K_d]:
            self.pos[0] += self.speed