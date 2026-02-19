import random
import pygame
from engine.food import Food
from engine.settings import *

STATE_CHASE = "chase"
STATE_BAIT = "bait"
STATE_STALK = "stalk"
STATE_RAGE = "rage"

class Enemy(Food):
    def __init__(self, position, dimension, display, enemy_speed=None):
        super().__init__(position, dimension, display)
        self.original_color = (189, 25, 23)
        self.color = list(self.original_color)
        
        self.base_speed = enemy_speed if enemy_speed else ENEMY_SPEED
        self.current_speed = self.base_speed
        self.size = 1
        
        self.pos = pygame.math.Vector2(self.rect.center)
        self.vel = pygame.math.Vector2(0, 0)
        
        self.state = STATE_CHASE
        self.state_timer = pygame.time.get_ticks()
        self.state_duration = random.randint(500, 2000)

    def decide_brain(self):
        now = pygame.time.get_ticks()
        if now - self.state_timer > self.state_duration:
            self.state_timer = now
            choices = [STATE_CHASE, STATE_BAIT, STATE_STALK, STATE_RAGE]
            weights = [60, 15, 10, 15]
            self.state = random.choices(choices, weights=weights, k=1)[0]
            
            if self.state == STATE_RAGE:
                self.state_duration = random.randint(400, 800)
            elif self.state == STATE_STALK:
                self.state_duration = random.randint(500, 1500)
            elif self.state == STATE_BAIT:
                 self.state_duration = random.randint(1000, 2000)
            else:
                self.state_duration = random.randint(1000, 3000)

    # UPDATED: Now accepts dt
    def chase_player(self, player, dt):
        self.decide_brain()

        player_vec = pygame.math.Vector2(player.rect.center)
        enemy_vec = self.pos
        
        direction = player_vec - enemy_vec
        distance = direction.length()
        
        if distance > 0:
            direction = direction.normalize()
        else:
            direction = pygame.math.Vector2(0, 0)

        if self.state == STATE_CHASE:
            self.current_speed = self.base_speed
            self.vel = direction * self.current_speed
            self.color = [189, 25, 23]

        elif self.state == STATE_BAIT:
            self.current_speed = self.base_speed * 0.8
            self.vel = -direction * self.current_speed
            self.color = [200, 100, 100]

        elif self.state == STATE_STALK:
            self.vel = pygame.math.Vector2(0, 0)
            self.color = [100, 0, 0]

        elif self.state == STATE_RAGE:
            self.current_speed = self.base_speed * 3.0
            self.vel = direction * self.current_speed
            self.color = [255, 50, 50]

        # MOVE WITH DT (Velocity * time = Distance)
        self.pos += self.vel * dt
        self.rect.center = round(self.pos.x), round(self.pos.y)

    def increase_size_and_slow_down(self):
        self.size += 1
        self.rect.inflate_ip(ENEMY_INFLATE_SIZE, ENEMY_INFLATE_SIZE)
        self.base_speed *= 0.9