import pygame

from asset import Asset

class Character(Asset):
    def __init__(self, position, size, speed, image, lives=1000):
        super().__init__()
        self.image = pygame.transform.scale(image, (size[0], size[1]))
        self.rect = self.image.get_rect()
        self.rect.topleft = (position[0], position[1])
        self.velocity = pygame.math.Vector2()

        self.speed = speed
        self.lives = lives

    def lose_lives(self, amount):
        self.lives -= amount

    def check_alive(self):
        if self.lives <= 0:
            print(f"{self.__str__()} has died.")
            self.kill()
            return False
        return True