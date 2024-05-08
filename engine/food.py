from engine.player import Player
from engine.particles import ParticleManager

class Food(Player):
    def __init__(self, position, dimension, display):
        super().__init__(position, dimension, display)
        self.color = (82, 163, 65)

    def spit_particles(self, partman: ParticleManager):
        for _ in range(10):  
            partman.create_particle(self.rect.center, [9, 9], 1.1)
