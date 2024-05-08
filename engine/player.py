import pygame

from engine.display import Display



class Player:
    def __init__(self, position:list, dimension:list, display:Display) -> None:
        dimension = [dimension[0]*display.display_width, dimension[1]*display.display_height]
        self.rect = pygame.Rect(position, dimension)
        self.dimen = dimension
        self.color = (106, 109, 115)
        self.lives = 5
    
    def update_pos(self, x, y, centered=False, dimen=None):
        if centered:
            player_center_x = self.rect.centerx
            player_center_y = self.rect.centery

            mouse_offset_x = x - player_center_x
            mouse_offset_y = y - player_center_y

            self.rect.move_ip(mouse_offset_x, mouse_offset_y)
        else:
            if dimen:
                self.rect.update([x, y], dimen)
            else:
                self.rect.update([x, y], self.dimen)
        
        if dimen:
            self.rect.update([x, y], dimen)
        else:
            self.rect.update([x, y], self.dimen)

    

