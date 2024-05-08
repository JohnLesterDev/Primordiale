import random

from engine.player import Player
from engine.particles import ParticleManager

class Food(Player):
    def __init__(self, position, dimension, display):
        super().__init__(position, dimension, display)
        self.color = (82, 163, 65)
        self.color_choices = [
            [235, 64, 52],
            [235, 150, 52],
            [235, 174, 52],
            [226, 235, 52],
            [119, 235, 52],
            [52, 235, 131],
            [52, 235, 232],
            [52, 150, 235],
            [55, 52, 235],
            [143, 52, 235],
            [225, 52, 247]
        ]

    def spit_particles(self, partman: ParticleManager, is_last=False):
        if not is_last:
            for _ in range(110):  
                partman.create(list(self.rect.center), [11, 11], 1.4, color=(82, 163, 65))
        else:
            for _ in range(350):  
                partman.create(list(self.rect.center), [10, 10], 2.1, random.choice(self.color_choices))
