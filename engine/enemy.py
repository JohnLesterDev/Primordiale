from engine.food import Food
from engine.settings import *
from math import atan2, degrees, pi, cos, sin

class Enemy(Food):
    def __init__(self, position, dimension, display, enemy_speed=None):
        super().__init__(position, dimension, display)
        self.vel = [0,0]
        self.color = [189, 25, 23]
        self.enemy_speed = enemy_speed

    def chase_player(self, player):
        # Calculate the direction towards the player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        # Calculate the angle towards the player (in degrees)
        angle = degrees(atan2(dy, dx))

        # Adjust the enemy's velocity based on the calculated angle
        if not self.enemy_speed:
            speed = ENEMY_SPEED  # Adjust as needed
        else:
            speed = self.enemy_speed
        self.vel[0] = speed * cos(angle * pi / 180)  # Convert angle to radians
        self.vel[1] = speed * sin(angle * pi / 180)

        # Update the enemy's position
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]
