import pygame
from .game_manager import GameManager

class GameScreen:
    def __init__(self, screen, game_mode="1P"):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.game_mode = game_mode
        
        # Initialize game manager
        self.game_manager = GameManager(screen)
        
        # Game state
        self.paused = False
        self.game_over = False
        
        # Load background
        try:
            self.background = pygame.image.load("assets/images/backgrounds/background_backyard.jpg").convert()
            self.hud_image = pygame.image.load("assets/images/backgrounds/hud_top_bar.png").convert_alpha()
        except:
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((20, 20, 40))  # fallback dark color
        
        # Pause button rectangle (top-left)
        self.pause_button = pygame.Rect(10, 10, 50, 50)
        
    def draw_health_bars(self):
        # Positions and sizes - adjust to fit your HUD
        left_bar_pos = (75, 45)
        right_bar_pos = (self.screen_width - 475, 45)
        bar_width = 400
        bar_height = 27

        red = (255, 0, 0)
        green = (0, 255, 0)

        # Draw left player health bar background (red)
        pygame.draw.rect(self.screen, red, (*left_bar_pos, bar_width, bar_height))
        # Draw left player current health (green)
        health_width_left = int((self.game_manager.player1.health / 100) * bar_width)
        pygame.draw.rect(self.screen, green, (left_bar_pos[0], left_bar_pos[1], health_width_left, bar_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (*left_bar_pos, bar_width, bar_height), 2)  # border

        # Draw right player health bar background (red)
        pygame.draw.rect(self.screen, red, (*right_bar_pos, bar_width, bar_height))
        # Draw right player current health (green)
        health_width_right = int((self.game_manager.player2.health / 100) * bar_width)
        pygame.draw.rect(self.screen, green, (right_bar_pos[0], right_bar_pos[1], health_width_right, bar_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (*right_bar_pos, bar_width, bar_height), 2)  # border
    
    def handle_event(self, event):
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
            if self.pause_button.collidepoint(mx, my):
                self.paused = not self.paused
            elif not self.paused:
                # Forward other mouse events to game manager (e.g. shooting/projectiles)
                self.game_manager.handle_event(event)
        elif not self.paused:
            # Forward other events when not paused
            self.game_manager.handle_event(event)
        
    def move_current_player(self, direction):
        # Move current player left (-1) or right (1)
        current_player = self.game_manager.current_player
        move_speed = 5
        new_x = current_player.rect.x + (direction * move_speed)
        
        # Keep player inside screen horizontally
        new_x = max(0, min(new_x, self.screen_width - current_player.rect.width))
        current_player.rect.x = new_x
    
    def update(self):
        if not self.paused:
            self.game_manager.update()
    
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.hud_image, (0, 0)) 

        self.draw_health_bars()
        
        self.game_manager.player1.draw(self.screen)
        self.game_manager.player2.draw(self.screen)

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