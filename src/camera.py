import pygame
from abc import ABC, abstractmethod


class Camera(ABC):
    def __init__(self, target, width, height):
        self.target = target
        self.width = width
        self.height = height
        self.offset = pygame.math.Vector2(0, 0)
        self.const = pygame.math.Vector2(-(4 / 10) * self.width, 0)

    def set_method(self, method):
        self.method = method

    def set_target(self, target):
        self.target = target

    def set_const(self, const_x, const_y):
        self.const = pygame.math.Vector2(const_x, const_y)

    def scroll(self):
        self.method.scroll()

    def apply_offset(self, entity):
        return entity.rect.move(-self.offset)


class CameraScrollMode(ABC):
    def __init__(self, camera):
        self.camera = camera

    @abstractmethod
    def scroll(self):
        pass


class FollowCamMode(CameraScrollMode):
    def __init__(self, camera):
        super().__init__(camera)

    def scroll(self):
        self.camera.offset.x = self.camera.target.rect.centerx + self.camera.const.x


class BorderCamMode(CameraScrollMode):
    def __init__(self, camera, left_border, right_border):
        super().__init__(camera)
        self.left_border = left_border
        self.right_border = right_border

    def scroll(self):
        self.camera.offset.x = self.camera.target.rect.centerx + self.camera.const.x
        self.camera.offset.x = max(self.camera.offset.x, self.left_border)
        self.camera.offset.x = min(self.camera.offset.x, self.right_border - self.camera.width)


class AutoCamMode(CameraScrollMode):
    def __init__(self, camera, scroll_speed):
        super().__init__(camera)
        self.scroll_speed = scroll_speed

    def scroll(self):
        self.camera.offset.x += self.scroll_speed
