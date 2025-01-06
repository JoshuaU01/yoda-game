import os
import pygame

os.chdir("..")  # Work from root directory of the project to include all media and source files

from src.assets.characters.player import Player
from src.assets.characters.enemies.runner import Runner
from src.assets.characters.enemies.sniper_guy import SniperGuy
from src.assets.objects.border import Border
from src.environment.sprite_sheet import SpriteSheet
from src.environment.grid_map import GridMap
from src.environment.world import World, Directions, Colors
from src.environment.camera import (Camera, FollowCamModeX, BorderCamModeX, AutoCamModeX, FollowCamModeY,
                                    BorderCamModeY, AutoCamModeY, PageCamModeY)


def main() -> None:
    """
    The main function containing the game loop
    """
    # Init pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Init screen
    pygame.display.set_caption("Joda Game")
    display_info = pygame.display.Info()
    screen = pygame.display.set_mode((World.SCREEN_WIDTH, World.SCREEN_HEIGHT))

    # Load sprite sheets and maps
    World.load_images()
    meadow_sheet = SpriteSheet("media/images/blocks/meadow_sheet")
    layer_0 = GridMap("media/maps/meadow_level_layer_0", meadow_sheet, 32)
    layer_0.load_csv()
    layer_0.build()
    layer_0.render()
    World.set_boundaries(
        -3 * layer_0.grid_size, (layer_0.map_width + 3) * layer_0.grid_size, -3 * layer_0.grid_size,
        (layer_0.map_height + 5) * layer_0.grid_size)

    # Create player
    player_1 = Player((200, 680), (41, 116), 8, World.images["player"], Directions.RIGHT, 4)

    # Create enemies
    enemy_1 = Runner((600, 800), (60, 150), 4, World.images["runner"], Directions.RIGHT, (600, 250), 5)
    enemy_2 = SniperGuy((2160, 490), (60, 110), 0, World.images["stickman"], Directions.LEFT, 32, 80, 3)
    enemy_3 = Runner((2380, 700), (60, 150), 4, World.images["runner"], Directions.RIGHT, (600, 250), 5)
    enemy_4 = SniperGuy((4080, 330), (60, 110), 0, World.images["stickman"], Directions.LEFT, 24, 50, 4)

    # Create borders
    left_wall = Border(-100, -100, 100, World.SCREEN_HEIGHT + 200)
    right_wall = Border(layer_0.map_width * layer_0.grid_size, -100, 100, World.SCREEN_HEIGHT + 200)

    # Init camera
    camera = Camera(player_1, World.SCREEN_WIDTH, World.SCREEN_HEIGHT)
    follow_cam_mode_x = FollowCamModeX(camera)
    border_cam_mode_x = BorderCamModeX(camera, left_wall.rect.right, right_wall.rect.left, (4, 6))
    auto_cam_mode_x = AutoCamModeX(camera, 1)
    follow_cam_mode_y = FollowCamModeY(camera)
    border_cam_mode_y = BorderCamModeY(camera, -2 * camera.height, layer_0.map_height * layer_0.grid_size, 180, 100)
    auto_cam_mode_y = AutoCamModeY(camera, -1)
    page_cam_mode_y = PageCamModeY(camera)
    camera.set_horizontal_method(border_cam_mode_x)
    camera.set_vertical_method(border_cam_mode_y)
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
                        screen = pygame.display.set_mode((World.SCREEN_WIDTH, World.SCREEN_HEIGHT))
                    else:
                        screen = pygame.display.set_mode((World.SCREEN_WIDTH, World.SCREEN_HEIGHT), pygame.FULLSCREEN)
                    World.FULLSCREEN = not World.FULLSCREEN
                # Check for key inputs which set the camera
                elif event.key == pygame.K_1:
                    camera.set_horizontal_method(follow_cam_mode_x)
                elif event.key == pygame.K_2:
                    camera.set_horizontal_method(border_cam_mode_x)
                elif event.key == pygame.K_3:
                    camera.set_horizontal_method(auto_cam_mode_x)
                elif event.key == pygame.K_4:
                    camera.set_vertical_method(follow_cam_mode_y)
                elif event.key == pygame.K_5:
                    camera.set_vertical_method(border_cam_mode_y)
                elif event.key == pygame.K_6:
                    camera.set_vertical_method(auto_cam_mode_y)
                elif event.key == pygame.K_7:
                    camera.set_vertical_method(page_cam_mode_y)
                elif event.key == pygame.K_8:
                    characters_list = World.players.sprites() + World.enemies.sprites()
                    character_focus_index = (character_focus_index + 1) % len(characters_list)
                    camera.set_target(characters_list[character_focus_index])
                elif event.key == pygame.K_9:
                    World.health_bars_visible = not World.health_bars_visible
                    for character in (World.players.sprites() + World.enemies.sprites()):
                        character.health_bar.toggle_on_off()
                elif event.key == pygame.K_0:
                    World.hitboxes_visible = not World.hitboxes_visible
                    for asset in (World.all_sprites.sprites()):
                        asset.toggle_hitbox_visibility()
                elif event.key == pygame.K_BACKSPACE:
                    Runner(
                        (player_1.rect.centerx + player_1.direction * (player_1.rect.width + 50),
                         player_1.rect.bottom - 90), (35, 90), 3, World.images["runner"], player_1.direction, (0, 0), 1)
                elif event.key == pygame.K_F1:  # Make player bigger
                    midbottom = player_1.rect.midbottom
                    player_1.rect.size = (player_1.rect.width * 2, player_1.rect.height * 2)
                    player_1.rect.midbottom = midbottom
                elif event.key == pygame.K_F2:  # Make player smaller
                    midbottom = player_1.rect.midbottom
                    player_1.rect.size = (player_1.rect.width / 2, player_1.rect.height / 2)
                    player_1.rect.midbottom = midbottom

        World.all_sprites.update()  # Update all assets
        camera.scroll()  # Update the camera offset

        # Update display
        screen.fill(Colors.WHITE)
        screen.blit(World.images["background"], (0, 0))
        for sprite in World.all_sprites:
            if sprite.visible:
                screen.blit(sprite.image, camera.apply_offset(sprite))
            if sprite.hitbox_visible:
                pygame.draw.rect(screen, Colors.WHITE, camera.apply_offset(sprite), 1)

        pygame.display.update()  # Update some pygame internals
        clock.tick(50)  # Set the framerate (in fps)


if __name__ == '__main__':
    main()
    pygame.quit()
