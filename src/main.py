import sys
import os
import pygame

import player
import enemy
import sniper_guy
import world
import bullet


def check_collision(hitboxes):
    if hitboxes[0].collidelist(hitboxes[1:]) != -1:
        return True

# Resize graphical elements to the screen size
def resize(old_size) -> int:
    return int(old_size / RESIZE_FACTOR)

# Load an image from a path and resize it
def load_image(image_path, dimensions, do_resize=True):
    image = pygame.image.load(image_path)
    if do_resize is True:
        dimensions = (resize(dimensions[0]), resize(dimensions[1]))
    return pygame.transform.scale(image, dimensions)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    os.chdir("..")  # Work from root directory of the project to include all media and source files

    pygame.display.set_caption("Joda Game")

    display_info = pygame.display.Info()
    screen_width = display_info.current_w
    screen_height = display_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    global RESIZE_FACTOR
    RESIZE_FACTOR = 950 / screen_height

    # Load and resize images
    image_player = load_image("media/images/player/ziwomol/ziwomol_v3.png", (95, 260))
    image_enemy = load_image("media/images/template/stickman.png", (140, 260))
    image_world = load_image("media/images/background/map_gras.png", (screen_width, screen_height), do_resize=False)

    # Create objects
    p1 = player.Player(resize(300), resize(540), resize(96), resize(128), resize(10), resize(0), resize(95), resize(260), image_player)
    e1 = sniper_guy.SniperGuy(resize(1200), resize(540), resize(96), resize(128), resize(10), resize(0), resize(140), resize(260), image_enemy)
    w1 = world.World(image_world, (screen_width, screen_height), False, False, resize(30))

    # Start the game loop
    while True:
        # Get input
        for event in pygame.event.get():
            # Check for key inputs which close the game
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None

        # Update movement
        p1.move()
        p1.jump(w1.gravity)
        p1.shoot()
        for bullet in p1.bullets:
            bullet.move()

        # Update display
        w1.draw(screen)
        p1.update_hitbox()
        p1.draw(screen, show_hitbox=True)
        e1.update_hitbox()
        e1.draw(screen, show_hitbox=True)
        for bullet in p1.bullets:
            bullet.draw(screen)

        hitboxes = [p1.hitbox, e1.hitbox]
        if check_collision(hitboxes):
            p1.movement_lock[1] = True
        else:
            p1.movement_lock[1] = False
        pygame.display.update()
        clock.tick(60)  # Set the framerate to 60fps


# Call the main function if running this script
if __name__ == '__main__':
    main()
    pygame.quit()