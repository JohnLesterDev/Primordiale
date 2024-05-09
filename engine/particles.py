import random

from engine.settings import *

class ParticleManager:
    def __init__(self) -> None:
        self.particle_list = []
    
    def getall(self) -> list:
        return [particle for particle in self.particle_list]

    def update(self, gravity=False, grav=GRAVITY) -> None:
        for particle in self.particle_list:
            particle.pos[0] += particle.vel[0]
            particle.pos[1] += particle.vel[1]

            if gravity:
                particle.vel[1] += grav

            if particle.span <= 0:
                self.particle_list.remove(particle)
            else:
                particle.span -= 0.7
    
    def create(self, position:list, max_velocity:list, max_lifespan_percent:float, color=(255, 255, 255)) -> None:
        rand_vel = [
            random.uniform((max_velocity[0]*-1)*2,max_velocity[0]+2),
            random.uniform((max_velocity[1]*-1)*2,max_velocity[1]+2)
            ]
        
        max_lifespan = (FPS / 2) * max_lifespan_percent
        
        lifespan = random.uniform(FPS / 2, max_lifespan)
        
        particle = Particle(position, rand_vel, lifespan, color=color)
        self.particle_list.append(particle)

        return particle
        

class Particle:
    def __init__(self, position:list, velocity:list, lifespan:int, color=(255, 255, 255)) -> None:
        self.pos = position
        self.vel = velocity
        self.span = lifespan
        self.color = color