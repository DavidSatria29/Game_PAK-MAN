import pygame

class musik:
    def __init__(self):
        pygame.mixer.init()
        self.jalan = pygame.mixer.Sound('musik/jalan.mp3')
        self.mati = pygame.mixer.Sound('musik/mati.wav')
        self.menang = pygame.mixer.Sound('musik/menang.wav')
        self.makan = pygame.mixer.Sound('musik/pelet.wav')
        self.bunuh = pygame.mixer.Sound('musik/bunuh.wav')
        self.medkit = pygame.mixer.Sound('musik/medkit.wav')
        self.slowmo = pygame.mixer.Sound('musik/slowmo.mp3')
        self.speed = pygame.mixer.Sound('musik/speed.wav')
        self.hantu = pygame.mixer.Sound('musik/hantu.mp3')
        self.teleport = pygame.mixer.Sound('musik/teleport.wav')
        self.kerjabagus = pygame.mixer.Sound('musik/kerjabagus.mp3')
        self.hati2 = pygame.mixer.Sound('musik/hati2.mp3')
        pygame.mixer.music.load('musik/musik2.mp3')