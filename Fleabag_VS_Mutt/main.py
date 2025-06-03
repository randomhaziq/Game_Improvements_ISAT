import pygame
from game.game_manager import GameManager

pygame.init()
screen = pygame.display.set_mode((1152, 588))
pygame.display.set_caption("Fleabag vs Mutt")

menu_bg = pygame.image.load("assets/images/backgrounds/main_interface.jpg").convert()
choose_game_bg = pygame.image.load("assets/images/backgrounds/choose_game_interface.jpg").convert()
choose_customize_1p_bg = pygame.image.load("assets/images/backgrounds/customization_interface_1p.jpg").convert()
choose_customize_2p_bg = pygame.image.load("assets/images/backgrounds/customization_interface_2p.jpg").convert()

#Main interface buttons location
play_main_button = pygame.Rect(223, 387, 300, 70)
background_button = pygame.Rect(639, 387, 300, 70)
howto_button = pygame.Rect(215, 493, 300, 70)
setting_button = pygame.Rect(645, 493, 300, 70)

#Choose player mode buttons location
mode_button_1 = pygame.Rect(365, 240, 175, 180)
mode_button_2 = pygame.Rect(565, 240, 200, 180)
back_mode_button = pygame.Rect(37, 30, 131, 46)

#Customization buttons location
play_customize_button_1p = pygame.Rect(400, 495, 363, 80)
customize_button_1p = pygame.Rect(465, 175, 233, 175)
back_customize_button_1p = pygame.Rect(46, 10, 123, 40)

play_customize_button_2p = pygame.Rect(400, 495, 363, 80)
dog_customize_button_2p = pygame.Rect(365, 175, 206, 190)
cat_customize_button_2p = pygame.Rect(590, 175, 206, 190)
back_customize_button_2p = pygame.Rect(46, 10, 123, 40)


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
                if play_main_button.collidepoint(mx, my):
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
                    current_screen = "choose_customize_1p"   
                elif mode_button_2.collidepoint(mx, my):
                    print("2 Player Mode Selected")
                    current_screen = "choose_customize_2p"
                elif back_mode_button.collidepoint(mx, my):
                    print("Back button clicked")
                    current_screen = "menu"

            elif current_screen == "choose_customize_1p":
                if play_customize_button_1p.collidepoint(mx, my):
                    print("Start 1P game")
                    # start 1 player game
                elif customize_button_1p.collidepoint(mx, my):
                    print("Customize 1P")
                elif back_customize_button_1p.collidepoint(mx, my):
                    current_screen = "choose_game"

            elif current_screen == "choose_customize_2p":
                if play_customize_button_2p.collidepoint(mx, my):
                    print("Start 2P game")
                    # start 2 player game
                elif cat_customize_button_2p.collidepoint(mx, my):
                    print("CAT Customize 2P")
                elif dog_customize_button_2p.collidepoint(mx, my):
                    print("DOG Customize 2P")
                elif back_customize_button_2p.collidepoint(mx, my):
                    current_screen = "choose_game"


    # Draw based on current screen
    if current_screen == "menu":
        screen.blit(menu_bg, (0, 0))
    elif current_screen == "choose_game":
        screen.blit(choose_game_bg, (0, 0))
    elif current_screen == "choose_customize_1p":
        screen.blit(choose_customize_1p_bg, (0, 0))
    elif current_screen == "choose_customize_2p":
        screen.blit(choose_customize_2p_bg, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
