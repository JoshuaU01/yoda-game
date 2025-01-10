from abc import ABC, abstractmethod
import pygame

from src.asset import Asset
from src.assets.object import Object
from src.environment.world import World, Colors


class Zone(Object, ABC):
    """
    A class for geometrical shapes that can interact with other assets like other zones.
    """

    @abstractmethod
    def __init__(
            self,
            shape: pygame.Surface,
            owner: Asset = None,
            offset: tuple[int | float, int | float] = (0, 0),
            color: Colors | tuple[int] = Colors.WHITE_TRANSPARENT) \
            -> None:
        """
        Creates an instance of this class.

        :param shape: A surface filled with the shape of the zone.
        :param owner: The asset to which this zone belongs.
        :param offset: Positional offset with respect to the owner.
        If the zone has no owner, the offset is its position.
        :param color: Color of the zone that shows if zone is visible.
        """
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
        """
        Updates the zone with every frame, if it has an owner.
        """
        if self.owner:
            self.update_position()
            self.check_owner_alive()

    def update_position(self) -> None:
        """
        Updates the zone's position with respect to its owner and the offset.
        """
        if self.owner:
            self.rect.center = (self.owner.rect.center[0] + self.offset[0], self.owner.rect.center[1] + self.offset[1])
        else:
            self.rect.center = self.offset

    def contains(self, asset) -> list[Asset]:
        """
        Checks whether an asset is inside the zone. Mask based collision check.
        The asset counts as in the zone, if at least one pixel intersects with it.

        :param asset: The asset to be checked.
        :return: The asset in a list, if it is in the zone. Otherwise, the list is empty.
        """
        return pygame.sprite.spritecollide(self, [asset], False, pygame.sprite.collide_mask)

    def check_owner_alive(self) -> None:
        """
        Checks if the owner is alive and destroys the zone if not.
        """
        if not self.owner.alive():
            self.kill()


class EllipticZone(Zone):
    """
    A specific Zone with an elliptic shape.
    """

    def __init__(
            self,
            width: int | float,
            height: int | float,
            owner: Asset = None,
            offset: tuple[int | float, int | float] = (0, 0),
            color: Colors | tuple[int] = Colors.WHITE_TRANSPARENT) \
            -> None:
        """
        Creates an instance of this class.

        :param width: The width of the ellipse.
        :param height: The height of the ellipse.
        :param owner: The asset to which this zone belongs.
        :param offset: Positional offset with respect to the owner.
        If the zone has no owner, the offset is its position.
        :param color: Color of the zone that shows if zone is visible.
        """
        ellipse_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.ellipse(ellipse_surface, Colors.WHITE, (0, 0, width, height))
        super().__init__(ellipse_surface, owner=owner, offset=offset, color=color)


class SemiEllipticZone(Zone):
    """
    A specific Zone with an elliptic shape cut in half by the x-axis.
    """

    def __init__(
            self,
            width: int | float,
            height: int | float,
            owner: Asset = None,
            offset: tuple[int | float, int | float] = (0, 0),
            flip: bool = False,
            color: Colors | tuple[int] = Colors.WHITE_TRANSPARENT) \
            -> None:
        """
        Creates an instance of this class.

        :param width: The width of the semi-ellipse.
        :param height: The height of the semi-ellipse.
        :param owner: The asset to which this zone belongs.
        :param offset: Positional offset with respect to the owner.
        :param flip: Whether the zone is flipped on the y-axis.
        If the zone has no owner, the offset is its position.
        :param color: Color of the zone that shows if zone is visible.
        """
        semi_ellipse_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.ellipse(semi_ellipse_surface, Colors.WHITE, (0, 0, width, 2 * height))
        semi_ellipse_surface = pygame.transform.flip(semi_ellipse_surface, False, flip)
        super().__init__(semi_ellipse_surface, owner=owner, offset=offset, color=color)


class RectangularZone(Zone):
    """
    A specific Zone with a rectangular shape.
    """

    def __init__(
            self,
            width: int | float,
            height: int | float,
            owner: Asset = None,
            offset: tuple[int | float, int | float] = (0, 0),
            color: Colors | tuple[int] = Colors.WHITE_TRANSPARENT) \
            -> None:
        """
        Creates an instance of this class.

        :param width: The width of the rectangle.
        :param height: The height of the rectangle.
        :param owner: The asset to which this zone belongs.
        :param offset: Positional offset with respect to the owner.
        If the zone has no owner, the offset is its position.
        :param color: Color of the zone that shows if zone is visible.
        """
        rectangle_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(rectangle_surface, Colors.WHITE, (0, 0, width, height))
        super().__init__(rectangle_surface, owner=owner, offset=offset, color=color)


class CustomZone(Zone):
    """
    A special zone that allows the user to directly pass a custom shape.
    """

    def __init__(
            self,
            shape: pygame.Surface,
            owner: Asset = None,
            offset: tuple[int | float, int | float] = (0, 0),
            color: Colors | tuple[int] = Colors.WHITE_TRANSPARENT) \
            -> None:
        """
        Creates an instance of this class.

        :param shape: A custom shape on a surface object.
        :param owner: The asset to which this zone belongs.
        :param offset: Positional offset with respect to the owner.
        If the zone has no owner, the offset is its position.
        :param color: Color of the zone that shows if zone is visible.
        """
        super().__init__(shape, owner=owner, offset=offset, color=color)
