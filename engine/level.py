import pygame
import random
import sys
from engine.food import Food
from engine.enemy import Enemy
from engine.player import Player
from engine.display import Display
from engine.settings import *

class LevelManager:
    def __init__(self, screen, player:Player, display:Display):
        self.current_level = 1
        self.food_remaining = 5
        self.enemy_count = 1
        self.player = player
        self.display = display
        self.food = []
        self.enemies = []
        self.screen = screen

    def initialize_level(self):
        self.food = []
        for _ in range(self.food_remaining):
            food_width = int(FOOD_DIMEN[0] * self.display.display_width)
            food_height = int(FOOD_DIMEN[1] * self.display.display_height)

            random_x = random.randint(0, self.display.display_width - food_width)
            random_y = random.randint(0, self.display.display_height - food_height)
            food = Food([random_x, random_y], FOOD_DIMEN, self.display)
            self.food.append(food)

        self.enemies = []
        for _ in range(self.enemy_count):
            enemy_width = int(ENEMY_DIMEN[0] * self.display.display_width)
            enemy_height = int(ENEMY_DIMEN[1] * self.display.display_height)

            random_x = random.randint(0, self.display.display_width - enemy_width)
            random_y = random.randint(0, self.display.display_height - enemy_height)
            enemy = Enemy([random_x, random_y], ENEMY_DIMEN, self.display)
            self.enemies.append(enemy)

    def check_collisions(self):
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                pygame.quit()
                sys.exit()

        for food in self.food:
            if food.rect.colliderect(self.player.rect):
                self.food.remove(food)

        if not self.food:
            self.reset_level()

        for enemy in self.enemies:
            for food in self.food:
                if enemy.rect.colliderect(food.rect):
                    # Calculate collision direction
                    dx = enemy.rect.centerx - food.rect.centerx
                    dy = enemy.rect.centery - food.rect.centery

                    # Move food box away from enemy
                    if abs(dx) > abs(dy):
                        # Horizontal collision
                        if dx > 0:
                            food.rect.right = enemy.rect.left
                        else:
                            food.rect.left = enemy.rect.right
                    else:
                        # Vertical collision
                        if dy > 0:
                            food.rect.bottom = enemy.rect.top
                        else:
                            food.rect.top = enemy.rect.bottom

    def reset_level(self):
        self.current_level += 1
        self.food_remaining += 2
        self.enemy_count += 1
        self.initialize_level()

    def update(self):
        for enemy in self.enemies:
            enemy.chase_player(self.player)
            pygame.draw.rect(self.screen, enemy.color, enemy.rect)
        for food in self.food:
            pygame.draw.rect(self.screen, food.color, food.rect)
