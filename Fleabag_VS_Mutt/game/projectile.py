import pygame
import math

class Projectile:
    def __init__(self, x, y, angle, power, wind, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.x = x
        self.y = y
        self.angle = angle
        self.power = power
        self.wind = wind
        self.vx = math.cos(angle) * power + wind
        self.vy = -math.sin(angle) * power
        self.gravity = 0.5
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
