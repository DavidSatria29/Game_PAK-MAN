import pygame

class background:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background_image = None

    def set_background_image(self, image_path):
        self.background_image = pygame.image.load(image_path).convert()

    def draw_background(self):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))

    def add_image(self, image_path, x, y):
        image = pygame.image.load(image_path).convert_alpha()
        self.screen.blit(image, (x, y))
    def update(self):
        pygame.display.flip()
