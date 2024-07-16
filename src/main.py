import sys
import os
import pygame

from player import Player
from enemy import Enemy
from sniper_guy import SniperGuy
from world import World
from floor import Floor
from block import Block
from bullet import Bullet

from colors import *


# Resize graphical elements to the screen size
def resize(old_size) -> int:
    return int(old_size / RESIZE_FACTOR)

# Load an image from a path and resize it
def load_image(image_path, dimensions, do_resize=True):
    image = pygame.image.load(image_path)
    #if do_resize is True:
        #dimensions = (resize(dimensions[0]), resize(dimensions[1]))
    return pygame.transform.scale(image, dimensions)


def main():
    # Init pygame
    pygame.init()
    clock = pygame.time.Clock()
    os.chdir("..")  # Work from root directory of the project to include all media and source files

    # Init screen
    RUNNING = True
    fullscreen = False
    pygame.display.set_caption("Joda Game")
    display_info = pygame.display.Info()
    screen_width = 1440#display_info.current_w
    screen_height = 810#display_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height))
    global RESIZE_FACTOR
    RESIZE_FACTOR = 950 / screen_height

    # Load and resize images
    image_player = load_image("media/images/player/ziwomol/ziwomol_v3.png", (95, 260))
    image_enemy = load_image("media/images/template/stickman.png", (140, 260))
    background = load_image("media/images/background/map_grass_background.png", (screen_width, screen_height), do_resize=False)
    image_floor = load_image("media/images/background/map_grass_floor.png", (screen_width, 180), do_resize=False)
    image_bullet = load_image("media/images/bullet/bullet_small.png", (16, 16), do_resize=False)

    # Create objects
    players = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    floors = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    p1 = Player((400, 530), (57, 156), (30,0), image_player)
    players.add(p1)
    all_sprites.add(p1)

    e1 = SniperGuy((1130, 510), (84, 156), (30,0), image_enemy)
    enemies.add(e1)
    all_sprites.add(e1)

    floor = Floor(screen_width, 145, 0, screen_height - 145, image_floor)
    floors.add(floor)
    all_sprites.add(floor)

    block_positions = [
        (100, 620),
        (200, 640),
        (300, 480)
    ]

    for pos in block_positions:
        block = Block(30, 30, pos[0], pos[1])
        blocks.add(block)
        all_sprites.add(block)

    #w1 = World(background, (screen_width, screen_height), False, False, 30)
    #all_sprites.add(w1)

    # Load blocks, items, enemies of level
    #w1.load_map()
    #for i, b in enumerate(w1.blocks):
        #all_sprites.add(w1.blocks[i])

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
                if fullscreen:
                    screen = pygame.display.set_mode((screen_width, screen_height))
                else:
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
                fullscreen = not fullscreen

        all_sprites.update(enemies, floors, blocks, screen_height)  # Update sprites
        p1.shoot(image_bullet)
        if p1.die():
            print("Player p1 died.")
            return None

        # Update enemy
        if e1.die():
            print("Enemy e1 died.")
            return None

        # Update movement of player's bullets
        for i, b in enumerate(p1.bullets):
            destroy = b.collide(all_sprites[1:])
            b.move()
            if destroy:  # If bullet hit an object, destroy it
                del p1.bullets[i]

        # Update display
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        screen.blit(image_floor, (0, screen_height - 180))
        all_sprites.draw(screen)
        #p1.draw(screen, True)

        pygame.display.update()
        clock.tick(60)  # Set the framerate to 60fps


# Call the main function if running this script
if __name__ == '__main__':
    main()
    pygame.quit()