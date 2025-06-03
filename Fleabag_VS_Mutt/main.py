import pygame
from game.game_manager import GameManager

pygame.init()
screen = pygame.display.set_mode((1152, 588))
pygame.display.set_caption("Fleabag vs Mutt")

menu_bg = pygame.image.load("assets/images/backgrounds/main_interface.jpg").convert()
choose_game_bg = pygame.image.load("assets/images/backgrounds/choose_game_interface.jpg").convert()

#Main interface buttons location
play_button = pygame.Rect(223, 387, 300, 70)
background_button = pygame.Rect(639, 387, 300, 70)
howto_button = pygame.Rect(215, 493, 300, 70)
setting_button = pygame.Rect(645, 493, 300, 70)

#Choose player mode buttons location
mode_button_1 = pygame.Rect(365, 240, 175, 180)
mode_button_2 = pygame.Rect(565, 240, 200, 180)
back_button = pygame.Rect(37, 30, 131, 46)

#Customization buttons location


clock = pygame.time.Clock()
game = GameManager(screen)

current_screen = "menu"  # Track current screen

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if current_screen == "menu":
                if play_button.collidepoint(mx, my):
                    print("Play Game clicked")
                    current_screen = "choose_game"
                elif background_button.collidepoint(mx, my):
                    print("Background clicked")
                elif howto_button.collidepoint(mx, my):
                    print("How to Play clicked")
                elif setting_button.collidepoint(mx, my):
                    print("Setting clicked")

            elif current_screen == "choose_game":
                if mode_button_1.collidepoint(mx, my):
                    print("1 Player Mode Selected")
                    # Start 1 player mode logic here
                elif mode_button_2.collidepoint(mx, my):
                    print("2 Player Mode Selected")
                    # Start 2 player mode logic here
                elif back_button.collidepoint(mx, my):
                    print("Back button clicked")
                    current_screen = "menu"

    # Draw based on current screen
    if current_screen == "menu":
        screen.blit(menu_bg, (0, 0))

    elif current_screen == "choose_game":
        screen.blit(choose_game_bg, (0, 0))
        

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
