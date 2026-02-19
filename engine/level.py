import pygame
import random
import sys
from engine.food import Food
from engine.enemy import Enemy
from engine.player import Player
from engine.display import Display
from engine.particles import ParticleManager
from engine.audio import *
from engine.settings import *

# Access global variables
from engine.settings import ENEMY_SPEED, PARTICLE_SCALE_TRAIL
from engine.enemy import STATE_BOSS, STATE_VACUUM, STATE_BEING_SUCKED, STATE_CHASE

class LevelManager:
    # ... (Keep __init__, update_timer_text, game_over, reset_game, etc. EXACTLY AS IS) ...
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
        self.leveled_sfx = load_sound("level-1.wav")
        self.eat_sfx = load_sound("eat-1.wav")
        self.kill_sfx = load_sound("kill.wav")
        self.eat_sfx.set_volume(0.4)
        self.game_over_font = pygame.font.Font(None, 36)
        self.highest_level = 1
        self.is_game_over = False
        self.timer_text = ""

    def update_timer_text(self, timer_text):
        self.timer_text = timer_text

    def game_over(self, start_time):
        pygame.mouse.set_visible(True)
        pause_background_music()
        game_over_text = self.game_over_font.render("Game Over", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(self.display.width // 2, self.display.height // 2 - 50))
        highest_level_text = self.game_over_font.render("Highest Level: " + str(self.highest_level) + " On " + self.timer_text, True, (255, 255, 255))
        highest_level_rect = highest_level_text.get_rect(center=(self.display.width // 2, self.display.height // 2))
        replay_text = self.game_over_font.render("Click to Restart", True, (255, 255, 255))
        replay_rect = replay_text.get_rect(center=(self.display.width // 2, self.display.height // 2 + 50))

        while True:
            self.screen.fill((0, 0, 0))
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(highest_level_text, highest_level_rect)
            self.screen.blit(replay_text, replay_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if replay_rect.collidepoint(event.pos):
                        self.is_game_over = False
                        start_time = pygame.time.get_ticks()
                        self.reset_game() 
                        pygame.mouse.set_visible(False)
                        return start_time
            self.source.blit(self.screen, [0,0])
            pygame.display.update()
    
    def reset_game(self):
        global ENEMY_SPEED
        self.current_level = 1
        self.food_remaining = 8
        self.enemy_count = 2
        self.food = []
        self.enemies = []
        self.highest_level = 1
        self.timer_text = ""
        ENEMY_SPEED = 210.0 
        unpause_background_music()
        self.initialize_level()

    def get_food_random_movement_chance(self):
        base_chance = 0.1  
        increase_per_level = 0.02  
        return base_chance + (increase_per_level * (self.current_level))

    def initialize_level(self, enemy_speed=None):
        self.food = []
        for _ in range(self.food_remaining):
            food_pixel_size = int(FOOD_DIMEN[0] * self.display.height)
            random_x = random.randint(0, self.display.width - food_pixel_size)
            random_y = random.randint(0, self.display.height - food_pixel_size)
            if random.random() < self.get_food_random_movement_chance():
                food = Food([random_x, random_y], FOOD_DIMEN, self.display, has_random_movement=True)
            else:
                food = Food([random_x, random_y], FOOD_DIMEN, self.display)
            self.food.append(food)

        self.enemies = []
        while len(self.enemies) < self.enemy_count:
            enemy_pixel_size = int(ENEMY_DIMEN[0] * self.display.height)
            edge = random.choice(["top", "bottom", "left", "right"])
            if edge == "top":
                random_x = random.randint(0, self.display.width - enemy_pixel_size)
                random_y = 0
            elif edge == "bottom":
                random_x = random.randint(0, self.display.width - enemy_pixel_size)
                random_y = self.display.height - enemy_pixel_size
            elif edge == "left":
                random_x = 0
                random_y = random.randint(0, self.display.height - enemy_pixel_size)
            else: 
                random_x = self.display.width - enemy_pixel_size
                random_y = random.randint(0, self.display.height - enemy_pixel_size)

            player_pos = self.player.rect.center
            enemy_pos = (random_x + enemy_pixel_size / 2, random_y + enemy_pixel_size / 2)
            distance = ((player_pos[0] - enemy_pos[0]) ** 2 + (player_pos[1] - enemy_pos[1]) ** 2) ** 0.5
            if distance < 450: continue
            
            enemy = Enemy([random_x, random_y], ENEMY_DIMEN, self.display, enemy_speed, level=self.current_level)
            self.enemies.append(enemy)


    def check_collisions(self, partman):
        for enemy in self.enemies:
            # 1. Normal Body Collision
            if enemy.rect.colliderect(self.player.rect):
                self.is_game_over = True
                return
            
            # 2. BOSS PROJECTILE Collision
            if enemy.state == STATE_BOSS:
                for proj in enemy.boss_projectiles:
                    if proj['rect'].colliderect(self.player.rect):
                        self.is_game_over = True
                        return

        for food in self.food:
            if food.rect.colliderect(self.player.rect):
                self.food.remove(food)
                self.shake = SHAKE_DURATION
                self.eat_sfx.play()
                if not self.food:
                    food.spit_particles(self.partman, is_last=True, mpos=pygame.mouse.get_pos())
                    self.reset_level()
                else:
                    food.spit_particles(self.partman)

        for enemy1 in self.enemies:
            for enemy2 in self.enemies:
                if enemy1 != enemy2 and enemy1.rect.colliderect(enemy2.rect):
                    if enemy1.size >= enemy2.size:
                        enemy1.increase_size_and_slow_down()
                        self.kill_sfx.play()
                        enemy2.spit_particles(partman)
                        self.enemies.remove(enemy2)
                        break 

        for enemy in self.enemies:
            for food in self.food:
                if enemy.rect.colliderect(food.rect):
                    dx = enemy.rect.centerx - food.rect.centerx
                    dy = enemy.rect.centery - food.rect.centery
                    if abs(dx) > abs(dy):
                        if dx > 0: food.rect.right = enemy.rect.left
                        else: food.rect.left = enemy.rect.right
                    else:
                        if dy > 0: food.rect.bottom = enemy.rect.top
                        else: food.rect.top = enemy.rect.bottom

    def reset_level(self):
        global ENEMY_SPEED
        self.current_level += 1
        self.food_remaining += 2 + (self.food_remaining // 3)
        self.enemy_count += 1
        self.leveled_sfx.play()
        self.highest_level = self.current_level
        if self.current_level >= 14:
            self.enemy_count = 14
            ENEMY_SPEED += 9.0 
        self.initialize_level(ENEMY_SPEED)

    def get_safe_spawn_pos(self):
        """Finds a coordinate at least 400px away from the player."""
        player_vec = pygame.math.Vector2(self.player.rect.center)
        enemy_pixel_size = int(ENEMY_DIMEN[0] * self.display.height)
        
        while True:
            rx = random.randint(0, self.display.width - enemy_pixel_size)
            ry = random.randint(0, self.display.height - enemy_pixel_size)
            pos = pygame.math.Vector2(rx, ry)
            
            # Ensure moderate distance (safe spawn)
            if pos.distance_to(player_vec) > 400:
                return [rx, ry]

    def update(self, mpos, ppartmen, dt):
        is_big_enemy_present = any(enemy.size >= 4 for enemy in self.enemies)
        
        # --- VACUUM LOGIC FIX ---
        
        # 1. First, define vacuum_enemy by looking for an existing one
        vacuum_enemy = None
        for e in self.enemies:
            if e.state == STATE_VACUUM:
                vacuum_enemy = e
                break
        
        # 2. If NO vacuum exists, check if we should trigger one
        if len(self.enemies) > 4 and vacuum_enemy is None:
            # Pick the largest enemy to be the center
            self.enemies.sort(key=lambda x: x.size, reverse=True)
            vacuum_enemy = self.enemies[0]
            vacuum_enemy.state = STATE_VACUUM
            
            # Set all others to "sucked"
            for other in self.enemies:
                if other != vacuum_enemy:
                    other.state = STATE_BEING_SUCKED
        
        # 3. Apply Vacuum Physics if we have a valid vacuum enemy
        if vacuum_enemy and vacuum_enemy in self.enemies:
            vac_pos = vacuum_enemy.pos
            for other in self.enemies:
                if other != vacuum_enemy and other.state == STATE_BEING_SUCKED:
                    direction = vac_pos - other.pos
                    dist = direction.length()
                    if dist > 0:
                        direction = direction.normalize()
                        other.pos += direction * 400.0 * dt
                        other.rect.center = round(other.pos.x), round(other.pos.y)

        # 4. Reset Check: If enemy count drops to 1, turn Vacuum back to Normal
        if len(self.enemies) <= 1:
            for e in self.enemies:
                if e.state == STATE_VACUUM:
                    e.state = STATE_CHASE 
                    e.exhaustion_timer = 20.0 

        # ---------------------------

        new_enemies_to_add = []

        for enemy in self.enemies:
            enemy.chase_player(self.player, dt)
            pygame.draw.rect(self.screen, enemy.color, enemy.rect)
            
            if enemy.shatter_pending > 0:
                count = enemy.shatter_pending
                enemy.shatter_pending = 0 
                safe_pos = self.get_safe_spawn_pos()
                enemy.pos = pygame.math.Vector2(safe_pos)
                enemy.rect.topleft = safe_pos
                for _ in range(count - 1):
                    spawn_pos = self.get_safe_spawn_pos()
                    new_enemy = Enemy(spawn_pos, ENEMY_DIMEN, self.display, level=self.current_level)
                    new_enemies_to_add.append(new_enemy)
            
            if enemy.state == STATE_BOSS:
                for proj in enemy.boss_projectiles:
                    pygame.draw.rect(self.screen, (255, 255, 200), proj['rect'])
        
        self.enemies.extend(new_enemies_to_add)
        
        for food in self.food:
            food.update_position(dt) 
            pygame.draw.rect(self.screen, food.color, food.rect)

        self.player.update_pos(mpos[0], mpos[1], dt) 

        t_min = PARTICLE_SCALE_TRAIL[0] * self.display.height
        t_max = PARTICLE_SCALE_TRAIL[1] * self.display.height
        trail_size = random.uniform(t_min, t_max)
        
        ppartmen.create(
            list(self.player.rect.center), 
            [random.randint(0, 6), random.randint(0, 6)], 
            0.4, 
            size=trail_size, 
            color=self.player.color
        )

        if is_big_enemy_present:
            self.shake = 30

        pygame.draw.rect(self.screen, self.player.color, self.player.rect)
        
        if self.shake > 0:
            self.shake -= 1
        
        if self.shake:
            self.shake_offset[0] = random.randint(0, SHAKE_INTENSITY) - SHAKE_INTENSITY
            self.shake_offset[1] = random.randint(0, SHAKE_INTENSITY) - SHAKE_INTENSITY

        self.source.blit(self.screen, self.shake_offset)