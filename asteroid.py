import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = 0

    def draw(self, screen):
        pygame.draw.circle(screen, 'white', self.position, self.radius)

    def update(self, dt):
        # Asteroids might not need to update like players do,
        # but you can add movement or rotation logic here if needed.
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        # Create two smaller asteroids when this one splits
        if self.radius < ASTEROID_MIN_RADIUS:
            return
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        angle = random.uniform(20, 50)

        vel1 = self.velocity.rotate(angle) *1.2
        vel2 = self.velocity.rotate(-angle) *1.2

        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = vel1
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = vel2