import pygame
import os

def run_game():
    os.system("python run.py")
pygame.init()

# set up the screen
screen = pygame.display.set_mode((800, 600))

# load font
font = pygame.font.SysFont("Arial", 24)

# set up text
text = "PERATURAN GAME PACMAN\n\n1. Pacman harus memakan semua titik dalam labirin tanpa ditangkap oleh hantu.\n2. Pacman dapat makan titik besar untuk sementara waktu dapat memakan hantu.\n3. Jangan sampai Pacman kehabisan nyawa atau permainan akan berakhir.\n4. Gunakan tombol panah untuk menggerakkan Pacman.\n\nTekan SPACE untuk mulai bermain."

# render text
text_rendered = font.render(text, True, (255, 255, 255))

# set up background
background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))

# set up clock
clock = pygame.time.Clock()

# run the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                run_game()
            break
                
    
    # draw the screen
    screen.blit(background, (0, 0))
    screen.blit(text_rendered, (50, 50))
    pygame.display.flip()
    
    # set up the frame rate
    clock.tick(60)

# quit the game
pygame.quit()
