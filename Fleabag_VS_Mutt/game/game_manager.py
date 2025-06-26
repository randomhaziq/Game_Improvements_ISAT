import math
import pygame
import random
from .player import Player
from .projectile import Projectile

class GameManager:
    def __init__(self, screen, game_mode="1P", gravity=0.5):
        self.screen = screen
        self.game_mode = game_mode
        self.gravity = gravity

        if game_mode == "1P":
            # AI is player1, human is player2
            self.player1 = Player(100, 400, "assets/images/character/fleabag.png", "Fleabag (AI)")
            self.player1.projectile_img = "assets/images/projectiles/projectile_fleabag.png"
            self.player2 = Player(800, 400, "assets/images/character/mutt.png", "Mutt (You)")
            self.player2.projectile_img = "assets/images/projectiles/projectile_mutt.png"
        else:
            # Both are humans
            self.player1 = Player(100, 400, "assets/images/character/fleabag.png", "Fleabag")
            self.player1.projectile_img = "assets/images/projectiles/projectile_fleabag.png"
            self.player2 = Player(800, 400, "assets/images/character/mutt.png", "Mutt")
            self.player2.projectile_img = "assets/images/projectiles/projectile_mutt.png"

        self.current_player = self.player1  # AI always starts in 1P mode
        self.opponent = self.player2
        self.projectiles = []
        self.wind = 0
        self.charging = False
        self.charge_start_time = 0
        self.projectile_in_flight = False  # Add this flag
        self.input_locked = False

        self.fence_rects = [
            pygame.Rect(550, 320, 45, 270),   # Existing fence
        ]   
        self.original_fence_heights = [fence.height for fence in self.fence_rects] 

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

        self.stink_bomb_active = False

        self.last_throw_valid = False  # Add this line

        # New attributes for wall heightening
        self.wall_heightened_active = False
        self.wall_heightened_turns = 0
        self.wall_heightened_pending = False 

        # Track used boosters for each player
        self.player1.used_boosters = set()
        self.player2.used_boosters = set()

    def handle_event(self, event):
        if self.game_over:
            return

        # In 1P mode, only allow input if it's player2's (human's) turn
        if self.game_mode == "1P" and self.current_player != self.player2:
            return

        # Only allow charging/firing if no projectile is in flight
        if event.type == pygame.MOUSEBUTTONDOWN and not self.projectile_in_flight:
            self.charging = True
            self.charge_start_time = pygame.time.get_ticks()
        elif event.type == pygame.MOUSEBUTTONUP and self.charging and not self.projectile_in_flight:
            self.charging = False
            charge_duration = (pygame.time.get_ticks() - self.charge_start_time) / 1000
            power = min(charge_duration * 25, 50)  # No multiplier for launching speed
            self.power_boost = 1.0  # Reset after use

            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - self.current_player.rect.centerx
            dy = self.current_player.rect.centery - mouse_y
            angle = math.atan2(dy, dx)

            # Save last throw parameters
            self.last_throw_angle = angle
            self.last_throw_power = power

            # --- Add scale for Power Throw ---
            scale = 1.4 if self.power_throw_active else 1.0

            proj = Projectile(
                self.current_player.rect.centerx,
                self.current_player.rect.centery,
                angle,
                power,
                self.wind,
                self.current_player.projectile_img,
                scale=scale
            )
            self.projectiles.append(proj)
            self.projectile_in_flight = True  # Block further shots until resolved

            # Only activate double throw if booster is active
            if self.double_throw_active:
                self.double_throw_pending = True
                self.double_throw_active = False

    def apply_stink_bomb(self):
        self.stink_bomb_turns = 3  # Damage for 3 turns

    def update(self):
        if self.game_over:
            return

        # In 1P mode, let AI act when it's player1's turn
        if self.game_mode == "1P" and self.current_player == self.player1 and not self.projectile_in_flight:
            self.ai_move()
            return

        turn_should_end = False

        if not self.projectiles:
            self.projectile_in_flight = False

        for proj in self.projectiles[:]:
            proj.update()

            # Check collision with opponent
            if self.opponent.rect.colliderect(proj.rect):
                self.handle_projectile_hit(10, self.opponent)
                if self.player1.health <= 0 or self.player2.health <= 0:
                    self.game_over = True
                self.projectiles.remove(proj)
                self.projectile_in_flight = False
                turn_should_end = True
                self.last_throw_valid = True  # Only set to True on valid hit
                break

            # Check collision with fences
            hit_fence = False
            for fence in self.fence_rects:
                if proj.rect.colliderect(fence):
                    self.projectiles.remove(proj)
                    self.projectile_in_flight = False
                    hit_fence = True
                    turn_should_end = True
                    self.last_throw_valid = False  # Not a valid hit
                    break

            if hit_fence:
                continue

            # Remove projectile if it falls below screen
            if proj.y > self.screen.get_height():
                self.projectiles.remove(proj)
                self.projectile_in_flight = False
                turn_should_end = True
                self.last_throw_valid = False  # Not a valid hit

            # Remove projectile if it hits left or right edge
            elif proj.x <= 0 or proj.x >= self.screen.get_width():
                self.projectiles.remove(proj)
                self.projectile_in_flight = False
                turn_should_end = True
                self.last_throw_valid = False  # Not a valid hit

            if self.player1.health <= 0 or self.player2.health <= 0:
                self.game_over = True

        # Handle double throw
        if self.double_throw_pending and not self.projectile_in_flight:
            self.input_locked = True
            self.repeat_last_throw()
            self.double_throw_pending = False
            turn_should_end = False

        # After the second throw finishes:
        if self.input_locked and not self.projectile_in_flight and not self.double_throw_pending:
            self.input_locked = False
            turn_should_end = True

        # Only switch turns if all throws are done and not pending
        if turn_should_end and not self.projectile_in_flight and not self.double_throw_pending and not self.input_locked:
            self.switch_turns()

    def draw(self):
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        for proj in self.projectiles:
            proj.draw(self.screen)

    def switch_turns(self):
        # Reset boosters that should only last for one turn
        self.double_throw = False
        self.power_boost = 1.0
        self.power_throw_active = False
        self.double_throw_active = False
        self.double_throw_pending = False
        self.stink_bomb_active = False

        self.current_player, self.opponent = self.opponent, self.current_player
        self.wind = random.randint(-10, 10)
        # Apply DOT at the start of the new current player's turn
        if hasattr(self.current_player, "stink_bomb_turns") and self.current_player.stink_bomb_turns > 0:
            self.current_player.hit(10)
            self.current_player.stink_bomb_turns -= 1

        # --- Wall booster logic ---
        # 1. If pending, heighten now for this new turn
        if self.wall_heightened_pending:
            self.heighten_fences(amount=60)
            self.wall_heightened_active = True
            self.wall_heightened_turns = 1
            self.wall_heightened_pending = False

        # 2. If active, decrement and revert if expired
        elif self.wall_heightened_active:
            self.wall_heightened_turns -= 1
            if self.wall_heightened_turns <= 0:
                self.wall_heightened_active = False
                for fence, orig_height in zip(self.fence_rects, self.original_fence_heights):
                    fence.y += (fence.height - orig_height)
                    fence.height = orig_height

    def handle_projectile_hit(self, damage, target):
        # Apply power throw booster to damage only
        if self.power_throw_active:
            damage = int(damage * 2.5)
            self.power_throw_active = False  # Reset after use
        if self.stink_bomb_active:
            target.stink_bomb_turns = 3
            self.stink_bomb_active = False
        target.hit(damage)

    def repeat_last_throw(self):
        # --- Add scale for Power Throw if needed ---
        scale = 1.5 if self.power_throw_active else 1.0
        proj = Projectile(
            self.current_player.rect.centerx,
            self.current_player.rect.centery,
            self.last_throw_angle,
            self.last_throw_power,
            self.wind,
            self.current_player.projectile_img,
            scale=scale
        )
        self.projectiles.append(proj)
        self.projectile_in_flight = True

    def heal_up(self, amount=20):
        self.current_player.health = min(self.current_player.health + amount, 100)  # Assuming max health is 100

    def heighten_fences(self, amount=60):
        for i, fence in enumerate(self.fence_rects):
            if fence.height == self.original_fence_heights[i]:
                fence.height += amount
                fence.y -= amount  # Move up so the bottom stays in place

    def ai_move(self):
        # Randomly decide to move left or right for a few steps before firing
        steps = random.randint(1, 5)
        direction = random.choice([-1, 1])
        step_size = 10
        min_y = 320  # Minimum y position to avoid going too low

        for _ in range(steps):
            new_x = self.current_player.rect.x + direction * step_size
            if 0 < new_x < self.screen.get_width() - self.current_player.rect.width:
                self.current_player.rect.x = new_x

        # Try up to 10 times to get a shot that reaches at least min_y
        for _ in range(10):
            angle = random.uniform(0.5, 1.2)
            power = random.uniform(15, 35) * 0.6  # Reduced AI power
            velocity_scale = 10  # Use your game's scale if different
            vy = -math.sin(angle) * power * velocity_scale
            gravity = 9.81  # Use your game's gravity

            # Calculate peak y position (lower y is higher on screen)
            start_y = self.current_player.rect.centery
            peak_y = start_y + (vy ** 2) / (2 * gravity)  # downward is positive

            if peak_y <= min_y:
                break  # Found a suitable shot

        proj = Projectile(
            self.current_player.rect.centerx,
            self.current_player.rect.centery,
            angle,
            power,
            self.wind,
            self.current_player.projectile_img,
            scale=1.0
        )
        self.projectiles.append(proj)
        self.projectile_in_flight = True

    def update_projectile(self, projectile):
        projectile.vy += self.gravity
        projectile.y += projectile.vy

    def restart_game(self):
        # Re-initialize the GameManager (and optionally GameScreen if needed)
        self.game_manager = GameManager(self.screen, self.game_mode, gravity=self.gravity)
        # Reset any other GameScreen state if needed
        self.paused = False
        # If you have other state variables (like self.winner, etc.), reset them here