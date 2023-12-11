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
        x = (id % (self.sprites_no-1)) * self.size
        y = (id // (self.sprites_no-1)) * self.size
        return self.image_at((x, y, self.size, self.size), colorkey)
    

    def images_at(self, rects, colorkey = (0, 0, 0)):
        return [self.image_at(rect, colorkey) for rect in rects]
    

    def load_strip(self, rect, image_count, colorkey = (0, 0, 0)):
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)
    
PLAYER = 0
PLAYER_RIGHT_1 = 1
PLAYER_RIGHT_2 = 2
PLAYER_RIGHT_3 = 3
PLAYER_LEFT_1 = 4
PLAYER_LEFT_2 = 5
PLAYER_LEFT_3 = 6
PLAYER_UP_1 = 7
PLAYER_UP_2 = 8
PLAYER_UP_3 = 9
PLAYER_DOWN_1 = 10
PLAYER_DOWN_2 = 11
PLAYER_DOWN_3 = 12
SHADOW = 13