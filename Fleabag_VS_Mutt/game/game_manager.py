import random
import math
import pygame
from .player import Player
from .projectile import Projectile

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.player1 = Player(100, 400, "assets/images/character/fleabag.png", "Fleabag")
        self.player1.projectile_img = "assets/images/projectile_fleabag.png"

        self.player2 = Player(800, 400, "assets/images/character/mutt.png", "Mutt")
        self.player2.projectile_img = "assets/images/projectile_mutt.png"
        
        self.current_player = self.player1
        self.opponent = self.player2
        self.projectiles = []
        self.wind = random.uniform(-1.0, 1.0)
        self.charging = False
        self.charge_start_time = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.charging = True
            self.charge_start_time = pygame.time.get_ticks()
        elif event.type == pygame.MOUSEBUTTONUP and self.charging:
            self.charging = False
            charge_duration = (pygame.time.get_ticks() - self.charge_start_time) / 1000
            power = min(charge_duration * 10, 15)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - self.current_player.rect.centerx
            dy = self.current_player.rect.centery - mouse_y
            angle = math.atan2(dy, dx)
            proj = Projectile(
                self.current_player.rect.centerx,
                self.current_player.rect.centery,
                angle,
                power,
                self.wind,
                self.current_player.projectile_img  # different image per player
            )
            self.projectiles.append(proj)
    
    def update(self):
        # Update all projectiles
        for proj in self.projectiles[:]:  # iterate on a copy to safely remove items
            proj.update()

            # Check if projectile hits opponent
            if self.opponent.rect.colliderect(proj.rect):
                self.opponent.hit(10)  # apply damage (adjust as needed)
                self.projectiles.remove(proj)
                self.switch_turns()

            # Remove projectile if it falls below screen height
            elif proj.y > 540:
                self.projectiles.remove(proj)
                self.switch_turns()

    def draw(self):
        # Draw players
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)

        # Draw projectiles
        for proj in self.projectiles:
            proj.draw(self.screen)

    def switch_turns(self):
        # Switch current player and opponent
        self.current_player, self.opponent = self.opponent, self.current_player
        # Reset or change wind randomly
        self.wind = random.uniform(-1.0, 1.0)
