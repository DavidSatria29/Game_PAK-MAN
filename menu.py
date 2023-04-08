import pygame

pygame.init()

# Set ukuran layar
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu Game")

# Load gambar background
# bg_image = pygame.image.load("background.jpg")

# Load font
font = pygame.font.Font(None, 30)

# Membuat tombol "Start"
start_button = pygame.Rect(200, 200, 200, 50)
start_text = font.render("Start", True, (255, 255, 255))
start_text_rect = start_text.get_rect(center=start_button.center)

# Membuat tombol "Quit"
quit_button = pygame.Rect(200, 300, 200, 50)
quit_text = font.render("Quit", True, (255, 255, 255))
quit_text_rect = quit_text.get_rect(center=quit_button.center)

# Loop utama
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Cek apakah tombol "Start" diklik
            if start_button.collidepoint(event.pos):
                # Panggil halaman keterangan
                import keterangan
                keterangan.run()
                # Setelah selesai, tampilkan tombol "Run"
                run_button = pygame.Rect(screen_width - 150, screen_height - 50, 100, 30)
                run_text = font.render("Run", True, (255, 255, 255))
                run_text_rect = run_text.get_rect(center=run_button.center)
            # Cek apakah tombol "Run" diklik
            elif 'run_button' in locals() and run_button.collidepoint(event.pos):
                # Panggil game
                import run
                run.run()
            # Cek apakah tombol "Quit" diklik
            elif quit_button.collidepoint(event.pos):
                running = False

    # Tampilkan gambar background
    # screen.blit(bg_image, (0, 0))

    # Tampilkan tombol "Start" dan "Quit"
    pygame.draw.rect(screen, (0, 0, 0), start_button)
    screen.blit(start_text, start_text_rect)
    pygame.draw.rect(screen, (0, 0, 0), quit_button)
    screen.blit(quit_text, quit_text_rect)

    # Jika tombol "Run" telah muncul, tampilkan tombol "Run"
    if 'run_button' in locals():
        pygame.draw.rect(screen, (0, 0, 0), run_button)
        screen.blit(run_text, run_text_rect)

    pygame.display.flip()

# Keluar dari Pygame
pygame.quit()
