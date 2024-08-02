import pygame
from game_attr import Game
from settings import *


def main():
    pygame.init()
    screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.set_caption(screen_title)
    clock = pygame.time.Clock()
    done = False
    game = Game()

    while True:
        done = game.processEvents()
        if game.victory:
            game.end_screen(screen, "victory")
            pygame.time.wait(7000)
            break
        elif game.player.lifes == 0:
            game.end_screen(screen, "game_over")
            pygame.time.wait(7000)
            break
        if done:
            break
        else:
            game.runLogic()
            game.draw(screen)
            clock.tick(60)

    pygame.quit()


main()
