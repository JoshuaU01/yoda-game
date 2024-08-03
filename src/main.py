import sys
import os
import pygame

os.chdir("..")  # Work from root directory of the project to include all media and source files

from player import Player
from runner import Runner
from sniper_guy import SniperGuy
from world import World
from sprite_sheet import SpriteSheet
from tile_grid_map import TileGridMap
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

    # Create player
    player_1 = Player((200, 530), (40, 110), 10, World.image_player, 2)
    World.players.add(player_1)
    World.all_sprites.add(player_1)

    # Create enemies
    enemy_1 = Runner((600, 500), (70, 130), 0, World.image_enemy, 5)
    World.enemies.add(enemy_1)
    World.all_sprites.add(enemy_1)
    enemy_2 = SniperGuy((2195, 100), (60, 110), -2, World.image_enemy, 3)
    World.enemies.add(enemy_2)
    World.all_sprites.add(enemy_2)

    # Create borders
    #floor = Border(0, SCREEN_HEIGHT, 10 * SCREEN_HEIGHT, 100)
    #World.borders.add(floor)
    #World.all_sprites.add(floor)
    left_wall = Border(-100, -100, 100, SCREEN_HEIGHT + 200)
    World.borders.add(left_wall)
    World.all_sprites.add(left_wall)
    right_wall = Border(2560, -100, 100, SCREEN_HEIGHT + 200)
    World.borders.add(right_wall)
    World.all_sprites.add(right_wall)

    # Init camera
    camera = Camera(player_1, SCREEN_WIDTH, SCREEN_HEIGHT)
    follow_cam_mode = FollowCamMode(camera)
    border_cam_mode = BorderCamMode(camera, left_wall.rect.right, right_wall.rect.left)
    auto_cam_mode = AutoCamMode(camera, 1)
    camera.set_method(border_cam_mode)
    character_focus_index = 0

    # Load sprite sheets and maps
    grass_sheet = SpriteSheet("media/images/blocks/grass_sheet_64")
    layer_0 = TileGridMap("media/maps/grass_level_layer_0.csv", grass_sheet, 32)
    layer_0.load_csv()
    layer_0.render()

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
                    character_focus_index = (character_focus_index + 1) % len(characters_list)
                    camera.set_target(characters_list[character_focus_index])

        World.all_sprites.update()
        camera.scroll()

        # Update display
        screen.fill(WHITE)
        screen.blit(World.image_background, (0, 0))
        for sprite in World.all_sprites:
            screen.blit(sprite.image, camera.apply_offset(sprite))

        pygame.display.update()
        clock.tick(60)  # Set the framerate to 60fps
        print(player_1.rect)


if __name__ == '__main__':
    main()
    pygame.quit()