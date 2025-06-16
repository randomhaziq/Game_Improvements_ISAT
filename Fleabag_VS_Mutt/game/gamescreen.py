import pygame
import math
import random
from .game_manager import GameManager

class GameScreen:
    def __init__(self, screen, game_mode="1P", current_screen=None, background_path="assets/images/backgrounds/background_backyard.jpg", gravity=0.5):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.game_mode = game_mode
        self.winner_menu_button = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 80, 200, 60)
        self.current_screen = current_screen
        self.retry_button = pygame.Rect(self.screen_width // 3 - 100, self.screen_height // 2 + 50, 200, 50)
        self.main_menu_button = pygame.Rect(self.screen_width // 3 * 2 - 100, self.screen_height // 2 + 50, 200, 50)

        # Initialize game manager
        self.gravity = gravity
        self.game_manager = GameManager(screen, game_mode=game_mode, gravity=self.gravity)
        
        # Game state
        self.paused = False
        self.game_over = False
        
        # Load background
        try:
            self.background = pygame.image.load(background_path).convert()
            self.hud_image = pygame.image.load("assets/images/backgrounds/hud_top_bar.png").convert_alpha()
            self.pointer_image = pygame.image.load("assets/images/character/pointer_arrow.png").convert_alpha()

        except:
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((20, 20, 40))  # fallback dark color
            self.pointer_image.fill((20, 20, 40))

        # Load the wall image and x image
        try:
            self.wall_image = pygame.image.load("assets/images/wall.png").convert_alpha()
            self.x_image = pygame.image.load("assets/images/x.png").convert_alpha()
        except pygame.error:
            print("Error loading wall image. Using fallback color.")
            self.wall_image = None
            self.x_image = None

        # Pause button rectangle (top-left)
        self.pause_button = pygame.Rect(10, 10, 50, 50)

         # Example fence rectangles (x, y, width, height) — adjust to your level design
        self.fence_rects = [
            pygame.Rect(550, 320, 45, 270),
        ]   

        self.boosters = [
            # Player 1 boosters
            {"rect": pygame.Rect(72, 80, 60, 60), "desc": "Double Throws: Throw the projectile twice", "player": self.game_manager.player1},
            {"rect": pygame.Rect(160, 80, 60, 50), "desc": "Power Throw: Increase the projectile throw power", "player": self.game_manager.player1},
            {"rect": pygame.Rect(240, 80, 60, 60), "desc": "Stink Bomb: Deal damage over turns", "player": self.game_manager.player1},
            {"rect": pygame.Rect(330, 80, 60, 60), "desc": "Heal Up: Restore health points", "player": self.game_manager.player1},
            {"rect": pygame.Rect(410, 80, 60, 60), "desc": "Wall Heightened: Increase the wall height for opponent", "player": self.game_manager.player1},

            # Player 2 boosters
            {"rect": pygame.Rect(700, 80, 60, 60), "desc": "Double Throws: Throw the projectile twice", "player": self.game_manager.player2},
            {"rect": pygame.Rect(800, 80, 60, 60), "desc": "Power Throw: Increase the projectile throw power", "player": self.game_manager.player2},
            {"rect": pygame.Rect(870, 80, 60, 60), "desc": "Stink Bomb: Deal damage over turns", "player": self.game_manager.player2},
            {"rect": pygame.Rect(950, 80, 60, 60), "desc": "Heal Up: Restore health points", "player": self.game_manager.player2},
            {"rect": pygame.Rect(1040, 80, 60, 60), "desc": "Wall Heightened: Increase the wall height for opponent", "player": self.game_manager.player2},
        ]
    
    def draw_turn_indicator_triangle(self):
        # Get the current player's rect
        player_rect = self.game_manager.current_player.rect
        
        # Calculate the triangle points (a small downward triangle above player's head)
        triangle_width = 20
        triangle_height = 30
        center_x = player_rect.centerx
        top_y = player_rect.top - 10  # 10 pixels above the player's sprite
        
        # Points: left, right, bottom (pointing downward)
        points = [
            (center_x - triangle_width // 2, top_y),
            (center_x + triangle_width // 2, top_y),
            (center_x, top_y + triangle_height)
        ]
        
        pygame.draw.polygon(self.screen, (255, 0, 0), points)  # Red color

    def draw_aiming_pointer(self):
        if self.paused: 
            return
        
        # Get the current position of the mouse
        mx, my = pygame.mouse.get_pos()

        # Calculate the vector between the player's position and the mouse cursor
        player_center = self.game_manager.current_player.rect.center
        dx = mx - player_center[0]
        dy = my - player_center[1]
        
        # Calculate the angle in radians
        angle = math.atan2(dy, dx)

        # Rotate the pointer image based on the angle
        rotated_pointer = pygame.transform.rotate(self.pointer_image, -math.degrees(angle))

        # Update the rect for the rotated image
        pointer_rect = rotated_pointer.get_rect(center=(player_center[0], player_center[1] - 20))  # Move 20 pixels up

        # Draw the rotated pointer image on the screen
        self.screen.blit(rotated_pointer, pointer_rect.topleft)

    def draw_tooltip(self, text, position):
        font = pygame.font.SysFont(None, 24)
        tooltip_surface = font.render(text, True, (255, 255, 255))
        
        # Background rect behind text
        bg_rect = tooltip_surface.get_rect(topleft=(position[0] + 10, position[1] + 10))
        bg_rect.inflate_ip(10, 10)  # padding
        
        # Draw semi-transparent black background
        s = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.screen.blit(s, bg_rect.topleft)
        
        # Draw text on top
        self.screen.blit(tooltip_surface, (bg_rect.x + 5, bg_rect.y + 5))

    def check_booster_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        for booster in self.boosters:
            if booster["rect"].collidepoint(mouse_pos):
                self.draw_tooltip(booster["desc"], mouse_pos)
                break  # show only one tooltip at a time
    def draw_pause_overlay(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)  # semi-transparent
        overlay.fill((0, 0, 0))  # black
        
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.SysFont(None, 80)
        text = font.render("Game Paused", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.screen.blit(text, text_rect)

        # Draw "retry" and "main menu" options in yellow
        option_font = pygame.font.SysFont(None, 60)
        retry_text = option_font.render("Retry", True, (255, 255, 0))  # Yellow color
        menu_text = option_font.render("Main Menu", True, (255, 255, 0))  # Yellow color

        retry_rect = retry_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 100))
        menu_rect = menu_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 160))

        self.screen.blit(retry_text, retry_rect)
        self.screen.blit(menu_text, menu_rect)

        # Store the clickable areas for the retry and menu options
        self.retry_rect = retry_rect
        self.menu_rect = menu_rect

        small_font = pygame.font.SysFont(None, 36)
        small_text = small_font.render("\"Press ESC to resume\"", True, (200, 200, 200))
        small_text_rect = small_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 20))
        self.screen.blit(small_text, small_text_rect)

    def draw_health_bars(self):
        left_bar_pos = (75, 45)
        right_bar_pos = (self.screen_width - 475, 45)
        bar_width = 400
        bar_height = 27

        red = (255, 0, 0)
        green = (0, 255, 0)

        # Player 1 (left): shrink from right to left
        pygame.draw.rect(self.screen, red, (*left_bar_pos, bar_width, bar_height))
        health_width_left = int((self.game_manager.player1.health / 100) * bar_width)
        green_bar_x_left = left_bar_pos[0] + (bar_width - health_width_left)
        pygame.draw.rect(self.screen, green, (green_bar_x_left, left_bar_pos[1], health_width_left, bar_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (*left_bar_pos, bar_width, bar_height), 2)

        # Player 2 (right): shrink from left to right
        pygame.draw.rect(self.screen, red, (*right_bar_pos, bar_width, bar_height))
        health_width_right = int((self.game_manager.player2.health / 100) * bar_width)
        pygame.draw.rect(self.screen, green, (right_bar_pos[0], right_bar_pos[1], health_width_right, bar_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (*right_bar_pos, bar_width, bar_height), 2)

    def handle_event(self, event):
        if self.game_manager.input_locked:
            return  # Ignore all input while locked

        if self.game_manager.game_over:
            # Handle winner menu button click
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if self.winner_menu_button.collidepoint(mx, my):
                    self.return_to_main_menu()
                    return "menu"
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
            elif not self.paused:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.move_current_player(-1)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.move_current_player(1)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            # --- Booster click detection ---
            for booster in self.boosters:
                if booster["rect"].collidepoint(mx, my):
                    # Check if the booster belongs to the current player
                    if booster["player"] == self.game_manager.current_player:
                        self.activate_booster(booster["desc"])
                    return  # Only one booster per click

            if self.paused:
                # Check if the user clicked on "retry" or "main menu"
                if self.retry_rect.collidepoint(mx, my):
                    self.restart_game()
                elif self.menu_rect.collidepoint(mx, my):
                    self.return_to_main_menu()
                    return "menu"

            elif self.pause_button.collidepoint(mx, my):
                self.paused = not self.paused
            elif not self.paused:
                self.game_manager.handle_event(event)
    
        elif not self.paused:
            self.game_manager.handle_event(event)

    def activate_booster(self, desc):
        booster_key = desc.split()[0]
        player = self.game_manager.current_player

        if booster_key in player.used_boosters:
            return

        player.used_boosters.add(booster_key)

        if booster_key == "Double":
            self.game_manager.double_throw_active = True
        elif booster_key == "Power":
            self.game_manager.power_throw_active = True
        elif booster_key == "Stink":
            self.game_manager.stink_bomb_active = True
        elif desc.startswith("Heal Up"):
            self.game_manager.heal_up(20)
        elif booster_key == "Wall":
            self.game_manager.wall_heightened_pending = True 

    def restart_game(self):
        # Reset game state for a new round
        self.game_manager = GameManager(self.screen)  # Re-initialize the game manager
        self.paused = False  # Unpause the game

    def return_to_main_menu(self):
        self.current_screen = "menu"  # Modify current_screen directly
        self.paused = False

    def move_current_player(self, direction):
        player = self.game_manager.current_player
        step = 10  # or your movement step

        new_x = player.rect.x + (step if direction == 1 else -step)

        # Prevent going offscreen
        screen_width = self.screen.get_width()
        if new_x < 0:
            new_x = 0
        if new_x + player.rect.width > screen_width:
            new_x = screen_width - player.rect.width

        # Fence logic: Only apply to the correct player and direction
        fence = self.game_manager.fence_rects[0]  # Only one fence in your game

        if player == self.game_manager.player1:
            # Fleabag: can't move right past the left side of the fence
            if direction == 1 and player.rect.right <= fence.left and new_x + player.rect.width > fence.left:
                new_x = fence.left - player.rect.width
        elif player == self.game_manager.player2:
            # Mutt: can't move left past the right side of the fence
            if direction == -1 and player.rect.left >= fence.right and new_x < fence.right:
                new_x = fence.right

        player.rect.x = new_x
    
    def update(self):
        if self.paused or self.game_manager.game_over:
            return

        # --- AI Turn Logic for 1P Mode ---
        if (
            self.game_mode == "1P"
            and self.game_manager.current_player == self.game_manager.player1
            and not self.game_manager.projectile_in_flight
        ):
            # Only act if AI is not already moving or firing
            if not getattr(self.game_manager, "ai_action_started", False):
                # AI Booster Logic
                ai_boosters = [
                    "Double",
                    "Power",
                    "Heal",
                    "Stink",
                    "Wall"
                ]
                available_boosters = [b for b in ai_boosters if b not in self.game_manager.current_player.used_boosters]
                if available_boosters:
                    chosen_booster = random.choice(available_boosters)
                    # Pass the full description string that activate_booster expects
                    booster_desc_map = {
                        "Double": "Double Throws: Throw the projectile twice",
                        "Power": "Power Throw: Increase the projectile throw power",
                        "Heal": "Heal Up: Restore health points",
                        "Stink": "Stink Bomb: Deal damage over turns",
                        "Wall": "Wall Heightened: Increase the wall height for opponent"
                    }
                    self.activate_booster(booster_desc_map[chosen_booster])
                    self.game_manager.current_player.used_boosters.add(chosen_booster)

                # Mark that AI has started its action this turn
                self.game_manager.ai_action_started = True

                # Start AI movement/firing
                self.game_manager.ai_move()
            return

        # Reset AI action flag when it's not AI's turn
        if getattr(self.game_manager, "ai_action_started", False) and (
            self.game_manager.current_player != self.game_manager.player1
            or self.game_manager.projectile_in_flight
        ):
            self.game_manager.ai_action_started = False

        # --- Regular Game Update ---
        self.game_manager.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.hud_image, (0, 0)) 

        self.draw_health_bars()
        self.draw_wind_indicator()

        self.game_manager.player1.draw(self.screen)
        self.game_manager.player2.draw(self.screen)

        self.draw_turn_indicator_triangle()
        self.game_manager.draw()

        # Draw pause button background (light blue with purple border)
        pause_rect = pygame.Rect(10, 10, 50, 50)
        pygame.draw.rect(self.screen, (173, 216, 230), pause_rect)  # Light blue
        pygame.draw.rect(self.screen, (138, 43, 226), pause_rect, 3)  # Purple border

        # Draw pause icon (two white bars)
        bar_width, bar_height = 8, 30
        bar1_x = pause_rect.x + 12
        bar2_x = pause_rect.x + 30
        bar_y = pause_rect.y + 10
        pygame.draw.rect(self.screen, (255, 255, 255), (bar1_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (bar2_x, bar_y, bar_width, bar_height))

        if self.paused:
            self.draw_pause_overlay()

        if self.game_manager.game_over:
            self.draw_winner()
        else:
            # Only show aiming pointer if game is not over
            self.draw_aiming_pointer()

        self.check_booster_hover()

        # --- Draw fences LAST so they appear on top ---
        self.draw_fences()

        # --- Draw "x" on used boosters ---
        for booster in self.boosters:
            booster_key = booster["desc"].split()[0]  # Extract the booster name
            booster_owner = booster["player"]  # Get the owner of the booster

            # Check if the booster is used by its owner
            if booster_key in booster_owner.used_boosters:
                if self.x_image:
                    x_rect = self.x_image.get_rect(center=booster["rect"].center)
                    self.screen.blit(self.x_image, x_rect.topleft)

    def draw_winner(self):
        font = pygame.font.SysFont(None, 80)
        if self.game_manager.player1.health <= 0:
            winner_text = f"{self.game_manager.player2.name} Wins!"
        elif self.game_manager.player2.health <= 0:
            winner_text = f"{self.game_manager.player1.name} Wins!"
        else:
            return  # no winner yet
        
        text = font.render(winner_text, True, (255, 215, 0))  # gold color
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(text, text_rect)

        # Draw "Main Menu" button
        pygame.draw.rect(self.screen, (30, 144, 255), self.winner_menu_button)  # Dodger blue
        pygame.draw.rect(self.screen, (255, 255, 255), self.winner_menu_button, 3)  # White border
        btn_font = pygame.font.SysFont(None, 48)
        btn_text = btn_font.render("Main Menu", True, (255, 255, 255))
        btn_rect = btn_text.get_rect(center=self.winner_menu_button.center)
        self.screen.blit(btn_text, btn_rect)

    def draw_fences(self):
        if self.game_manager.wall_heightened_active:
            for fence in self.game_manager.fence_rects:
                if self.wall_image:
                    # Scale the wall image to match the fence dimensions
                    scaled_wall = pygame.transform.scale(self.wall_image, (fence.width, fence.height))
                    self.screen.blit(scaled_wall, (fence.x, fence.y))
                else:
                    # Fallback: Draw a black rectangle if the image is not available
                    pygame.draw.rect(self.screen, (0, 0, 0), fence)

    def draw_wind_indicator(self):
        rect_x, rect_y, rect_w, rect_h = 484, 90, 188, 51

        pygame.draw.rect(self.screen, (30, 30, 60), (rect_x, rect_y, rect_w, rect_h), border_radius=12)
        pygame.draw.rect(self.screen, (100, 100, 180), (rect_x, rect_y, rect_w, rect_h), 2, border_radius=12)

        font = pygame.font.SysFont(None, 28)
        label = font.render("Wind:", True, (255, 255, 255))
        label_rect = label.get_rect()
        label_rect.midleft = (rect_x + 15, rect_y + rect_h // 2)
        self.screen.blit(label, label_rect)

        indicator_center_x = rect_x + 125
        indicator_center_y = rect_y + rect_h // 2

        wind = self.game_manager.wind
        max_wind = 10
        arrow_max_length = 40  # Adjust as needed
        arrow_length = int((abs(wind) / max_wind) * arrow_max_length) if wind != 0 else 0
        color = (0, 191, 255)
        arrowhead_length = 14

        # Draw vertical reference lines
        # Center (tallest)
        pygame.draw.line(
            self.screen,
            (200, 200, 255),
            (indicator_center_x, rect_y + 8),
            (indicator_center_x, rect_y + rect_h - 8),
            2
        )
        # Left max (shorter)
        left_x = indicator_center_x - arrow_max_length
        pygame.draw.line(
            self.screen,
            (200, 200, 255),
            (left_x, indicator_center_y - 10),
            (left_x, indicator_center_y + 10),
            2
        )
        # Right max (shorter)
        right_x = indicator_center_x + arrow_max_length
        pygame.draw.line(
            self.screen,
            (200, 200, 255),
            (right_x, indicator_center_y - 10),
            (right_x, indicator_center_y + 10),
            2
        )

        if wind > 0:
            start = (indicator_center_x, indicator_center_y)
            line_end = (indicator_center_x + arrow_length - arrowhead_length, indicator_center_y)
            triangle_tip = (indicator_center_x + arrow_length, indicator_center_y)
            pygame.draw.line(self.screen, color, start, line_end, 5)
            pygame.draw.polygon(self.screen, color, [
                triangle_tip,
                (triangle_tip[0] - arrowhead_length, triangle_tip[1] - 8),
                (triangle_tip[0] - arrowhead_length, triangle_tip[1] + 8)
            ])
        elif wind < 0:
            start = (indicator_center_x, indicator_center_y)
            line_end = (indicator_center_x - arrow_length + arrowhead_length, indicator_center_y)
            triangle_tip = (indicator_center_x - arrow_length, indicator_center_y)
            pygame.draw.line(self.screen, color, start, line_end, 5)
            pygame.draw.polygon(self.screen, color, [
                triangle_tip,
                (triangle_tip[0] + arrowhead_length, triangle_tip[1] - 8),
                (triangle_tip[0] + arrowhead_length, triangle_tip[1] + 8)
            ])
        else:
            pygame.draw.circle(self.screen, color, (indicator_center_x, indicator_center_y), 7)
