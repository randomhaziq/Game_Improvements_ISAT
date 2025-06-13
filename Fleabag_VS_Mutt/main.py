import pygame
from game.game_manager import GameManager
from game.gamescreen import GameScreen

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1152, 588))
pygame.display.set_caption("Fleabag vs Mutt")

# Load images for menus and backgrounds
menu_bg = pygame.image.load("assets/images/backgrounds/main_interface.jpg").convert()
how_to_bg = pygame.image.load("assets/images/backgrounds/how_to.jpg").convert()
setting_bg = pygame.image.load("assets/images/backgrounds/setting.jpg").convert()
background_bg = pygame.image.load("assets/images/backgrounds/choose_background.jpg").convert()
choose_game_bg = pygame.image.load("assets/images/backgrounds/choose_game_interface.jpg").convert()
choose_customize_1p_bg = pygame.image.load("assets/images/backgrounds/customization_interface_1p.jpg").convert()
choose_customize_2p_bg = pygame.image.load("assets/images/backgrounds/customization_interface_2p.jpg").convert()

# Music
music_1 = "assets/sounds/music_1.mp3"

# Slider properties for volume control
slider_track = pygame.Rect(495, 277, 259, 4)
slider_handle_radius = 9
volume = 0.5
slider_handle_x = slider_track.x + int(volume * slider_track.width)
pygame.mixer.music.set_volume(volume)
dragging = False

# Buttons (from both files)
play_button = pygame.Rect(223, 387, 300, 70)
background_button = pygame.Rect(639, 387, 300, 70)
howto_button = pygame.Rect(215, 493, 300, 70)
setting_button = pygame.Rect(645, 493, 300, 70)

mode_button_1 = pygame.Rect(365, 240, 175, 180)
mode_button_2 = pygame.Rect(565, 240, 200, 180)
back_button = pygame.Rect(37, 30, 131, 46)

play_customize_button_1p = pygame.Rect(400, 495, 363, 80)
customize_button_1p = pygame.Rect(465, 175, 233, 175)
back_customize_button_1p = pygame.Rect(46, 10, 123, 40)

play_customize_button_2p = pygame.Rect(400, 495, 363, 80)
dog_customize_button_2p = pygame.Rect(365, 175, 206, 190)
cat_customize_button_2p = pygame.Rect(590, 175, 206, 190)
back_customize_button_2p = pygame.Rect(46, 10, 123, 40)

clock = pygame.time.Clock()
current_screen = "menu"
game_screen = GameScreen(screen, game_mode="1P", current_screen=current_screen)

def play_music(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)

def set_current_screen(new_screen):
    global current_screen
    current_screen = new_screen

play_music(music_1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_screen == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if play_button.collidepoint(mx, my):
                    current_screen = "choose_game"
                elif background_button.collidepoint(mx, my):
                    current_screen = "background"
                elif howto_button.collidepoint(mx, my):
                    current_screen = "how_to"
                elif setting_button.collidepoint(mx, my):
                    current_screen = "setting"

        elif current_screen == "choose_game":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if mode_button_1.collidepoint(mx, my):
                    current_screen = "choose_customize_1p"
                elif mode_button_2.collidepoint(mx, my):
                    current_screen = "choose_customize_2p"
                elif back_button.collidepoint(mx, my):
                    current_screen = "menu"

        elif current_screen == "choose_customize_1p":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if play_customize_button_1p.collidepoint(mx, my):
                    game_screen = GameScreen(screen, game_mode="1P")
                    current_screen = "game"
                elif customize_button_1p.collidepoint(mx, my):
                    pass
                elif back_customize_button_1p.collidepoint(mx, my):
                    current_screen = "choose_game"

        elif current_screen == "choose_customize_2p":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if play_customize_button_2p.collidepoint(mx, my):
                    game_screen = GameScreen(screen, game_mode="2P")
                    current_screen = "game"
                elif cat_customize_button_2p.collidepoint(mx, my):
                    pass
                elif dog_customize_button_2p.collidepoint(mx, my):
                    pass
                elif back_customize_button_2p.collidepoint(mx, my):
                    current_screen = "choose_game"

        elif current_screen == "game":
            if game_screen:
                result = game_screen.handle_event(event)
                if result == "pause_menu":
                    current_screen = "menu"
                    game_screen = None
                elif result == "menu":
                    current_screen = "menu"
                    game_screen = None


        elif current_screen == "background":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if back_button.collidepoint(mx, my):
                    current_screen = "menu"

        elif current_screen == "how_to":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if back_button.collidepoint(mx, my):
                    current_screen = "menu"

        elif current_screen == "setting":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if (event.pos[0] - slider_handle_x) ** 2 + (event.pos[1] - slider_track.centery) ** 2 <= slider_handle_radius ** 2:
                    dragging = True
                if back_button.collidepoint(mx, my):
                    current_screen = "menu"
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                slider_handle_x = max(slider_track.x, min(event.pos[0], slider_track.x + slider_track.width))
                volume = (slider_handle_x - slider_track.x) / slider_track.width
                pygame.mixer.music.set_volume(volume)

    # Draw screen
    if current_screen == "menu":
        screen.blit(menu_bg, (0, 0))
    elif current_screen == "how_to":
        screen.blit(how_to_bg, (0, 0))
    elif current_screen == "background":
        screen.blit(background_bg, (0, 0))
    elif current_screen == "setting":
        screen.blit(setting_bg, (0, 0))
        # Draw slider
        pygame.draw.rect(screen, (200, 200, 200), slider_track)
        pygame.draw.circle(screen, (0, 0, 0), (slider_handle_x, slider_track.centery), slider_handle_radius)
        black_part = pygame.Rect(slider_track.x, slider_track.y, slider_handle_x - slider_track.x, slider_track.height)
        pygame.draw.rect(screen, (0, 0, 0), black_part) 
    elif current_screen == "choose_game":
        screen.blit(choose_game_bg, (0, 0))
    elif current_screen == "choose_customize_1p":
        screen.blit(choose_customize_1p_bg, (0, 0))
    elif current_screen == "choose_customize_2p":
        screen.blit(choose_customize_2p_bg, (0, 0))
    elif current_screen == "game" and game_screen:
        game_screen.update()
        game_screen.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
