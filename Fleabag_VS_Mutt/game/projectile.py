import pygame
import math

class Projectile:
    GRAVITY = 9.81  # pixels per second^2 (adjust as needed)

    def __init__(self, x, y, angle, power, wind, image_path):
        self.x = x
        self.y = y
        self.angle = angle
        self.power = power
        self.wind = wind
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        # Velocity components (pixels per frame)
        velocity_scale = 50

        self.vx = math.cos(angle) * power * velocity_scale
        self.vy = -math.sin(angle) * power  * velocity_scale 

        self.time = 0  # elapsed time since throw

    def update(self):
        dt = 1 / 60  # assuming 60 FPS; if you want accurate, pass delta time instead
        self.time += dt

        # Update position with basic projectile motion + wind acceleration horizontally
        self.x += self.vx * dt + self.wind * self.time * dt
        self.y += self.vy * dt + 0.5 * Projectile.GRAVITY * (self.time ** 2)

        self.rect.center = (int(self.x), int(self.y))

        # Update rect position for collision detection
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        
    
