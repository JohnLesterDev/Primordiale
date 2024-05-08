import pygame
import sys

from engine.settings import *
from engine.display import Display
from engine.particles import ParticleManager
from engine.player import Player
from engine.level import LevelManager  # Import LevelManager from level.py

pygame.init()
pygame.mixer.init()

display = Display(WIDTH, HEIGHT)
clock = pygame.time.Clock()
partman = ParticleManager()
player = Player([0, 0], PLAYER_DIMEN, display)
font = pygame.font.Font(None, 36)
enemies = []
shake_offset = [0, 0]

screen = pygame.display.set_mode((display.display_width, display.display_height))
canvas = pygame.Surface((display.display_width, display.display_height))
pygame.display.set_caption("Primordiale - JohnLesterDev")
pygame.mouse.set_visible(False)

level_manager = LevelManager(screen, canvas, player, display, partman)  # Initialize LevelManager with player and display
level_manager.initialize_level()

def display_info(fps, level_info, screen, font):
    fps_text = font.render("FPS: {:.2f}".format(fps), True, (255, 255, 255))
    level_text = font.render(level_info, True, (255, 255, 255))

    screen.blit(fps_text, (10, 10))
    screen.blit(level_text, (display.display_width - level_text.get_width() - 10, 10))

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    canvas.fill((0, 0, 0))

    partman.update(gravity=True)
    for particle in partman.getall():
        pygame.draw.circle(canvas, particle.color, particle.pos, 6.5)

    mpos = pygame.mouse.get_pos()
    level_manager.update(mpos)

    display_info(clock.get_fps(), "Level: " + str(level_manager.current_level), screen, font)

    level_manager.check_collisions()  # Check collisions between player, enemies, and food

    pygame.display.update()

pygame.quit()
sys.exit() 
