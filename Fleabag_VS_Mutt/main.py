import pygame
from game.game_manager import GameManager

pygame.init()
screen = pygame.display.set_mode((1152, 588))
pygame.display.set_caption("Fleabag vs Mutt")
clock = pygame.time.Clock()

game = GameManager(screen)

running = True
while running:
    background = pygame.image.load("assets/images/backgrounds/backyard.jpg").convert()
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        game.handle_event(event)

    game.update()
    game.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
