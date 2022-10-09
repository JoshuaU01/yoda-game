import sys
import os
import pygame

import player
import world
def check_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()

if __name__ == '__main__':

    pygame.init()
    clock = pygame.time.Clock()
    os.chdir("..")  # Work from root directory of the project to include all media and source files

    pygame.display.set_caption("Game")
    screen_size_x = 1800
    screen_size_y = 950
    screen = pygame.display.set_mode([screen_size_x, screen_size_y])

    image_player = pygame.image.load("media/images/player/ziwomol/ziwomol_v3.png")
    image_player = pygame.transform.scale(image_player, (95, 260))
    image_player_reverse = pygame.image.load("media/images/player/ziwomol/ziwomol_v3_reverse.png")
    image_player_reverse = pygame.transform.scale(image_player_reverse, (95, 260))

    player = player.Player()
    world = world.World("media/images/background/map_gras.png", (1800, 950), False, False, 30)

    while True:
        check_exit()  # Check for key inputs which close the game

        player.move()
        player.jump(world.gravity)

        # Update display
        screen.blit(world.background, (0, 0))
        player.draw(screen, image_player, image_player_reverse)
        pygame.display.update()
        clock.tick(60)