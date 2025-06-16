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
help_and_support_bg = pygame.image.load("assets/images/backgrounds/help_and_support.jpg").convert()

# Background image paths
background_backyard_path = "assets/images/backgrounds/background_backyard.jpg"
background_space_path = "assets/images/backgrounds/background_moon.jpg"
background_beach_path = "assets/images/backgrounds/background_beach.jpg"
background_paris_path = "assets/images/backgrounds/background_paris.jpg"

# Music and Sound
music_1 = "assets/sounds/music_1.mp3"
drag_effect = pygame.mixer.Sound("assets/sounds/Drag_Button.mp3")
click_effect = pygame.mixer.Sound("assets/sounds/Click_Button.mp3")

# Music volume slider
slider_track_music = pygame.Rect(495, 277, 259, 4)
slider_handle_music_radius = 9
music_volume = 0.5
slider_handle_x_music = slider_track_music.x + int(music_volume * slider_track_music.width)
dragging_music = False
pygame.mixer.music.set_volume(music_volume)

# Sound effect volume slider
slider_track_sound = pygame.Rect(495, 374, 259, 4)
slider_handle_sound_radius = 9
sound_volume = 0.5
slider_handle_x_sound = slider_track_sound.x + int(sound_volume * slider_track_sound.width)
dragging_sound = False
drag_effect.set_volume(sound_volume)
click_effect.set_volume(sound_volume)

# Buttons
play_button = pygame.Rect(223, 387, 300, 70)
background_button = pygame.Rect(639, 387, 300, 70)
howto_button = pygame.Rect(215, 493, 300, 70)
setting_button = pygame.Rect(645, 493, 300, 70)

mode_button_1 = pygame.Rect(365, 240, 175, 180)
mode_button_2 = pygame.Rect(565, 240, 200, 180)
back_button = pygame.Rect(37, 30, 131, 46)
help_and_support_button = pygame.Rect(442, 458, 271, 22)

# Background selection rectangles
background1_rect = pygame.Rect(200, 180, 296, 145)
background2_rect = pygame.Rect(646, 180, 296, 145)
background3_rect = pygame.Rect(202, 379, 296, 145)
background4_rect = pygame.Rect(643, 379, 296, 145)



clock = pygame.time.Clock()
current_screen = "menu"
game_screen = None

# User name editing
edit_name_icon = pygame.Rect(375, 148, 405, 66)
user_name = "Player1"
editing_name = False
input_box = pygame.Rect(430, 202, 285, 40)
input_text = ""

# Hovered button for drag sound
hovered_button = None

