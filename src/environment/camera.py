from __future__ import annotations
from typing import Any

import pygame
from abc import ABC, abstractmethod


class Camera:
    """
    A system that makes it possible to follow an asset (e.g. player) on the screen
    """

    def __init__(self, target: Any, width: int, height: int) -> None:
        """
        Creates an instance of this class.

        Args:
            target (Any): The asset that the camera follows.
            width (int): The width of the camera frame, usually the width of the screen.
            height (int): The height of the camera frame, usually the height of the screen.
        """
        self.target = target
        self.width = width
        self.height = height
        self.offset = pygame.math.Vector2(0, 0)
        self.const = pygame.math.Vector2(-(4 / 10) * self.width, 0)

    def set_method(self, method: CameraScrollMode) -> None:
        """
        Changes the behaviour of the camera while scrolling.

        Args:
            method (CameraScrollMode): The scroll method that the camera uses.
        """
        self.method = method

    def set_target(self, target: Any) -> None:
        """
        Changes the target that the camera follows.

        Args:
            target (Any): The asset that the camera follows.
        """
        self.target = target

    def set_const(self, const_x: int | float, const_y: int | float) -> None:
        """
        Sets the position of the target relative in the camera frame.

        Args:
            const_x (int | float): The horizontal constant offset of the target.
            const_y (int | float): The vertical constant offset of the target.
        """
        self.const = pygame.math.Vector2(const_x, const_y)

    def scroll(self) -> None:
        """
        Calls the scroll method of the active scroll mode.
        """
        self.method.scroll()

    def apply_offset(self, entity: Any) -> pygame.Rect:
        """
        Retrieves the rect of the entity adapted to the camera frame.

        Args:
            entity (Any): The entity whose offset shall be calculated.

        Returns:
            pygame.Rect: The new rect of the entity that has been pushed into the camera frame.
        """
        return entity.rect.move(-self.offset)


class CameraScrollMode(ABC):
    """
    An abstract class for the implementation of different scrolling methods according to the strategy pattern.
    """

    def __init__(self, camera: Camera) -> None:
        """
        Creates an instance of this class.

        Args:
            camera (Camera): The passed camera object.
        """
        self.camera = camera

    @abstractmethod
    def scroll(self) -> None:
        """
        To be implemented in the child classes.
        """
        ...


class FollowCamMode(CameraScrollMode):
    """
    A scrolling method that keeps the target in a fixed position in the camera frame.
    """

    def __init__(self, camera: Camera) -> None:
        """
        Creates an instance of this class.

        Args:
            camera (Camera): The passed camera object.
        """
        super().__init__(camera)

    def scroll(self) -> None:
        """
        Calculates the offset between camera and screen.
        """
        self.camera.offset.x = self.camera.target.rect.centerx + self.camera.const.x


class BorderCamMode(CameraScrollMode):
    """
    Like FollowCamMode, but with defined borders that can't be seen past.
    """

    def __init__(self, camera: Camera, left_border: int, right_border: int) -> None:
        """
        Creates an instance of this class.

        Args:
            camera (Camera): The passed camera object.
            left_border (int): The horizontal position of the left border that can't be seen past.
            right_border (int): The horizontal position of the right border that can't be seen past.
        """
        super().__init__(camera)
        self.left_border = left_border
        self.right_border = right_border

    def scroll(self) -> None:
        """
        Calculates the offset between camera and screen with respect to the borders.
        """
        self.camera.offset.x = self.camera.target.rect.centerx + self.camera.const.x
        self.camera.offset.x = max(self.camera.offset.x, self.left_border)
        self.camera.offset.x = min(self.camera.offset.x, self.right_border - self.camera.width)


class AutoCamMode(CameraScrollMode):
    """
    A scrolling method that continuously scrolls with a certain speed, regardless of the target.
    """

    def __init__(self, camera: Camera, scroll_speed: int) -> None:
        """
        Creates an instance of this class.

        Args:
            camera (Camera): The passed camera object.
            scroll_speed (int): The scroll speed of the camera.
        """
        super().__init__(camera)
        self.scroll_speed = scroll_speed

    def scroll(self) -> None:
        """
        Constantly increases the offset between camera and screen.
        """
        self.camera.offset.x += self.scroll_speed
