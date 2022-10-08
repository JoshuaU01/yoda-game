import sys
import pygame
def check_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()

if __name__ == '__main__':

    pygame.init()
    clock = pygame.time.Clock()

    pygame.display.set_caption("Game")
    screen_size_x = 1200
    screen_size_y = 595
    screen = pygame.display.set_mode([screen_size_x, screen_size_y])

    while True:
        check_exit()
        pygame.display.update()
        clock.tick(60)