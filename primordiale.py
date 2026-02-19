import random
import pygame
import sys

# Initialize pygame early
pygame.init()
pygame.mixer.init()

from engine.audio import *
from engine.settings import *
from engine.player import Player
from engine.display import Display
from engine.level import LevelManager
from engine.particles import ParticleManager

# 1. Initialize Display
display = Display()

clock = pygame.time.Clock()
partman = ParticleManager()
ppartmen = ParticleManager()

# 2. Player Init
player = Player([0, 0], PLAYER_DIMEN, display)
font = pygame.font.Font(None, 36)
enemies = []
shake_offset = [0, 0]

# 3. Set Screen Mode
screen = pygame.display.set_mode(
    (display.width, display.height), 
    pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
)
canvas = pygame.Surface((display.width, display.height))

pygame.display.set_caption("Primordiale - JohnLesterDev")
pygame.mouse.set_visible(False)

level_manager = LevelManager(screen, canvas, player, display, partman) 
level_manager.initialize_level()
play_background_music()

def display_info(fps, level_info, timer, screen, font):
    fps_text = font.render("FPS: {:.2f}".format(fps), True, (255, 255, 255))
    level_text = font.render(level_info, True, (255, 255, 255))
    timer_text = font.render(timer, True, (255, 255, 255))

    screen.blit(fps_text, (10, 10))
    screen.blit(level_text, (display.width - level_text.get_width() - 10, 10))
    screen.blit(timer_text, (display.width // 2 - timer_text.get_width() // 2, 10))


running = True
start_time = pygame.time.get_ticks()  

while running:
    # --- DELTA TIME CALCULATION ---
    # clock.tick returns milliseconds passed since last frame.
    # We divide by 1000 to get seconds (e.g., 0.016 for 60fps).
    dt = clock.tick(FPS) / 1000.0
    
    current_time = pygame.time.get_ticks() - start_time  
    minutes = current_time // 60000  
    seconds = (current_time // 1000) % 60 
    milliseconds = current_time % 1000 
    timer_text = "{:02}:{:02}:{:03}".format(minutes, seconds, milliseconds)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    canvas.fill((0, 0, 0))
    screen.fill((0, 0, 0))

    if not level_manager.is_game_over:
        mpos = pygame.mouse.get_pos()
        
        # TRAIL (ppartmen)
        ppartmen.update(dt=dt)
        for p in ppartmen.getall():
            # Draw using the particle's specific size
            pygame.draw.circle(canvas, p.color, p.pos, p.size)
        
        # EXPLOSIONS (partman)
        partman.update(dt=dt, gravity=True)
        for p in partman.getall():
            pygame.draw.circle(canvas, p.color, p.pos, p.size)

        level_manager.update(mpos, ppartmen, dt)
        level_manager.update_timer_text(timer_text)
        level_manager.check_collisions(partman)
    else:
        start_time = level_manager.game_over(start_time)

    display_info(clock.get_fps(), "Level: " + str(level_manager.current_level), timer_text, screen, font)
    pygame.display.update()

pygame.quit()
sys.exit()