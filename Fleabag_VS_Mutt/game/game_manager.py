import math
import pygame
import random
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
        self.wind = 0
        self.charging = False
        self.charge_start_time = 0
        self.projectile_in_flight = False  # Add this flag

        self.fence_rects = [
            pygame.Rect(550, 320, 45, 270),
        ]   
        
        self.game_over = False

    def handle_event(self, event):
        if self.game_over:
            return

        # Only allow charging/firing if no projectile is in flight
        if event.type == pygame.MOUSEBUTTONDOWN and not self.projectile_in_flight:
            self.charging = True
            self.charge_start_time = pygame.time.get_ticks()
        elif event.type == pygame.MOUSEBUTTONUP and self.charging and not self.projectile_in_flight:
            self.charging = False
            charge_duration = (pygame.time.get_ticks() - self.charge_start_time) / 1000
            power = min(charge_duration * 25, 50)

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
                self.current_player.projectile_img
            )
            self.projectiles.append(proj)
            self.projectile_in_flight = True  # Block further shots until resolved
            
    def update(self):
        if self.game_over:
            return

        if not self.projectiles:
            self.projectile_in_flight = False

        for proj in self.projectiles[:]:
            proj.update()

            # Check collision with opponent
            if self.opponent.rect.colliderect(proj.rect):
                self.opponent.hit(10)
                # Check for game over immediately after hit
                if self.player1.health <= 0 or self.player2.health <= 0:
                    self.game_over = True
                self.projectiles.remove(proj)
                self.switch_turns()
                self.projectile_in_flight = False
                break

            # Check collision with fences
            hit_fence = False
            for fence in self.fence_rects:
                if proj.rect.colliderect(fence):
                    self.projectiles.remove(proj)
                    self.switch_turns()
                    self.projectile_in_flight = False  # Allow next shot
                    hit_fence = True
                    break  # no need to check other fences

            if hit_fence:
                continue  # skip further processing for this projectile

            # Remove projectile if it falls below screen
            if proj.y > self.screen.get_height():
                self.projectiles.remove(proj)
                self.switch_turns()
                self.projectile_in_flight = False  # Allow next shot

            # --- NEW: Remove projectile if it hits left or right edge ---
            elif proj.x <= 0 or proj.x >= self.screen.get_width():
                self.projectiles.remove(proj)
                self.switch_turns()
                self.projectile_in_flight = False  # Allow next shot

            if self.player1.health <= 0 or self.player2.health <= 0:
                self.game_over = True

    def draw(self):
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        for proj in self.projectiles:
            proj.draw(self.screen)

    def switch_turns(self):
        self.current_player, self.opponent = self.opponent, self.current_player
        self.wind = random.randint(-10, 10)  # Wind changes each turn