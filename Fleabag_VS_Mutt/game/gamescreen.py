import pygame
import math
from .game_manager import GameManager

class GameScreen:
    def __init__(self, screen, game_mode="1P", current_screen=None):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.game_mode = game_mode
        self.winner_menu_button = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 80, 200, 60)
        self.current_screen = current_screen
        self.retry_button = pygame.Rect(self.screen_width // 3 - 100, self.screen_height // 2 + 50, 200, 50)
        self.main_menu_button = pygame.Rect(self.screen_width // 3 * 2 - 100, self.screen_height // 2 + 50, 200, 50)

        # Initialize game manager
        self.game_manager = GameManager(screen)
        
        # Game state
        self.paused = False
        self.game_over = False
        
        # Load background
        try:
            self.background = pygame.image.load("assets/images/backgrounds/background_backyard.jpg").convert()
            self.hud_image = pygame.image.load("assets/images/backgrounds/hud_top_bar.png").convert_alpha()
            self.pointer_image = pygame.image.load("assets/images/character/pointer_arrow.png").convert_alpha()

        except:
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((20, 20, 40))  # fallback dark color
            self.pointer_image.fill((20, 20, 40))

        # Pause button rectangle (top-left)
        self.pause_button = pygame.Rect(10, 10, 50, 50)

         # Example fence rectangles (x, y, width, height) — adjust to your level design
        self.fence_rects = [
            pygame.Rect(550, 320, 45, 270),
        ]   

        self.boosters = [
            {"rect": pygame.Rect(72, 80, 60, 60), "desc": "Double Throws: Throw an object twice"},
            {"rect": pygame.Rect(160, 80, 60, 50), "desc": "Power Throw: Increase the projectile throw power"},
            {"rect": pygame.Rect(240, 80, 60, 60), "desc": "Stink Bomb: Deal damage over time"},
            {"rect": pygame.Rect(330, 80, 60, 60), "desc": "Heal Up: Restore health points"},
            {"rect": pygame.Rect(410, 80, 60, 60), "desc": "Wall Heightened: Increase the wall height"},

            {"rect": pygame.Rect(700, 80, 60, 60), "desc": "Double Throws: Throw an object twice"},
            {"rect": pygame.Rect(800, 80, 60, 60), "desc": "Power Throw: Increase the projectile throw power"},
            {"rect": pygame.Rect(870, 80, 60, 60), "desc": "Stink Bomb: Deal damage over time"},
            {"rect": pygame.Rect(950, 80, 60, 60), "desc": "Heal Up: Restore health points"},
            {"rect": pygame.Rect(1040, 80, 60, 60), "desc": "Wall Heightened: Increase the wall height"},
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
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
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

    def restart_game(self):
        # Reset game state for a new round
        self.game_manager = GameManager(self.screen)  # Re-initialize the game manager
        self.paused = False  # Unpause the game

    def return_to_main_menu(self):
        self.current_screen = "menu"  # Modify current_screen directly
        self.paused = False

    def move_current_player(self, direction):
        # Move current player left (-1) or right (1)
        current_player = self.game_manager.current_player
        move_speed = 5
        new_x = current_player.rect.x + (direction * move_speed)
        
        # Keep player inside screen horizontally
        new_x = max(0, min(new_x, self.screen_width - current_player.rect.width))
        current_player.rect.x = new_x
    
    def update(self):
        if not self.paused and not self.game_manager.game_over:
          self.game_manager.update()
    
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.hud_image, (0, 0)) 

        self.draw_health_bars()
        self.draw_wind_indicator()  # <-- Add this line

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
        for fence in self.fence_rects:
            pygame.draw.rect(self.screen, (255, 0, 0), fence, 2)  # red outline

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
