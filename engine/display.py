import pygame

pygame.init()

display_info = pygame.display.Info()

class Display:
    def __init__(self, width_per=None, height_per=None) -> None:
        self.max_width = display_info.current_w
        self.max_height = display_info.current_h

        if width_per and height_per:
            self.display_width = int(self.max_width * width_per)
            self.display_height = int(self.max_height * height_per)
        else:
            self.display_height = self.max_height
            self.display_width = self.display_width