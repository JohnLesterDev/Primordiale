import random
import pygame # Need this for Vectors
from engine.player import Player
from engine.particles import ParticleManager
from engine.settings import *

class Food(Player):
    def __init__(self, position, dimension, display, has_random_movement=False):
        super().__init__(position, dimension, display)
        
        self.color = (82, 163, 65)
        self.display = display
        self.has_random_movement = has_random_movement

        self.color_choices = [
            [235, 64, 52], [235, 150, 52], [235, 174, 52],
            [226, 235, 52], [119, 235, 52], [52, 235, 131],
            [52, 235, 232], [52, 150, 235], [55, 52, 235],
            [143, 52, 235], [225, 52, 247]
        ]
        
        # Use Vectors for smoother float-based movement
        self.rect_pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        
        if self.has_random_movement:
            self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            # Speed needs to be high because we multiply by dt (e.g., 60 px/sec)
            self.speed = random.uniform(50.0, 200.0)
        else:
            self.velocity = pygame.math.Vector2(0, 0)
            self.speed = 0

    # UPDATED: Accepts dt
    def update_position(self, dt):
        if self.has_random_movement:
            # Move by Velocity * Speed * Time
            self.rect_pos += self.velocity * self.speed * dt
            
            # Update the integer rect
            self.rect.x = round(self.rect_pos.x)
            self.rect.y = round(self.rect_pos.y)

        # Boundary checks
        if self.rect.left < 0:
            self.velocity.x *= -1
            self.rect_pos.x = 0
        elif self.rect.right > self.display.width:
            self.velocity.x *= -1
            self.rect_pos.x = self.display.width - self.rect.width

        if self.rect.top < 0:
            self.velocity.y *= -1
            self.rect_pos.y = 0
        elif self.rect.bottom > self.display.height:
            self.velocity.y *= -1
            self.rect_pos.y = self.display.height - self.rect.height

    def spit_particles(self, partman: ParticleManager, is_last=False, mpos=None):
        if not is_last:
            for _ in range(220):
                # Calculate size for this specific particle
                s_min = PARTICLE_SCALE_EXPLOSION[0] * self.display.height
                s_max = PARTICLE_SCALE_EXPLOSION[1] * self.display.height
                p_size = random.uniform(s_min, s_max)
                
                partman.create(list(self.rect.center), [random.randint(0, 19), random.randint(0, 19)], 1.4, size=p_size, color=self.color)
        else:
            for _ in range(1000):
                s_min = PARTICLE_SCALE_EXPLOSION[0] * self.display.height
                s_max = PARTICLE_SCALE_EXPLOSION[1] * self.display.height
                p_size = random.uniform(s_min, s_max)
                
                partman.create(list(mpos), [19,19], 1, size=p_size, color=random.choice(self.color_choices))