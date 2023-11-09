import pygame
from new_manager import Manager


game = Manager()
game.init_game()

run = True
while run:
    game.game_loop()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    game.clock.tick(60)
pygame.quit()
