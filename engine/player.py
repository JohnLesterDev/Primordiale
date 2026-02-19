import pygame
from engine.display import Display

class Player:
    def __init__(self, position:list, dimension:list, display:Display) -> None:
        # FIX: We scale BOTH dimensions by display.height to keep it square
        pixel_w = int(dimension[0] * display.height)
        pixel_h = int(dimension[1] * display.height)
        
        self.rect = pygame.Rect(position, (pixel_w, pixel_h))
        self.dimen = [pixel_w, pixel_h]
        self.color = (106, 109, 115)
        self.lives = 5
    
    def update_pos(self, x, y, centered=False, dimen=None):
        if centered:
            self.rect.center = (x, y)
        else:
            if dimen:
                self.rect.update([x, y], dimen)
            else:
                self.rect.update([x, y], self.dimen)