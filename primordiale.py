import pygame
import sys

from engine.audio import *
from engine.settings import *
from engine.player import Player
from engine.display import Display
from engine.level import LevelManager  # Import LevelManager from level.py
from engine.particles import ParticleManager

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
play_background_music()

def display_info(fps, level_info, timer, screen, font):
    fps_text = font.render("FPS: {:.2f}".format(fps), True, (255, 255, 255))
    level_text = font.render(level_info, True, (255, 255, 255))
    timer_text = font.render(timer, True, (255, 255, 255))

    screen.blit(fps_text, (10, 10))
    screen.blit(level_text, (display.display_width - level_text.get_width() - 10, 10))
    screen.blit(timer_text, (display.display_width // 2 - timer_text.get_width() // 2, 10))


running = True
start_time = pygame.time.get_ticks()  # Get the initial time
while running:
    current_time = pygame.time.get_ticks() - start_time  # Calculate elapsed time
    minutes = current_time // 60000  # Calculate minutes
    seconds = (current_time // 1000) % 60  # Calculate seconds
    milliseconds = current_time % 1000  # Calculate milliseconds
    timer_text = "{:02}:{:02}:{:03}".format(minutes, seconds, milliseconds)

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    canvas.fill((0, 0, 0))

    if not level_manager.is_game_over:
        partman.update(gravity=True)
        for particle in partman.getall():
            pygame.draw.circle(canvas, particle.color, particle.pos, 6.5)

        mpos = pygame.mouse.get_pos()
        level_manager.update(mpos)
        level_manager.update_timer_text(timer_text)

        level_manager.check_collisions()  # Check collisions between player, enemies, and food
    else:
        start_time = level_manager.game_over(start_time)

    display_info(clock.get_fps(), "Level: " + str(level_manager.current_level), timer_text, screen, font)
    pygame.display.update()

pygame.quit()
sys.exit()