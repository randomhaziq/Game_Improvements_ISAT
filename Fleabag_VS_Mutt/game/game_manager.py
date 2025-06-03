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
        self.fence_rect = None  # Add fence rectangle
        
        # Booster states
        self.boosters = {
            'double_throw': False,
            'power_boost': False,
            'stink_bomb': False
        }
    def can_move_player(self, player, new_x):
        if not self.fence_rect:
            # If no fence set, no restriction
            return True

        fence_left = self.fence_rect.x - player.rect.width - 10
        fence_right = self.fence_rect.x + self.fence_rect.width + 10

        screen_width = self.screen.get_width()

        # Check if new_x is within screen bounds
        if new_x < 0 or new_x > screen_width - player.rect.width:
            return False

        # Fence collision logic:
        if player.rect.x < fence_left and new_x > fence_left:
            return False
        if player.rect.x > fence_right and new_x < fence_right:
            return False

        return True

    def set_fence(self, fence_rect):
        self.fence_rect = fence_rect

    def apply_booster(self, booster_name, active):
        if booster_name in self.boosters:
            self.boosters[booster_name] = active

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.charging = True
            self.charge_start_time = pygame.time.get_ticks()
        elif event.type == pygame.MOUSEBUTTONUP and self.charging:
            self.charging = False
            charge_duration = (pygame.time.get_ticks() - self.charge_start_time) / 1000
            
            # Apply power boost if active
            base_power = min(charge_duration * 10, 15)
            power = base_power * 1.5 if self.boosters['power_boost'] else base_power
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - self.current_player.rect.centerx
            dy = self.current_player.rect.centery - mouse_y
            angle = math.atan2(dy, dx)
            
            # Create projectile(s)
            proj = Projectile(
                self.current_player.rect.centerx,
                self.current_player.rect.centery,
                angle,
                power,
                self.wind,
                self.current_player.projectile_img
            )
            self.projectiles.append(proj)
            
            # Double throw booster
            if self.boosters['double_throw']:
                # Create second projectile with slightly different angle
                angle2 = angle + 0.2  # Small angle offset
                proj2 = Projectile(
                    self.current_player.rect.centerx,
                    self.current_player.rect.centery,
                    angle2,
                    power,
                    self.wind,
                    self.current_player.projectile_img
                )
                self.projectiles.append(proj2)
                self.boosters['double_throw'] = False  # Reset after use
            
            # Stink bomb effect (larger damage area)
            if self.boosters['stink_bomb']:
                proj.is_stink_bomb = True
                self.boosters['stink_bomb'] = False  # Reset after use
            
            # Reset power boost after use
            if self.boosters['power_boost']:
                self.boosters['power_boost'] = False
    
    def update(self):
        # Update all projectiles
        for proj in self.projectiles[:]:  # iterate on a copy to safely remove items
            proj.update()

            # Check if projectile hits fence/obstacle
            if self.fence_rect and self.fence_rect.colliderect(proj.rect):
                self.projectiles.remove(proj)
                self.switch_turns()
                continue

            # Check if projectile hits opponent
            if self.opponent.rect.colliderect(proj.rect):
                damage = 10
                
                # Check for stink bomb effect (larger damage)
                if hasattr(proj, 'is_stink_bomb') and proj.is_stink_bomb:
                    damage = 20
                
                self.opponent.hit(damage)
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