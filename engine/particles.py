import random
import pygame
from engine.settings import *

class ParticleManager:
    def __init__(self) -> None:
        self.particle_list = []
    
    def getall(self) -> list:
        return [particle for particle in self.particle_list]
    
    def clear(self):
        self.particle_list = []

    def update(self, dt, gravity=False, grav=GRAVITY) -> None:
        for particle in self.particle_list[:]:
            particle.pos[0] += particle.vel[0] * dt
            particle.pos[1] += particle.vel[1] * dt

            if gravity:
                particle.vel[1] += grav * dt

            particle.span -= dt

            if particle.span <= 0:
                self.particle_list.remove(particle)
    
    # UPDATED: Added 'size' parameter
    def create(self, position:list, max_velocity:list, max_lifespan_percent:float, size:float, color=(255, 255, 255)) -> None:
        scale = 120 
        
        vx = random.uniform((max_velocity[0]*-1)*2, max_velocity[0]+2) * scale
        vy = random.uniform((max_velocity[1]*-1)*2, max_velocity[1]+2) * scale
        rand_vel = [vx, vy]
        
        base_seconds = 5.0
        max_lifespan = base_seconds * max_lifespan_percent
        lifespan = random.uniform(0.1, max_lifespan)
        
        # Pass size to the particle
        particle = Particle(list(position), rand_vel, lifespan, size, color=color)
        self.particle_list.append(particle)
        return particle
        

class Particle:
    # UPDATED: Stores 'size'
    def __init__(self, position:list, velocity:list, lifespan:float, size:float, color=(255, 255, 255)) -> None:
        self.pos = position
        self.vel = velocity
        self.span = lifespan 
        self.size = size # The calculated pixel size
        self.color = color