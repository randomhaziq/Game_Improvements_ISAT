import pygame
from game.gamescreen import GameScreen  # import your GameScreen class

pygame.init()
screen = pygame.display.set_mode((1152, 588))
pygame.display.set_caption("Fleabag vs Mutt")

menu_bg = pygame.image.load("assets/images/backgrounds/main_interface.jpg").convert()
choose_game_bg = pygame.image.load("assets/images/backgrounds/choose_game_interface.jpg").convert()
choose_customize_1p_bg = pygame.image.load("assets/images/backgrounds/customization_interface_1p.jpg").convert()
choose_customize_2p_bg = pygame.image.load("assets/images/backgrounds/customization_interface_2p.jpg").convert()

# Buttons as before
play_main_button = pygame.Rect(223, 387, 300, 70)
background_button = pygame.Rect(639, 387, 300, 70)
howto_button = pygame.Rect(215, 493, 300, 70)
setting_button = pygame.Rect(645, 493, 300, 70)

mode_button_1 = pygame.Rect(365, 240, 175, 180)
mode_button_2 = pygame.Rect(565, 240, 200, 180)
back_mode_button = pygame.Rect(37, 30, 131, 46)

play_customize_button_1p = pygame.Rect(400, 495, 363, 80)
customize_button_1p = pygame.Rect(465, 175, 233, 175)
back_customize_button_1p = pygame.Rect(46, 10, 123, 40)

play_customize_button_2p = pygame.Rect(400, 495, 363, 80)
dog_customize_button_2p = pygame.Rect(365, 175, 206, 190)
cat_customize_button_2p = pygame.Rect(590, 175, 206, 190)
back_customize_button_2p = pygame.Rect(46, 10, 123, 40)

clock = pygame.time.Clock()

# Track current screen
current_screen = "menu"

# Add a variable for GameScreen instance, will be initialized when starting game
game_screen = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle events based on current screen
        if current_screen == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if play_main_button.collidepoint(mx, my):
                    current_screen = "choose_game"
                elif background_button.collidepoint(mx, my):
                    pass
                elif howto_button.collidepoint(mx, my):
                    pass
                elif setting_button.collidepoint(mx, my):
                    pass
        
        elif current_screen == "choose_game":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if mode_button_1.collidepoint(mx, my):
                    current_screen = "choose_customize_1p"
                elif mode_button_2.collidepoint(mx, my):
                    current_screen = "choose_customize_2p"
                elif back_mode_button.collidepoint(mx, my):
                    current_screen = "menu"
        
        elif current_screen == "choose_customize_1p":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if play_customize_button_1p.collidepoint(mx, my):
                    # Start 1P game: create game screen instance with "1P" mode
                    game_screen = GameScreen(screen, game_mode="1P")
                    current_screen = "game"
                elif customize_button_1p.collidepoint(mx, my):
                    pass  # your customize logic here
                elif back_customize_button_1p.collidepoint(mx, my):
                    current_screen = "choose_game"
        
        elif current_screen == "choose_customize_2p":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if play_customize_button_2p.collidepoint(mx, my):
                    # Start 2P game: create game screen instance with "2P" mode
                    game_screen = GameScreen(screen, game_mode="2P")
                    current_screen = "game"
                elif cat_customize_button_2p.collidepoint(mx, my):
                    pass  # cat selection logic here
                elif dog_customize_button_2p.collidepoint(mx, my):
                    pass  # dog selection logic here
                elif back_customize_button_2p.collidepoint(mx, my):
                    current_screen = "choose_game"
        
        elif current_screen == "game":
            # Pass event to game screen handler
            result = game_screen.handle_event(event)
            if result == "pause_menu":
                # Simple pause menu: go back to main menu or implement pause screen as needed
                current_screen = "menu"
                game_screen = None  # discard current game screen
                
    # Drawing section
    if current_screen == "menu":
        screen.blit(menu_bg, (0, 0))
    elif current_screen == "choose_game":
        screen.blit(choose_game_bg, (0, 0))
    elif current_screen == "choose_customize_1p":
        screen.blit(choose_customize_1p_bg, (0, 0))
    elif current_screen == "choose_customize_2p":
        screen.blit(choose_customize_2p_bg, (0, 0))
    elif current_screen == "game":
        # Update and draw the game screen
        game_screen.update()
        game_screen.draw()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
