import pygame

class Player:
    def __init__(self, x, y, image_path, name):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 100
        self.name = name

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def hit(self, damage):
        self.health = max(self.health - damage, 0)
