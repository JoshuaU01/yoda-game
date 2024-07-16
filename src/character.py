import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, position, size, velocity, image):
        super().__init__()
        self.position = pygame.math.Vector2(position[0], position[1])
        self.size = pygame.math.Vector2(size[0], size[1])
        self.velocity = pygame.math.Vector2(velocity[0], velocity[1])
        self.image = pygame.transform.scale(image, (self.size.x, self.size.y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.position.x, self.position.y)