import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []
        self.font = pygame.font.Font(None, 50)
        self.selected_option = 0
        self.button_height = 70  # ketinggian setiap tombol
        self.button_margin = 20  # jarak antara tombol
        self.background_image = None

    def set_background_image(self, image_path):
        self.background_image = pygame.image.load(image_path).convert()
    
    def draw(self):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill((0, 0, 0))
        
        
pygame.init()
screen = pygame.display.set_mode((448,576))

menu = Menu(screen)
menu.set_background_image('peraturan.png')

running = True

menu.draw()


