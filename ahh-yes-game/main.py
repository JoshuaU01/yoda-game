import pygame

if __name__ == '__main__':

    pygame.init()
    clock = pygame.time.Clock()

    pygame.display.set_caption("Ahh yes game")
    screen_size_x = 1200
    screen_size_y = 595
    screen = pygame.display.set_mode([screen_size_x, screen_size_y])

    while True:
        pygame.display.update()
        clock.tick(60)