# Selected background
selected_background_path = background_backyard_path
selected_background = pygame.image.load(selected_background_path).convert()

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
            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                if play_button.collidepoint(mx, my):
                    if hovered_button != "play_button":
                        drag_effect.play()
                        hovered_button = "play_button"
                elif background_button.collidepoint(mx, my):
                    if hovered_button != "background_button":
                        drag_effect.play()
                        hovered_button = "background_button"
                elif howto_button.collidepoint(mx, my):
                    if hovered_button != "howto_button":
                        drag_effect.play()
                        hovered_button = "howto_button"
                elif setting_button.collidepoint(mx, my):
                    if hovered_button != "setting_button":
                        drag_effect.play()
                        hovered_button = "setting_button"
                else:
                    hovered_button = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if play_button.collidepoint(mx, my):
                    click_effect.play()
                    set_current_screen("choose_game")
                elif background_button.collidepoint(mx, my):
                    click_effect.play()
                    set_current_screen("background")
                elif howto_button.collidepoint(mx, my):
                    click_effect.play()
                    set_current_screen("how_to")
                elif setting_button.collidepoint(mx, my):
                    click_effect.play()
                    set_current_screen("setting")

        elif current_screen == "choose_game":
            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                if back_button.collidepoint(mx, my):
                    if hovered_button != "back_button":
                        drag_effect.play()
                        hovered_button = "back_button"
                elif mode_button_1.collidepoint(mx, my):
                    if hovered_button != "mode_button_1":
                        drag_effect.play()
                        hovered_button = "mode_button_1"
                elif mode_button_2.collidepoint(mx, my):
                    if hovered_button != "mode_button_2":
                        drag_effect.play()
                        hovered_button = "mode_button_2"
                else:
                    hovered_button = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if mode_button_1.collidepoint(mx, my):
                    click_effect.play()
                    gravity = 0.2 if selected_background_path == background_space_path else 0.5  # 0.2 for moon, 0.5 normal
                    game_screen = GameScreen(screen, game_mode="1P", background_path=selected_background_path, gravity=gravity)
                    set_current_screen("game")
                elif mode_button_2.collidepoint(mx, my):
                    click_effect.play()
                    gravity = 0.2 if selected_background_path == background_space_path else 0.5
                    game_screen = GameScreen(screen, game_mode="2P", background_path=selected_background_path, gravity=gravity)
                    set_current_screen("game")
                elif back_button.collidepoint(mx, my):
                    click_effect.play()
                    set_current_screen("menu")

        elif current_screen == "game":
            if game_screen:
                result = game_screen.handle_event(event)
                if result == "menu":
                    set_current_screen("menu")
                    game_screen = None

        elif current_screen == "background":
            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                if back_button.collidepoint(mx, my):
                    if hovered_button != "back_button":
                        drag_effect.play()
                        hovered_button = "back_button"
                elif background1_rect.collidepoint(mx, my):
                    if hovered_button != "background1_rect":
                        drag_effect.play()
                        hovered_button = "background1_rect"
                elif background2_rect.collidepoint(mx, my):
                    if hovered_button != "background2_rect":
                        drag_effect.play()
                        hovered_button = "background2_rect"
                elif background3_rect.collidepoint(mx, my):
                    if hovered_button != "background3_rect":
                        drag_effect.play()
                        hovered_button = "background3_rect"
                elif background4_rect.collidepoint(mx, my):
                    if hovered_button != "background4_rect":
                        drag_effect.play()
                        hovered_button = "background4_rect"
                else:
                    hovered_button = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if back_button.collidepoint(mx, my):
                    click_effect.play()
                    set_current_screen("menu")
                elif background1_rect.collidepoint(mx, my):
                    click_effect.play()
                    selected_background_path = background_backyard_path
                    selected_background = pygame.image.load(selected_background_path).convert()
                elif background2_rect.collidepoint(mx, my):
                    click_effect.play()
                    selected_background_path = background_space_path
                    selected_background = pygame.image.load(selected_background_path).convert()
                elif background3_rect.collidepoint(mx, my):
                    click_effect.play()
                    selected_background_path = background_beach_path
                    selected_background = pygame.image.load(selected_background_path).convert()
                elif background4_rect.collidepoint(mx, my):
                    click_effect.play()
                    selected_background_path = background_paris_path
                    selected_background = pygame.image.load(selected_background_path).convert()

        elif current_screen == "how_to":
            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                if back_button.collidepoint(mx, my):
                    if hovered_button != "back_button":
                        drag_effect.play()
                        hovered_button = "back_button"
                else:
                    hovered_button = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if back_button.collidepoint(mx, my):
                    click_effect.play()
                    set_current_screen("menu")

        elif current_screen == "setting":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if back_button.collidepoint(mx, my):
                    click_effect.play()
                    set_current_screen("menu")
                elif edit_name_icon.collidepoint(mx, my):
                    click_effect.play()
                    editing_name = True
                elif (event.pos[0] - slider_handle_x_music) ** 2 + (event.pos[1] - slider_track_music.centery) ** 2 <= slider_handle_music_radius ** 2:
                    dragging_music = True
                elif (event.pos[0] - slider_handle_x_sound) ** 2 + (event.pos[1] - slider_track_sound.centery) ** 2 <= slider_handle_sound_radius ** 2:
                    dragging_sound = True
                elif help_and_support_button.collidepoint(mx, my):
                    click_effect.play()
                    set_current_screen("help_and_support")

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_music = False
                dragging_sound = False

            elif event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                if back_button.collidepoint(mx, my):
                    if hovered_button != "back_button":
                        drag_effect.play()
                        hovered_button = "back_button"
                elif edit_name_icon.collidepoint(mx, my):
                    if hovered_button != "edit_name_icon":
                        drag_effect.play()
                        hovered_button = "edit_name_icon"
                elif help_and_support_button.collidepoint(mx, my):
                    if hovered_button != "help_and_support_button":
                        drag_effect.play()
                        hovered_button = "help_and_support_button"
                else:
                    hovered_button = None
                if dragging_music:
                    slider_handle_x_music = max(slider_track_music.x, min(event.pos[0], slider_track_music.x + slider_track_music.width))
                    music_volume = (slider_handle_x_music - slider_track_music.x) / slider_track_music.width
                    pygame.mixer.music.set_volume(music_volume)
                elif dragging_sound:
                    slider_handle_x_sound = max(slider_track_sound.x, min(event.pos[0], slider_track_sound.x + slider_track_sound.width))
                    sound_volume = (slider_handle_x_sound - slider_track_sound.x) / slider_track_sound.width
                    drag_effect.set_volume(sound_volume)
                    click_effect.set_volume(sound_volume)

            elif event.type == pygame.KEYDOWN and editing_name:
                if event.key == pygame.K_RETURN:
                    click_effect.play()
                    user_name = input_text if input_text.strip() else user_name
                    input_text = ""
                    editing_name = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        elif current_screen == "help_and_support":
            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                if back_button.collidepoint(mx, my):
                    if hovered_button != "back_button":
                        drag_effect.play()
                        hovered_button = "back_button"
                else:
                    hovered_button = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if back_button.collidepoint(mx, my):
                    click_effect.play()
                    set_current_screen("setting")

    # Draw screen
    if current_screen == "menu":
        screen.blit(menu_bg, (0, 0))
    elif current_screen == "how_to":
        screen.blit(how_to_bg, (0, 0))
    elif current_screen == "background":
        screen.blit(background_bg, (0, 0))
        # White outlines for all backgrounds
        pygame.draw.rect(screen, (255, 255, 255), background1_rect, 3)
        pygame.draw.rect(screen, (255, 255, 255), background2_rect, 3)
        pygame.draw.rect(screen, (255, 255, 255), background3_rect, 3)
        pygame.draw.rect(screen, (255, 255, 255), background4_rect, 3)
        # Red outline for selected background
        if selected_background_path == background_backyard_path:
            pygame.draw.rect(screen, (255, 0, 0), background1_rect, 5)
        elif selected_background_path == background_space_path:
            pygame.draw.rect(screen, (255, 0, 0), background2_rect, 5)
        elif selected_background_path == background_beach_path:
            pygame.draw.rect(screen, (255, 0, 0), background3_rect, 5)
        elif selected_background_path == background_paris_path:
            pygame.draw.rect(screen, (255, 0, 0), background4_rect, 5)
    elif current_screen == "setting":
        screen.blit(setting_bg, (0, 0))
        # Draw music slider
        pygame.draw.rect(screen, (200, 200, 200), slider_track_music)
        pygame.draw.circle(screen, (0, 0, 0), (slider_handle_x_music, slider_track_music.centery), slider_handle_music_radius)
        black_part_music = pygame.Rect(slider_track_music.x, slider_track_music.y, slider_handle_x_music - slider_track_music.x, slider_track_music.height)
        pygame.draw.rect(screen, (0, 0, 0), black_part_music)
        # Draw sound effect slider
        pygame.draw.rect(screen, (200, 200, 200), slider_track_sound)
        pygame.draw.circle(screen, (0, 0, 0), (slider_handle_x_sound, slider_track_sound.centery), slider_handle_sound_radius)
        black_part_sound = pygame.Rect(slider_track_sound.x, slider_track_sound.y, slider_handle_x_sound - slider_track_sound.x, slider_track_sound.height)
        pygame.draw.rect(screen, (0, 0, 0), black_part_sound)
        # Display the user's name
        font = pygame.font.Font(None, 37)
        name_surface = font.render(f"{user_name}", True, (0, 0, 0))
        name_rect = name_surface.get_rect(center=(input_box.centerx, input_box.top - 20))
        screen.blit(name_surface, name_rect)
        # Draw the input box if editing
        if editing_name:
            pygame.draw.rect(screen, (255, 255, 255), input_box)
            pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
            input_surface = font.render(input_text, True, (0, 0, 0))
            input_rect = input_surface.get_rect(center=input_box.center)
            screen.blit(input_surface, input_rect)
    elif current_screen == "help_and_support":
        screen.blit(help_and_support_bg, (0, 0))
    elif current_screen == "choose_game":
        screen.blit(choose_game_bg, (0, 0))
    elif current_screen == "game" and game_screen:
        game_screen.update()
        game_screen.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
