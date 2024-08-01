import sys
import os
import pygame

os.chdir("..")  # Work from root directory of the project to include all media and source files

from player import Player
from enemy import Enemy
from sniper_guy import SniperGuy
from world import World
from border import Border
from block import Block
from camera import Camera, FollowCamMode, BorderCamMode, AutoCamMode

from colors import *
from screen_dimensions import *

def main():
    # Init pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Init screen
    pygame.display.set_caption("Joda Game")
    display_info = pygame.display.Info()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    player_1 = Player((400, 530), (55, 151), 10, World.image_player, 2)
    World.players.add(player_1)
    World.all_sprites.add(player_1)

    enemy_1 = Enemy((900, 510), (84, 156), 0, World.image_enemy, 3)
    World.enemies.add(enemy_1)
    World.all_sprites.add(enemy_1)

    enemy_2 = SniperGuy((2200, 200), (60, 110), -2, World.image_enemy, 5)
    World.enemies.add(enemy_2)
    World.all_sprites.add(enemy_2)

    floor = Border(5 * SCREEN_WIDTH, 145, 0, SCREEN_HEIGHT - 145)
    World.borders.add(floor)
    World.all_sprites.add(floor)

    wall_left = Border(100, SCREEN_HEIGHT + 200, -100, -100)
    World.borders.add(wall_left)
    World.all_sprites.add(wall_left)

    wall_right = Border(100, SCREEN_HEIGHT + 200, 2600, -100)
    World.borders.add(wall_right)
    World.all_sprites.add(wall_right)

    block_positions = [
        (100, 570),
        (200, 420),
        (300, 270),
        (330, 270),
        (360, 270),
        (600, 310),
        (800, 200),
        (1280, 500),
        (1500, 420),
        (1600, 280),
        (2170, 310),
        (2200, 310),
        (2230, 310),
        (2260, 310),
    ]

    for pos in block_positions:
        block = Block(30, 30, pos[0], pos[1])
        World.blocks.add(block)
        World.all_sprites.add(block)

    # Initialize camera
    camera = Camera(player_1, SCREEN_WIDTH, SCREEN_HEIGHT)
    follow_cam_mode = FollowCamMode(camera)
    border_cam_mode = BorderCamMode(camera, wall_left.rect.right, wall_right.rect.left)
    auto_cam_mode = AutoCamMode(camera, 1)
    camera.set_method(border_cam_mode)
    character_focus_index = 0

    # Start the game loop
    while World.RUNNING:
        # Get input
        for event in pygame.event.get():
            # Check for key inputs which close the game
            if event.type == pygame.QUIT:
                World.RUNNING = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    World.RUNNING = False
                # Check for key inputs which toggle between windows and full screen
                elif event.key == pygame.K_f:
                    if World.FULLSCREEN:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    else:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                    World.FULLSCREEN = not World.FULLSCREEN
                # Check for key inputs which set the camera
                elif event.key == pygame.K_1:
                    camera.set_method(follow_cam_mode)
                elif event.key == pygame.K_2:
                    camera.set_method(border_cam_mode)
                elif event.key == pygame.K_3:
                    camera.set_method(auto_cam_mode)
                elif event.key == pygame.K_4:
                    characters_list = World.players.sprites() + World.enemies.sprites()
                    if character_focus_index >= len(characters_list) - 1:
                        character_focus_index = 0
                    else:
                        character_focus_index += 1
                    camera.set_target(characters_list[character_focus_index])

        World.all_sprites.update()
        camera.scroll()

        # Update display
        screen.fill(WHITE)
        screen.blit(World.image_background, (0, 0))
        screen.blit(World.image_floor, (0, SCREEN_HEIGHT - 180))
        for sprite in World.all_sprites:
            screen.blit(sprite.image, camera.apply_offset(sprite))

        pygame.display.update()
        clock.tick(60)  # Set the framerate to 60fps


if __name__ == '__main__':
    main()
    pygame.quit()