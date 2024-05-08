import pygame

pygame.init()

display_info = pygame.display.Info()

# Get total screen width and height
screen_width = display_info.current_w
screen_height = display_info.current_h

print("Total screen size: {} x {}".format(screen_width, screen_height))

# Quit Pygame
pygame.quit()