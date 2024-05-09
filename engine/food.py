import random
from engine.player import Player
from engine.particles import ParticleManager

class Food(Player):
    def __init__(self, position, dimension, display, has_random_movement=False):
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
        self.display = display
        self.has_random_movement = has_random_movement
        if self.has_random_movement:
            self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
            self.speed = random.uniform(0.5, 2.0)
        else:
            self.velocity = [0, 0]

    def update_position(self):
        if self.has_random_movement:
            self.rect.x += self.velocity[0] * self.speed
            self.rect.y += self.velocity[1] * self.speed

        if self.rect.left < 0 or self.rect.right > self.display.display_width:
            self.velocity[0] *= -1  

        if self.rect.top < 0 or self.rect.bottom > self.display.display_height:
            self.velocity[1] *= -1  

    def spit_particles(self, partman: ParticleManager, is_last=False, mpos=None):
        if not is_last:
            for _ in range(220):  
                partman.create(list(self.rect.center), [random.randint(0, 19), random.randint(0, 19)], 1.4, color=self.color)
        else:
            for _ in range(1000):  
                partman.create(list(mpos), [19,19], 1, random.choice(self.color_choices))
