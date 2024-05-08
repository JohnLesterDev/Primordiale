import pygame
import random

from engine.settings import *

class ParticleManager:
    def __init__(self) -> None:
        self.particle_list = []

    def update(self) -> None:
        for particle in self.particle_list:
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]

            if self.span <= 0:
                self.particle_list.remove(particle)
            else:
                self.span -= 0.9
    
    def create(self, position:list, max_velocity:list, max_lifespan_percent:float) -> None:
        rand_vel = [
            random.randint(max_velocity[0]*-1,max_velocity[0]),
            random.randint(max_velocity[1]*-1,max_velocity[1])
            ]
        
        max_lifespan = (FPS / 2) * max_lifespan_percent
        
        lifespan = random.uniform(FPS / 2, max_lifespan)
        
        particle = Particle(position, rand_vel, lifespan)
        self.particle_list.append(particle)
        

class Particle:
    def __init__(self, position:list, velocity:list, lifespan:int) -> None:
        self.pos = position
        self.vel = velocity
        self.span = lifespan