import pygame

pygame.init()
display_info = pygame.display.Info()

class Display:
    def __init__(self) -> None:
        # Full Monitor Resolution
        self.width = display_info.current_w
        self.height = display_info.current_h
        
        # We assume the game uses the full resolution
        self.display_width = self.width
        self.display_height = self.height

    def get_scale_basis(self):
        """Returns the height, which is the basis for square scaling."""
        return self.height