import pygame
import random
import sys
from engine.food import Food
from engine.enemy import Enemy
from engine.player import Player
from engine.display import Display
from engine.settings import *
from engine.particles import ParticleManager



class LevelManager:
    def __init__(self, source, screen, player:Player, display:Display, partman:ParticleManager):
        self.current_level = 1
        self.food_remaining = 5
        self.enemy_count = 1
        self.player = player
        self.display = display
        self.food = []
        self.enemies = []
        self.screen = screen
        self.partman = partman
        self.source = source
        self.shake = 0
        self.shake_offset = [0, 0]

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
        while len(self.enemies) < self.enemy_count:
            enemy_width = int(ENEMY_DIMEN[0] * self.display.display_width)
            enemy_height = int(ENEMY_DIMEN[1] * self.display.display_height)

            # Choose a random edge of the screen
            edge = random.choice(["top", "bottom", "left", "right"])

            if edge == "top":
                random_x = random.randint(0, self.display.display_width - enemy_width)
                random_y = 0
            elif edge == "bottom":
                random_x = random.randint(0, self.display.display_width - enemy_width)
                random_y = self.display.display_height - enemy_height
            elif edge == "left":
                random_x = 0
                random_y = random.randint(0, self.display.display_height - enemy_height)
            else:  # edge == "right"
                random_x = self.display.display_width - enemy_width
                random_y = random.randint(0, self.display.display_height - enemy_height)

            # Check distance from player
            player_pos = self.player.rect.center
            enemy_pos = (random_x + enemy_width / 2, random_y + enemy_height / 2)
            distance = ((player_pos[0] - enemy_pos[0]) ** 2 + (player_pos[1] - enemy_pos[1]) ** 2) ** 0.5

            # If too close to player, choose a different edge
            min_distance = 450  # Adjust as needed
            if distance < min_distance:
                continue

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
               
                self.shake = SHAKE_DURATION

                if not self.food:
                    food.spit_particles(self.partman, is_last=True)
                    self.reset_level()
                else:
                    food.spit_particles(self.partman)

        for enemy1 in self.enemies:
            for enemy2 in self.enemies:
                if enemy1 != enemy2 and enemy1.rect.colliderect(enemy2.rect):
                    # Calculate direction from enemy1 to enemy2
                    dx = enemy2.rect.centerx - enemy1.rect.centerx
                    dy = enemy2.rect.centery - enemy1.rect.centery

                    # Move enemy1 away from enemy2
                    distance = ((dx ** 2) + (dy ** 2)) ** 0.5
                    if distance == 0:  # Avoid division by zero
                        distance = 1
                    repel_force = 200 # Adjust as needed
                    move_x = repel_force * (dx / distance)
                    move_y = repel_force * (dy / distance)

                    # Update enemy1 position
                    enemy1.rect.move_ip(-move_x, -move_y)

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


    def update(self, mpos):
        for enemy in self.enemies:
            enemy.chase_player(self.player)
            pygame.draw.rect(self.screen, enemy.color, enemy.rect)
        for food in self.food:
            pygame.draw.rect(self.screen, food.color, food.rect)

        self.player.update_pos(mpos[0], mpos[1])
        pygame.draw.rect(self.screen, self.player.color, self.player.rect)

        if self.shake > 0:
            self.shake -= 1
        
        if self.shake:
            self.shake_offset[0] = random.randint(0, SHAKE_INTENSITY) - SHAKE_INTENSITY
            self.shake_offset[1] = random.randint(0, SHAKE_INTENSITY) - SHAKE_INTENSITY

        self.source.blit(self.screen, self.shake_offset)
