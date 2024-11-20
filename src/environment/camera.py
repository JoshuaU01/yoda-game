from __future__ import annotations

from typing import Any, Optional

import pygame
from abc import ABC, abstractmethod

from src.environment.world import World


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
        self.const = pygame.math.Vector2(-(4 / 10) * self.width, -(4 / 10) * self.height)

        self.horizontal_method = None
        self.vertical_method = None

    def set_horizontal_method(self, method: CameraScrollMode) -> None:
        """
        Changes the behaviour of the camera on the x-axis while scrolling.

        Args:
            method (CameraScrollMode): The scroll method that the camera uses.
        """
        self.horizontal_method = method

    def set_vertical_method(self, method: CameraScrollMode) -> None:
        """
        Changes the behaviour of the camera on the y-axis while scrolling.

        Args:
            method (CameraScrollMode): The scroll method that the camera uses.
        """
        self.vertical_method = method

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
        if self.horizontal_method:
            self.horizontal_method.scroll()
        if self.vertical_method:
            self.vertical_method.scroll()

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


class FollowCamModeX(CameraScrollMode):
    """
    A scrolling method that follows the target in the camera frame.
    """

    def __init__(self, camera: Camera, left_border: Optional[int] = None, right_border: Optional[int] = None, direction_switch_scroll_speed: tuple[int, int] = (0, 0)) -> None:
        """
        Creates an instance of this class.

        Args:
            camera (Camera): The passed camera object.
            left_border (int): The horizontal position of the left border that can't be seen past.
            right_border (int): The horizontal position of the right border that can't be seen past.
            direction_switch_scroll_speed (tuple[int, int]): Additional scroll speed (left and right) that is applied when the target is switching its direction.
        """
        super().__init__(camera)
        self.left_border = left_border
        self.right_border = right_border
        self.direction_switch_scroll_speed = direction_switch_scroll_speed

    def scroll(self) -> None:
        """
        Calculates the offset between camera and screen with respect to the borders.
        This mode also dynamically adapts the constant offset of the target, depending on the direction it is moving towards.
        The condition for this behaviour to appear is direction_switch_scroll_speed > 0.
        """
        # Adjust the relative position of the target in the camera frame (const)
        if self.camera.target.velocity.x < 0 and self.camera.const.x > -(6 / 10) * self.camera.width:  # Movement to the left
            self.camera.const.x = max(self.camera.const.x - self.direction_switch_scroll_speed[0], -(6 / 10) * self.camera.width)
        elif self.camera.target.velocity.x > 0 and self.camera.const.x < -(4 / 10) * self.camera.width:  # Movement to the right
            self.camera.const.x = min(self.camera.const.x + self.direction_switch_scroll_speed[1], -(4 / 10) * self.camera.width)

        # Calculate the new camera offset
        self.camera.offset.x = self.camera.target.rect.centerx + self.camera.const.x

        # Mind the borders, if specified
        if self.left_border is not None:
            self.camera.offset.x = max(self.camera.offset.x, self.left_border)
        if self.right_border is not None:
            self.camera.offset.x = min(self.camera.offset.x, self.right_border - self.camera.width)


class AutoCamModeX(CameraScrollMode):
    """
    A scrolling method that continuously scrolls with a certain speed, regardless of the target.
    """

    def __init__(self, camera: Camera, scroll_speed: int, left_border: Optional[int] = None, right_border: Optional[int] = None) -> None:
        """
        Creates an instance of this class.

        Args:
            camera (Camera): The passed camera object.
            scroll_speed (int): The scroll speed of the camera.
        """
        super().__init__(camera)
        self.scroll_speed = scroll_speed
        self.left_border = left_border
        self.right_border = right_border

    def scroll(self) -> None:
        """
        Constantly increases the offset between camera and screen.
        """
        self.camera.offset.x += self.scroll_speed

        # Mind the borders, if specified
        if self.left_border is not None:
            self.camera.offset.x = max(self.camera.offset.x, self.left_border)
        if self.right_border is not None:
            self.camera.offset.x = min(self.camera.offset.x, self.right_border - self.camera.width)


