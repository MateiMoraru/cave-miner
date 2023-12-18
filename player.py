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
        #super().draw_colliders()


    def loop(self):
        super().loop()
        self.handle_keys()

    
    def handle_keys(self):
        keys = pygame.key.get_pressed()
        walked = False

        if keys[pygame.K_w] and self.collided != "up":
            self.offset[1] += self.speed
            walked = True
            self.direction = "up"
        elif keys[pygame.K_s] and self.collided != "down":
            self.offset[1] -= self.speed
            walked = True
            self.direction = "down"
        if keys[pygame.K_a] and self.collided != "left":
            self.offset[0] += self.speed
            walked = True
            self.direction = "left"
        elif keys[pygame.K_d] and self.collided != "right":
            self.offset[0] -= self.speed
            walked = True
            self.direction = "right"
        
        if not walked:
            self.direction = None
            return
        self.walking = walked

    
    # def player_light(self):
    #     w, h = self.sprite.get_size()
    #     r, g, b = (255, 255, 255)
    #     for x in range(w):
    #         for y in range(h):
    #             #a = self.sprite.get_at((x, y))[3]
    #             color = self.sprite.get_at((x, y))
    #             #print(a)
                
    #             self.sprite.set_at((x, y), pygame.Color(color.r, color[1].g, color[2].b, color.a))