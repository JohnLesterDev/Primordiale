from engine.food import Food
from engine.settings import *
from math import atan2, degrees, pi, cos, sin


class Enemy(Food):
    def __init__(self, position, dimension, display, enemy_speed=None):
        super().__init__(position, dimension, display)
        self.vel = [0,0]
        self.color = [189, 25, 23]
        self.enemy_speed = enemy_speed
        self.cur_speed = 0
        self.size = 1  # Add a size attribute and initialize it to 1

    def chase_player(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        angle = degrees(atan2(dy, dx))

        if not self.enemy_speed:
            speed = ENEMY_SPEED 
            self.cur_speed = speed
        else:
            speed = self.enemy_speed
            self.cur_speed = speed
        self.vel[0] = self.cur_speed * cos(angle * pi / 180) 
        self.vel[1] = self.cur_speed * sin(angle * pi / 180) 

        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]

    def increase_size_and_slow_down(self):
        self.size += 1  # Increase size
        self.rect.inflate_ip(ENEMY_INFLATE_SIZE, ENEMY_INFLATE_SIZE)  # Inflate the enemy's rect
        self.cur_speed *= ENEMY_SLOW_DOWN_FACTOR  # Slow down the speed by a factor