class PageCamModeX(CameraScrollMode):
    """
    A scrolling mode that turns the page when the target exceeds the borders of the camera frame.
    """

    def __init__(self, camera: Camera, left_border: Optional[int] = None,
                 right_border: Optional[int] = None) -> None:
        """
        Creates an instance of this class.

        Args:
            camera (Camera): The passed camera object.
        """
        super().__init__(camera)
        self.left_border = left_border
        self.right_border = right_border

    def scroll(self) -> None:
        """
        Increases or decreases the camera offset by its width, depending on the page the target is in.
        """
        if self.camera.target.rect.right - self.camera.offset.x < 0:  # Scroll left
            self.camera.offset.x -= self.camera.width
        elif self.camera.target.rect.left - self.camera.offset.x > self.camera.width:  # Scroll right
            self.camera.offset.x += self.camera.width

        # Mind the borders, if specified
        if self.left_border is not None:
            self.camera.offset.x = max(self.camera.offset.x, self.left_border)
        if self.right_border is not None:
            self.camera.offset.x = min(self.camera.offset.x, self.right_border - self.camera.width)

class FollowCamModeY(CameraScrollMode):
    """
    Scrolls the vertical axis. Uses borders that can not be seen past and scrolling thresholds.
    """

    def __init__(self, camera: Camera, upper_border: Optional[int] = None, lower_border: Optional[int] = None, upper_threshold: int = 0, lower_threshold: int = 0) -> None:
        """
        Creates an instance of this class.

        Args:
            camera (Camera): The passed camera object.
            upper_border (int): The vertical position of the upper border that can't be seen past.
            lower_border (int): The vertical position of the lower border that can't be seen past.
            upper_threshold (int): The upwards change of the targets position must be greater than this value to scroll the camera up.
            lower_threshold (int): The downwards change of the targets position must be greater than this value to scroll the camera down.
        """
        super().__init__(camera)
        self.upper_border = upper_border
        self.lower_border = lower_border
        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold

    def scroll(self) -> None:
        """
        Calculates the offset between camera and screen with respect to the borders and thresholds.
        The borders work just like in the BorderCamModeX mode.
        The thresholds (up and down) must be overcome in order to scroll the camera. This prevents hectic camera movement on the y-axis.
        """
        # Calculate the difference between new and current offset
        offset_diff = self.camera.target.rect.centery + self.camera.const.y - self.camera.offset.y

        # Mind the thresholds, if specified and calculate the new offset
        if offset_diff < -self.upper_threshold:
            self.camera.offset.y = self.camera.target.rect.centery + self.camera.const.y + self.upper_threshold
        elif offset_diff > self.lower_threshold:
            self.camera.offset.y = self.camera.target.rect.centery + self.camera.const.y - self.lower_threshold

        # Mind the borders, if specified
        if self.upper_border is not None:
            self.camera.offset.y = max(self.camera.offset.y, self.upper_border)
        if self.lower_border is not None:
            self.camera.offset.y = min(self.camera.offset.y, self.lower_border - self.camera.height)


class AutoCamModeY(CameraScrollMode):
    """
    A scrolling method that continuously scrolls with a certain speed, regardless of the target.
    """

    def __init__(self, camera: Camera, scroll_speed: int, upper_border: Optional[int] = None, lower_border: Optional[int] = None) -> None:
        """
        Creates an instance of this class.

        Args:
            camera (Camera): The passed camera object.
            scroll_speed (int): The scroll speed of the camera.
        """
        super().__init__(camera)
        self.scroll_speed = scroll_speed
        self.upper_border = upper_border
        self.lower_border = lower_border

    def scroll(self) -> None:
        """
        Constantly increases the offset between camera and screen.
        """
        self.camera.offset.y += self.scroll_speed

        # Mind the borders, if specified
        if self.upper_border is not None:
            self.camera.offset.y = max(self.camera.offset.y, self.upper_border)
        if self.lower_border is not None:
            self.camera.offset.y = min(self.camera.offset.y, self.lower_border - self.camera.height)


class PageCamModeY(CameraScrollMode):
    """
    A scrolling mode that turns the page when the target exceeds the borders of the camera frame.
    """

    def __init__(self, camera: Camera, upper_border: Optional[int] = None, lower_border: Optional[int] = None) -> None:
        """
        Creates an instance of this class.

        Args:
            camera (Camera): The passed camera object.
        """
        super().__init__(camera)
        self.upper_border = upper_border
        self.lower_border = lower_border

    def scroll(self) -> None:
        """
        Increases or decreases the camera offset by its height, depending on the page the target stands on.
        """
        if self.camera.target.rect.bottom - self.camera.offset.y < 0:  # Scroll up
            self.camera.offset.y -= self.camera.height
        elif self.camera.target.rect.bottom - self.camera.offset.y > self.camera.height:  # Scroll down
            self.camera.offset.y += self.camera.height

        # Mind the borders, if specified
        if self.upper_border is not None:
            self.camera.offset.y = max(self.camera.offset.y, self.upper_border)
        if self.lower_border is not None:
            self.camera.offset.y = min(self.camera.offset.y, self.lower_border - self.camera.height)

class IndicatorCamModeY:
    pass