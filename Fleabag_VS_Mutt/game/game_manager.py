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
        self.input_locked = False

        self.fence_rects = [
            pygame.Rect(550, 320, 45, 270),
        ]   
        
        self.game_over = False

        # --- NEW: Power-up attributes ---
        self.double_throw = False
        self.power_boost = 1.0
        self.stink_bomb_turns = 0
        self.power_throw_active = False
        self.double_throw_active = False
        self.double_throw_pending = False  # To track if second throw should happen

        self.last_throw_angle = 0
        self.last_throw_power = 0

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
            power = min(charge_duration * 25, 50) * self.power_boost
            self.power_boost = 1.0  # Reset after use

            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - self.current_player.rect.centerx
            dy = self.current_player.rect.centery - mouse_y
            angle = math.atan2(dy, dx)

            # Save last throw parameters
            self.last_throw_angle = angle
            self.last_throw_power = power

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
            
    def apply_stink_bomb(self):
        self.stink_bomb_turns = 3  # Damage for 3 turns

    def update(self):
        if self.game_over:
            return

        turn_should_end = False

        if not self.projectiles:
            self.projectile_in_flight = False

        for proj in self.projectiles[:]:
            proj.update()

            # Check collision with opponent
            if self.opponent.rect.colliderect(proj.rect):
                self.handle_projectile_hit(20, self.opponent)
                if self.player1.health <= 0 or self.player2.health <= 0:
                    self.game_over = True
                self.projectiles.remove(proj)
                self.projectile_in_flight = False
                turn_should_end = True  # Mark turn to end after double throw check
                break

            # Check collision with fences
            hit_fence = False
            for fence in self.fence_rects:
                if proj.rect.colliderect(fence):
                    self.projectiles.remove(proj)
                    self.projectile_in_flight = False
                    hit_fence = True
                    turn_should_end = True
                    break

            if hit_fence:
                continue

            # Remove projectile if it falls below screen
            if proj.y > self.screen.get_height():
                self.projectiles.remove(proj)
                self.projectile_in_flight = False
                turn_should_end = True

            # Remove projectile if it hits left or right edge
            elif proj.x <= 0 or proj.x >= self.screen.get_width():
                self.projectiles.remove(proj)
                self.projectile_in_flight = False
                turn_should_end = True

            if self.player1.health <= 0 or self.player2.health <= 0:
                self.game_over = True

        if self.stink_bomb_turns > 0:
            self.opponent.hit(5)
            self.stink_bomb_turns -= 1

        # Handle double throw
        if self.double_throw_pending and not self.projectile_in_flight:
            self.input_locked = True
            self.repeat_last_throw()  # Start the second throw
            self.double_throw_pending = False
            turn_should_end = False  # Don't end turn yet

        # After the second throw finishes:
        if self.input_locked and not self.projectile_in_flight and not self.double_throw_pending:
            self.input_locked = False
            turn_should_end = True  # Now end turn

        # Only switch turns if all throws are done and not pending
        if turn_should_end and not self.projectile_in_flight and not self.double_throw_pending and not self.input_locked:
            self.switch_turns()

    def draw(self):
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        for proj in self.projectiles:
            proj.draw(self.screen)

    def switch_turns(self):
        self.current_player, self.opponent = self.opponent, self.current_player
        self.wind = random.randint(-10, 10)  # Wind changes each turn

    def handle_projectile_hit(self, damage, target):
        # If power throw is active, increase damage
        if self.power_throw_active:
            damage = int(damage * 2.0)
            self.power_throw_active = False  # Only for one turn
        if self.double_throw_active:
            self.double_throw_pending = True  # Schedule a second throw
            self.double_throw_active = False  # Only for one hit
        target.hit(damage)

    def repeat_last_throw(self):
        proj = Projectile(
            self.current_player.rect.centerx,
            self.current_player.rect.centery,
            self.last_throw_angle,
            self.last_throw_power,
            self.wind,
            self.current_player.projectile_img
        )
        self.projectiles.append(proj)
        self.projectile_in_flight = True