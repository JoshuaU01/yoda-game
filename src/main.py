import sys
import os
import pygame
def check_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()

if __name__ == '__main__':

    pygame.init()
    clock = pygame.time.Clock()
    os.chdir("..")

    pygame.display.set_caption("Game")
    screen_size_x = 1800
    screen_size_y = 950
    screen = pygame.display.set_mode([screen_size_x, screen_size_y])

    background = pygame.image.load("media/images/background/map_gras.png")
    background = pygame.transform.scale(background, (1800, 950))

    while True:
        check_exit()
        screen.blit(background, (0, 0))



        pygame.display.update()
        clock.tick(60)