import sys
import os
import pygame

os.chdir("..")  # Work from root directory of the project to include all media and source files

from player import Player
from enemy import Enemy
from sniper_guy import SniperGuy
from world import World
from floor import Floor
from block import Block

from colors import *
from screen_dimensions import *

def main():
    # Init pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Init screen
    RUNNING = True
    FULLSCREEN = False
    pygame.display.set_caption("Joda Game")
    display_info = pygame.display.Info()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    player_1 = Player((400, 530), (55, 151), 10, World.image_player, 10)
    World.players.add(player_1)
    World.all_sprites.add(player_1)

    enemy_1 = SniperGuy((1130, 510), (84, 156), 0, World.image_enemy, 3)
    World.enemies.add(enemy_1)
    World.all_sprites.add(enemy_1)

    floor = Floor(SCREEN_WIDTH, 145, 0, SCREEN_HEIGHT - 145, World.image_floor)
    World.floors.add(floor)
    World.all_sprites.add(floor)

    block_positions = [
        (100, 570),
        (200, 420),
        (300, 270),
        (330, 270),
        (360, 270),
        (600, 310),
        (800, 200)
    ]

    for pos in block_positions:
        block = Block(30, 30, pos[0], pos[1])
        World.blocks.add(block)
        World.all_sprites.add(block)

    # Start the game loop
    while RUNNING:
        # Get input
        for event in pygame.event.get():
            # Check for key inputs which close the game
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                if FULLSCREEN:
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                else:
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                FULLSCREEN = not FULLSCREEN

        World.all_sprites.update()  # Update sprites

        # Update display
        screen.fill(WHITE)
        screen.blit(World.image_background, (0, 0))
        screen.blit(World.image_floor, (0, SCREEN_HEIGHT - 180))
        World.all_sprites.draw(screen)

        pygame.display.update()
        clock.tick(60)  # Set the framerate to 60fps


if __name__ == '__main__':
    main()
    pygame.quit()