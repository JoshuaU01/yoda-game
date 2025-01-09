from abc import ABC, abstractmethod
import pygame

from src.asset import Asset
from src.assets.object import Object
from src.environment.world import World, Colors


class Zone(Object, ABC):

    @abstractmethod
    def __init__(
            self,
            owner: Asset,
            shape: pygame.Surface,
            offset: tuple[int | float, int | float] = (0, 0),
            color: Colors | tuple[int] = Colors.WHITE_TRANSPARENT) -> None:
        sprite_groups = [World.all_sprites]
        super().__init__(sprite_groups=sprite_groups)
        self.visible = World.zones_visible
        self.owner = owner

        # Create alignment rectangle to make zone stick to its owner
        self.rect = shape.get_rect()
        self.offset = offset
        self.update_position()

        # Create mask for collision check and image for visualisation
        self.mask = pygame.mask.from_surface(shape)
        self.image = self.mask.to_surface(setcolor=color, unsetcolor=Colors.TRANSPARENT)

    def update(self) -> None:
        self.update_position()
        self.check_owner_alive()

    def update_position(self):
        self.rect.center = (self.owner.rect.center[0] + self.offset[0], self.owner.rect.center[1] + self.offset[1])

    def contains(self, asset) -> list[Asset]:
        return pygame.sprite.spritecollide(self, [asset], False, pygame.sprite.collide_mask)

    def check_owner_alive(self) -> None:
        """
        Checks if the owner is alive.
        """
        if not self.owner.alive():
            self.kill()


class EllipticZone(Zone):
    def __init__(
            self,
            owner: Asset,
            width: int | float,
            height: int | float,
            offset: tuple[int | float, int | float] = (0, 0),
            color: Colors | tuple[int] = Colors.WHITE_TRANSPARENT):
        ellipse_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.ellipse(ellipse_surface, Colors.WHITE, (0, 0, width, height))
        super().__init__(owner, ellipse_surface, offset=offset, color=color)


class SemiEllipticZone(Zone):
    def __init__(
            self,
            owner: Asset,
            width: int | float,
            height: int | float,
            offset: tuple[int | float, int | float] = (0, 0),
            flip: bool = False,
            color: Colors | tuple[int] = Colors.WHITE_TRANSPARENT):
        semi_ellipse_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.ellipse(semi_ellipse_surface, Colors.WHITE, (0, 0, width, 2 * height))
        semi_ellipse_surface = pygame.transform.flip(semi_ellipse_surface, False, flip)
        super().__init__(owner, semi_ellipse_surface, offset=offset, color=color)


class RectangularZone(Zone):
    def __init__(
            self,
            owner: Asset,
            width: int | float,
            height: int | float,
            offset: tuple[int | float, int | float] = (0, 0),
            color: Colors | tuple[int] = Colors.WHITE_TRANSPARENT):
        rectangle_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(rectangle_surface, Colors.WHITE, (0, 0, width, height))
        super().__init__(owner, rectangle_surface, offset=offset, color=color)
