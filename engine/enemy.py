import random
import pygame
import math 
from engine.food import Food
from engine.settings import *

STATE_CHASE = "chase"
STATE_BAIT = "bait"
STATE_STALK = "stalk"
STATE_RAGE = "rage"

STATE_WARNING = "warning" 
STATE_SPASM = "spasm"     
STATE_VIPER = "viper"     
STATE_ORBIT = "orbit"     
STATE_BOSS = "boss"       

# --- NEW STATES ---
STATE_VACUUM = "vacuum"         # The one sucking others in
STATE_BEING_SUCKED = "sucked"   # The ones being eaten

class Enemy(Food):
    def __init__(self, position, dimension, display, enemy_speed=None, level=1):
        super().__init__(position, dimension, display)
        self.original_color = (189, 25, 23)
        self.color = list(self.original_color)
        
        self.base_speed = enemy_speed if enemy_speed else ENEMY_SPEED
        self.current_speed = self.base_speed
        self.size = 1 
        self.level_difficulty = level 
        
        self.pos = pygame.math.Vector2(self.rect.center)
        self.vel = pygame.math.Vector2(0, 0)
        
        self.state = STATE_CHASE
        self.state_timer = pygame.time.get_ticks()
        self.state_duration = random.randint(500, 2000)
        
        self.wiggle_timer = random.random() * 100
        self.blink_timer = 0
        
        # --- BOSS VARIABLES ---
        self.exhaustion_timer = 0.0     
        self.boss_projectiles = []      
        self.boss_timer = 0.0     
        self.shatter_pending = 0 

    def decide_brain(self):
        # If being sucked or acting as vacuum, DO NOT change state automatically
        if self.state in [STATE_VACUUM, STATE_BEING_SUCKED]:
            return

        now = pygame.time.get_ticks()
        
        # 1. BOSS STATE END CHECK
        if self.state == STATE_BOSS:
             if now - self.state_timer > self.state_duration:
                self.state = STATE_CHASE
                self.state_timer = now
                self.shatter_pending = self.size 
                self.size = 1
                self.rect.size = (int(ENEMY_DIMEN[0] * self.display.height), int(ENEMY_DIMEN[1] * self.display.height))
                self.boss_projectiles = [] 
                self.exhaustion_timer = 0 
                self.base_speed = ENEMY_SPEED 
                self.color = list(self.original_color)
                return

        if now - self.state_timer > self.state_duration:
            self.state_timer = now
            
            # 2. BOSS TRIGGER CHECK
            if self.size >= 3 and self.exhaustion_timer > 15.0:
                self.state = STATE_BOSS
                self.state_duration = 8000 
                self.boss_timer = 0.0
                self.init_boss_projectiles()
                self.color = [255, 140, 0] 
                return 

            # Default choices 
            choices = [STATE_CHASE, STATE_BAIT, STATE_STALK, STATE_RAGE]
            weights = [60, 15, 10, 15]
            
            if self.level_difficulty >= 4:
                choices.extend([STATE_WARNING, STATE_VIPER, STATE_ORBIT])
                chaos_weight = min((self.level_difficulty - 4) * 5, 40)
                weights = [40, 10, 5, 15, 15 + chaos_weight, 10 + chaos_weight, 10 + chaos_weight]

            self.state = random.choices(choices, weights=weights, k=1)[0]
            
            level_bonus_time = self.level_difficulty * 100
            
            if self.state == STATE_RAGE:
                self.state_duration = random.randint(400, 800)
            elif self.state == STATE_WARNING:
                self.state_duration = 1500 
            elif self.state == STATE_VIPER:
                self.state_duration = random.randint(1500, 3000) + level_bonus_time
            elif self.state == STATE_ORBIT:
                self.state_duration = random.randint(2000, 4000) + level_bonus_time
            else:
                self.state_duration = random.randint(1000, 3000)

    def init_boss_projectiles(self):
        self.boss_projectiles = []
        count = self.size * 3
        p_size = int(self.rect.width * 0.3)
        for i in range(count):
            angle = (360 / count) * i
            self.boss_projectiles.append({
                'angle': angle,
                'dist': self.rect.width * 1.5, 
                'rect': pygame.Rect(0, 0, p_size, p_size),
                'pos': pygame.math.Vector2(0, 0),
                'vel': pygame.math.Vector2(0, 0),
                'speed': 100.0,                   
                'launched': False                 
            })

    def chase_player(self, player, dt):
        self.exhaustion_timer += dt
        
        # Disable brain if we are in a forced event state
        if self.state not in [STATE_SPASM, STATE_VACUUM, STATE_BEING_SUCKED]:
            self.decide_brain()

        player_vec = pygame.math.Vector2(player.rect.center)
        enemy_vec = self.pos
        
        direction = player_vec - enemy_vec
        distance = direction.length()
        
        if distance > 0:
            norm_dir = direction.normalize()
        else:
            norm_dir = pygame.math.Vector2(0, 0)

        # --- FORCE COMBINE STATES ---
        if self.state == STATE_VACUUM:
            # The "Black Hole" moves slowly to the center of the screen to feast
            center_screen = pygame.math.Vector2(self.display.width/2, self.display.height/2)
            to_center = center_screen - self.pos
            if to_center.length() > 5:
                self.vel = to_center.normalize() * (self.base_speed * 0.5)
            else:
                self.vel = pygame.math.Vector2(0, 0)
            
            self.color = [20, 0, 20] # Very dark purple/black
            
        elif self.state == STATE_BEING_SUCKED:
            # Do nothing here. 
            # The LevelManager will apply the suction force manually.
            self.vel = pygame.math.Vector2(0, 0)
            self.color = [100, 100, 255] # Blueish (helpless)
            # We don't apply velocity here to avoid conflicting with the level logic
            return 

        # --- BOSS LOGIC ---
        elif self.state == STATE_BOSS:
            self.boss_timer += dt
            if self.boss_timer < 3.5:
                self.vel = pygame.math.Vector2(0, 0)
                for p in self.boss_projectiles:
                    p['angle'] += 200 * dt 
                    rad = math.radians(p['angle'])
                    p['pos'].x = self.pos.x + math.cos(rad) * p['dist']
                    p['pos'].y = self.pos.y + math.sin(rad) * p['dist']
                    p['rect'].center = (round(p['pos'].x), round(p['pos'].y))
            else:
                self.vel = pygame.math.Vector2(0, 0)
                for p in self.boss_projectiles:
                    if not p['launched']:
                        p['launched'] = True
                        rad = math.radians(p['angle'])
                        p['vel'] = pygame.math.Vector2(math.cos(rad), math.sin(rad))
                        p['speed'] = 150.0 
                    p['speed'] += 300.0 * dt 
                    if self.boss_timer < 5.5:
                        p_center = pygame.math.Vector2(p['rect'].center)
                        target_dir = (player_vec - p_center)
                        if target_dir.length() > 0:
                            p['vel'] = p['vel'].lerp(target_dir.normalize(), 0.08).normalize()
                    p['pos'] += p['vel'] * p['speed'] * dt
                    p['rect'].center = (round(p['pos'].x), round(p['pos'].y))

        # --- STANDARD MOVEMENTS ---
        elif self.state == STATE_CHASE:
            self.current_speed = self.base_speed
            self.vel = norm_dir * self.current_speed
            self.color = [189, 25, 23]
        elif self.state == STATE_BAIT:
            self.current_speed = self.base_speed * 0.8
            self.vel = -norm_dir * self.current_speed
            self.color = [200, 100, 100]
        elif self.state == STATE_STALK:
            self.vel = pygame.math.Vector2(0, 0)
            self.color = [100, 0, 0]
        elif self.state == STATE_RAGE:
            self.current_speed = self.base_speed * 3.0
            self.vel = norm_dir * self.current_speed
            self.color = [255, 50, 50]
        elif self.state == STATE_WARNING:
            self.vel = pygame.math.Vector2(0, 0)
            self.blink_timer += dt
            if int(self.blink_timer * 20) % 2 == 0: self.color = [255, 255, 255]
            else: self.color = [50, 50, 50]
            if pygame.time.get_ticks() - self.state_timer > self.state_duration:
                self.state = STATE_SPASM
                self.state_duration = 9999999
        elif self.state == STATE_SPASM:
            self.current_speed = self.base_speed * 0.6
            approach = norm_dir * self.current_speed
            jitter = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            self.vel = approach + (jitter * 600.0)
            self.color = [200, 200, 255]
        elif self.state == STATE_VIPER:
            self.current_speed = self.base_speed * 1.3
            perp = pygame.math.Vector2(-norm_dir.y, norm_dir.x)
            self.wiggle_timer += dt * 10
            wiggle = math.sin(self.wiggle_timer) * 350.0
            self.vel = (norm_dir * self.current_speed) + (perp * wiggle)
            self.color = [160, 32, 240] 
        elif self.state == STATE_ORBIT:
            self.current_speed = self.base_speed * 1.6
            perp = pygame.math.Vector2(-norm_dir.y, norm_dir.x)
            self.vel = (perp * self.current_speed * 0.85) + (norm_dir * self.current_speed * 0.15)
            self.color = [0, 255, 255]

        # Physics Application
        if self.state != STATE_BOSS: 
             self.pos += self.vel * dt
             self.rect.center = round(self.pos.x), round(self.pos.y)
        elif self.state == STATE_BOSS and self.boss_timer < 3.5:
             self.rect.center = round(self.pos.x), round(self.pos.y)

    def increase_size_and_slow_down(self):
        self.size += 1
        self.rect.inflate_ip(ENEMY_INFLATE_SIZE, ENEMY_INFLATE_SIZE)
        self.base_speed *= 0.9