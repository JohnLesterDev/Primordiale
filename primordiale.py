import pygame

from engine.settings import *
from engine.display import Display
from engine.particles import ParticleManager

pygame.init()
pygame.mixer.init()

display = Display(WIDTH, HEIGHT)
clock = pygame.time.Clock()

screen = pygame.display.set_mode((display.display_width, display.display_height))
pygame.display.set_caption("Primordiale - JohnLesterDev")


running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0,0,0))
    
    pygame.display.update()

pygame.quit()