import pygame

class Menu:
    def __init__(self, screen, title, options):
        self.screen = screen
        self.title = title
        self.options = options
        self.buttons = []
        self.font = pygame.font.Font(None, 50)
        self.selected_option = 0
    
    def add_button(self, button):
        self.buttons.append(button)
    
    def draw(self):
        title_text = self.font.render(self.title, True, (255,255,255))
        title_rect = title_text.get_rect(center=(self.screen.get_width()/2, 100))
        self.screen.blit(title_text, title_rect)
        
        button_top = title_rect.bottom + 50
        for i, button in enumerate(self.buttons):
            text = self.font.render(button.label, True, (255,255,255) if i != self.selected_option else (255,0,0))
            rect = text.get_rect(center=(self.screen.get_width()/2, button_top + 70*i))
            self.screen.blit(text, rect)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.buttons)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                self.buttons[self.selected_option].select()

class Button:
    def __init__(self, label, callback):
        self.label = label
        self.callback = callback
    
    def select(self):
        self.callback()

# example usage
pygame.init()
screen = pygame.display.set_mode((800,600))

menu = Menu(screen, "PAK-MAN", ["Start Game", "Settings", "Quit"])
menu.add_button(Button("Start Game", lambda: print("starting game...")))
menu.add_button(Button("Settings", lambda: print("opening settings menu...")))
menu.add_button(Button("Quit", lambda: pygame.quit()))

running = True
while running:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False
        else:
            menu.handle_event(event)
    screen.fill((0,0,0))
    menu.draw()
    
    pygame.display.flip()
    
pygame.quit()