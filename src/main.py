import sys
import os
import pygame

import player
import enemy
import sniper_guy
import world

def check_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()

def check_collision(hitboxes):
    if hitboxes[0].collidelist(hitboxes[1:]) != -1:
        return True

def resize(old_size) -> int:
    return int(old_size / resize_factor)

if __name__ == '__main__':

    pygame.init()
    clock = pygame.time.Clock()
    os.chdir("..")  # Work from root directory of the project to include all media and source files

    pygame.display.set_caption("Joda Game")

    display_info = pygame.display.Info()
    screen_width = display_info.current_w
    screen_height = display_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    global resize_factor
    resize_factor = 950 / screen_height

    image_player = pygame.image.load("media/images/player/ziwomol/ziwomol_v3.png")
    image_player = pygame.transform.scale(image_player, (resize(95), resize(260)))

    image_enemy = pygame.image.load("media/images/template/stickman.png")
    image_enemy = pygame.transform.scale(image_enemy, (resize(140), resize(260)))


    player = player.Player(resize(300), resize(540), resize(96), resize(128), resize(10), resize(0), resize(95), resize(260), image_player)
    enemy = sniper_guy.SniperGuy(resize(1200), resize(540), resize(96), resize(128), resize(10), resize(0), resize(140), resize(260), image_enemy)
    world = world.World("media/images/background/map_gras.png", (screen_width, screen_height), False, False, resize(30))

    while True:
        check_exit()  # Check for key inputs which close the game

        player.move()
        player.jump(world.gravity)

        # Update display
        world.draw(screen)
        player.update_hitbox()
        player.draw(screen, show_hitbox=True)
        enemy.update_hitbox()
        enemy.draw(screen, show_hitbox=True)

        hitboxes = [player.hitbox, enemy.hitbox]
        if check_collision(hitboxes):
            player.movement_lock[1] = True
        else:
            player.movement_lock[1] = False
        pygame.display.update()
        clock.tick(60)