import pygame

pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)

def play():
    pygame.mixer.Sound("./static/sound.mp3").play()
