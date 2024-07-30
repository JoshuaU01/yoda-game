import pygame

class Asset(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)  # Placeholder

    def move_with_screen(self, speed):
        self.rect.x -= speed