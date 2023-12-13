import pygame
from typing import Tuple, List

class Entity:
    def __init__(self, window:pygame.Surface, pos:List[float], size:List[float], color:Tuple[int]=(255, 0, 255), sprite:pygame.Surface=None, speed:int=3):
        self.window = window
        self.pos = [pos[0] - size[0] / 2, pos[1] - size[1] / 2]
        self.size = size
        self.color = color
        if sprite is not None:
            self.sprite = pygame.transform.scale(sprite, self.size)
        self.speed = self.size[0] / 15

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