import pygame

from src.asset import Asset
from src.assets.object import Object
from src.environment.world import World, Colors

class Zone(Object):

    def __init__(self, owner: Asset, width: int | float, height: int | float, color: Colors | tuple[int] = Colors.WHITE_TRANSPARENT) -> None:
        sprite_groups = [World.all_sprites]
        super().__init__(sprite_groups=sprite_groups)
        self.visible = World.zones_visible
        self.owner = owner

        # Create alignment rectangle
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.update_position()

        # Create mask
        pygame.draw.ellipse(self.image, Colors.WHITE, (0, 0, width, height))
        self.mask = pygame.mask.from_surface(self.image)
        self.image = self.mask.to_surface(setcolor=color, unsetcolor=Colors.TRANSPARENT)

    def update(self) -> None:
        self.update_position()
        self.check_owner_alive()

    def update_position(self):
        self.rect.center = self.owner.rect.center

    def contains(self, asset) -> list[Asset]:
        return pygame.sprite.spritecollide(self, pygame.sprite.Group(asset), False, pygame.sprite.collide_mask)

    def check_owner_alive(self) -> None:
        """
        Checks if the owner is alive.
        """
        if not self.owner.alive():
            self.kill()
