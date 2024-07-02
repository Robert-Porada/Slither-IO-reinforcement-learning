import pygame

from object import Object

class Wall(Object):
    def __init__(self, x, y, w, h, texture_path) -> None:
        super().__init__(x, y, w, h, texture_path)