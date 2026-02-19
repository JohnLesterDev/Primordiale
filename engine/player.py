import pygame
from engine.display import Display

# How fast the player catches up to the mouse.
# 15.0 is snappy but has a tiny bit of weight. Lower = more floaty/delayed.
PLAYER_LERP_SPEED = 16.0

class Player:
    def __init__(self, position:list, dimension:list, display:Display) -> None:
        pixel_w = int(dimension[0] * display.height)
        pixel_h = int(dimension[1] * display.height)
        
        self.rect = pygame.Rect(position, (pixel_w, pixel_h))
        self.dimen = [pixel_w, pixel_h]
        self.color = (106, 109, 115)
        self.lives = 5
        
        # We need precise float coordinates for smooth movement
        self.pos = pygame.math.Vector2(position)

    # UPDATED: Now accepts 'dt' (Delta Time)
    def update_pos(self, target_x, target_y, dt, centered=False):
        # 1. Define the target (Mouse Position)
        if centered:
             # Calculate top-left from center
            target = pygame.math.Vector2(target_x - self.rect.width / 2, target_y - self.rect.height / 2)
        else:
            # The input x,y is already top-left (usually)
            # But since we use centered=True in level.py, we focus on that case.
            # However, LevelManager passes raw mouse pos which should be the CENTER of the player.
            # So we offset the target to make the mouse the center of the square.
            target = pygame.math.Vector2(target_x - self.rect.width / 2, target_y - self.rect.height / 2)
        
        # 2. The LERP Formula (Smooth Chase)
        # New Pos = Current Pos + (Difference * Speed * Time)
        direction = target - self.pos
        self.pos += direction * PLAYER_LERP_SPEED * dt
        
        # 3. Apply to the integer Rect
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))