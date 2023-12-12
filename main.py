import pygame
from environment import Environment
from spritesheet import Spritesheet
from text import Text
from menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font('assets/font.ttf', 20)

        self.window_size = (1100, 750)
        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Terraria")
        self.running = True
        
        self.spritesheet = Spritesheet("assets/spritesheet.png", 32, 320)
        self.tiles = Spritesheet("assets/tiles.png", 32, 320)
        self.environment = Environment(self.window, self.window_size, self.spritesheet, self.tiles, self.font) 

        self.clock = pygame.time.Clock()
        
        self.in_menu = [True, False]
        main_menu = Menu(self.window, self.window_size, self.window_size)
        main_menu.add_buttons(self.main_menu_start, self.font, (self.window_size[0] / 2 - 250, self.window_size[1] / 2 - 25), (500, 50), (111, 123, 128, 255), "Start Game")
        main_menu.add_buttons(self.exit, self.font, (self.window_size[0] / 2 - 250, self.window_size[1] / 2 + 50), (500, 50), (111, 123, 128, 255), "Exit")
        self.menus = [main_menu]


    def run(self):
        self.loop()

        self.exit()


    def draw(self):
        self.environment.draw()

        Text(self.font, f"FPS {int(self.clock.get_fps())}", (255, 255, 255), (0, 0), "topleft").draw(self.window)


    def loop(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.exit()
                    
            self.window.fill((0, 5, 13))

            if not self.in_menu[0]:
                self.draw()
                self.environment.loop()
            else:
                self.menus[0].draw()

            pygame.display.update()
            self.clock.tick(FPS)

    
    def main_menu_start(self):
        self.in_menu[0] = False


    def exit(self):
        quit()


if __name__ == "__main__":
    game = Game()
    FPS = 60
    game.run()