import pygame
from environment import Environment
from spritesheet import Spritesheet
from text import Text
from menu import Menu
import pyautogui

class Game:
    def __init__(self):
        pygame.init()
        

        screen_size = pyautogui.size()
        self.window_size = (screen_size.width, screen_size.height)
        self.scale = screen_size[0] / 1100 # Default sizing is (1100, 750)
        self.window = pygame.display.set_mode(self.window_size, pygame.FULLSCREEN)
        pygame.display.set_caption("Cave Miner")
        self.running = True

        self.font = pygame.font.Font('assets/font.ttf', int(20 * self.scale))
        self.spritesheet = Spritesheet("assets/spritesheet.png", 32, 320)
        #self.tiles = Spritesheet("assets/tiles.png", 32, 320)
        self.environment = Environment(self.window, self.window_size, self.scale, self.spritesheet, self.font) 

        self.clock = pygame.time.Clock()
        
        self.in_menu = [True, False]
        main_menu = Menu(self.window, self.window_size, self.window_size)
        main_menu.add_buttons(self.main_menu_start, self.font, (self.window_size[0] / 2 , self.window_size[1] / 2), (500 * self.scale, 50 * self.scale), (111, 123, 128, 255), "Start Game")
        main_menu.add_buttons(self.exit, self.font, (self.window_size[0] / 2, self.window_size[1] / 2 + 100 * self.scale), (500 * self.scale, 50 * self.scale), (111, 123, 128, 255), "Exit")
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
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.in_menu[0] = not self.in_menu[0]
                    
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