import pygame
from new_manager import Manager


game = Manager()
game.init_game()

running = True
while running:
    game.game_loop()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    game.clock.tick(45)
pygame.quit()
