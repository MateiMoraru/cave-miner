import pygame

class Spritesheet(object):
    def __init__(self, filename, size:int=32, total_size:int=320):
        self.size = size #ex 16x16
        self.total_size = total_size #128x128
        self.sprites_no = self.total_size / self.size
        self.unit_size = total_size / size

        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as message:
            print('Unable to load spritesheet image:', filename)
        

    def image_at(self, rectangle, colorkey = None):

        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    

    def image(self, id, colorkey = (0, 0, 0)):
        x = (id % (self.sprites_no)) * self.size
        y = (id // (self.sprites_no)) * self.size
        return self.image_at((x, y, self.size, self.size), colorkey)
    

    def images_at(self, rects, colorkey = (0, 0, 0)):
        return [self.image_at(rect, colorkey) for rect in rects]
    

    def load_strip(self, rect, image_count, colorkey = (0, 0, 0)):
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

WALL_1 = 16    
PLAYER = 20
PLAYER_RIGHT_1 = 21
PLAYER_RIGHT_2 = 22
PLAYER_RIGHT_3 = 23
PLAYER_LEFT_1 = 24
PLAYER_LEFT_2 = 25
PLAYER_LEFT_3 = 26
PLAYER_UP_1 = 27
PLAYER_UP_2 = 28
PLAYER_UP_3 = 29
PLAYER_DOWN_1 = 30
PLAYER_DOWN_2 = 31
PLAYER_DOWN_3 = 32
