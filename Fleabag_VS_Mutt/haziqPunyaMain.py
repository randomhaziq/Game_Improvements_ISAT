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

# Music and Sound
music_1 = "assets/sounds/music_1.mp3"
drag_effect = pygame.mixer.Sound("assets/sounds/Drag_Button.mp3")
click_effect = pygame.mixer.Sound("assets/sounds/Click_Button.mp3")

# Slider properties for music volume control
slider_track_music = pygame.Rect(495, 277, 259, 4)
slider_handle_music_radius = 9
music_volume = 0.5
slider_handle_x_music = slider_track_music.x + int(music_volume * slider_track_music.width)
dragging_music = False

# Set initial music volume
pygame.mixer.music.set_volume(music_volume)

# Slider properties for sound effects volume control
slider_track_sound = pygame.Rect(495, 374, 259, 4)
slider_handle_sound_radius = 9
sound_volume = 0.5
slider_handle_x_sound = slider_track_sound.x + int(sound_volume * slider_track_sound.width)
dragging_sound = False

# Set initial sound effect volume
drag_effect.set_volume(sound_volume)
click_effect.set_volume(sound_volume)

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
game_screen = None

# Add a rectangle for the name edit icon
edit_name_icon = pygame.Rect(723, 171, 27, 24)  # Example coordinates and size for the icon

# Variable to store the user's name
user_name = "Player"  # Default name
editing_name = False  # Flag to check if the user is editing their name
input_box = pygame.Rect(430, 202, 285, 40)  # Input box for name editing
input_text = ""  # Text entered by the user

def play_music(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)

play_music(music_1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_screen == "menu":
            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                # Check if the mouse is on top any button
                if play_button.collidepoint(mx, my):
                    if hovered_button != "play_button":  # Only play if not already hovered
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
                    hovered_button = None  # Reset when the mouse leaves all buttons

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if play_button.collidepoint(mx, my):
                    click_effect.play()
                    current_screen = "choose_game"
                elif background_button.collidepoint(mx, my):
                    click_effect.play()
                    current_screen = "background"
                elif howto_button.collidepoint(mx, my):
                    click_effect.play()
                    current_screen = "how_to"
                elif setting_button.collidepoint(mx, my):
                    click_effect.play()
                    current_screen = "setting"

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
                    current_screen = "choose_customize_1p"
                elif mode_button_2.collidepoint(mx, my):
                    click_effect.play()
                    current_screen = "choose_customize_2p"
                elif back_button.collidepoint(mx, my):
                    click_effect.play()
                    current_screen = "menu"

        elif current_screen == "choose_customize_1p":
            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                if back_button.collidepoint(mx, my):
                    if hovered_button != "back_button":  
                        drag_effect.play()
                        hovered_button = "back_button"
                elif customize_button_1p.collidepoint(mx, my):
                    if hovered_button != "customize_button_1p":
                        drag_effect.play()
                        hovered_button = "customize_button_1p"
                elif play_customize_button_1p.collidepoint(mx, my):
                    if hovered_button != "play_customize_button_1p":
                        drag_effect.play()
                        hovered_button = "play_customize_button_1p"
                else: 
                    hovered_button = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if play_customize_button_1p.collidepoint(mx, my):
                    click_effect.play()
                    game_screen = GameScreen(screen, game_mode="1P")
                    current_screen = "game"
                elif customize_button_1p.collidepoint(mx, my):
                    click_effect.play()
                    pass
                elif back_customize_button_1p.collidepoint(mx, my):
                    click_effect.play()
                    current_screen = "choose_game"

        elif current_screen == "choose_customize_2p":
            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                if back_button.collidepoint(mx, my):
                    if hovered_button != "back_button":  
                        drag_effect.play()
                        hovered_button = "back_button"
                elif cat_customize_button_2p.collidepoint(mx, my):
                    if hovered_button != "cat_customize_button_2p":
                        drag_effect.play()
                        hovered_button = "cat_customize_button_2p"
                elif dog_customize_button_2p.collidepoint(mx, my):
                    if hovered_button != "dog_customize_button_2p":
                        drag_effect.play()
                        hovered_button = "dog_customize_button_2p"
                elif play_customize_button_2p.collidepoint(mx, my):
                    if hovered_button != "play_customize_button_2p":
                        drag_effect.play()
                        hovered_button = "play_customize_button_2p"
                else: 
                    hovered_button = None 

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if play_customize_button_2p.collidepoint(mx, my):
                    click_effect.play()
                    game_screen = GameScreen(screen, game_mode="2P")
                    current_screen = "game"
                elif cat_customize_button_2p.collidepoint(mx, my):
                    click_effect.play()
                    pass
                elif dog_customize_button_2p.collidepoint(mx, my):
                    click_effect.play()
                    pass
                elif back_customize_button_2p.collidepoint(mx, my):
                    click_effect.play()
                    current_screen = "choose_game"

        elif current_screen == "game":
            # Forward events to game screen
            if game_screen:
                result = game_screen.handle_event(event)
                if result == "pause_menu":
                    current_screen = "menu"
                    game_screen = None

        elif current_screen == "background":
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
                    current_screen = "menu"

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
                    current_screen = "menu"

        elif current_screen == "setting":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if back_button.collidepoint(mx, my):
                    click_effect.play()
                    current_screen = "menu"
                elif edit_name_icon.collidepoint(mx, my):  
                    click_effect.play()
                    editing_name = True  
                elif (event.pos[0] - slider_handle_x_music) ** 2 + (event.pos[1] - slider_track_music.centery) ** 2 <= slider_handle_music_radius ** 2:
                    dragging_music = True
                elif (event.pos[0] - slider_handle_x_sound) ** 2 + (event.pos[1] - slider_track_sound.centery) ** 2 <= slider_handle_sound_radius ** 2:
                    dragging_sound = True

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

            elif event.type == pygame.KEYDOWN and editing_name:  # Handle keyboard input for name editing
                if event.key == pygame.K_RETURN:  # Save the name when Enter is pressed
                    click_effect.play()
                    user_name = input_text if input_text.strip() else user_name  # Keep the old name if input is empty
                    input_text = ""
                    editing_name = False  # Disable name editing
                elif event.key == pygame.K_BACKSPACE:  # Handle backspace
                    input_text = input_text[:-1]
                else:  # Add typed characters to the input text
                    input_text += event.unicode

    # Draw screen
    if current_screen == "menu":
        screen.blit(menu_bg, (0, 0))
    elif current_screen == "how_to":
        screen.blit(how_to_bg, (0, 0))
    elif current_screen == "background":
        screen.blit(background_bg, (0, 0))
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
        name_rect = name_surface.get_rect(center=(input_box.centerx, input_box.top - 20))  # Center above the input box
        screen.blit(name_surface, name_rect)
        # Draw the input box if editing
        if editing_name:
            pygame.draw.rect(screen, (255, 255, 255), input_box) # Input Box
            pygame.draw.rect(screen, (0, 0, 0), input_box, 2)  # Border 
            input_surface = font.render(input_text, True, (0, 0, 0))
            input_rect = input_surface.get_rect(center=input_box.center)  # Center inside the input box
            screen.blit(input_surface, input_rect)
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
