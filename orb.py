import pygame
from object import Object


class Orb(Object):
    def __init__(self, x: int, y: int, r: int, texture_path: str) -> None:
        super().__init__(x, y, r, r, texture_path)
        self.r = r

    def update(self, player) -> bool:
        if self.object_hitbox.colliderect(player.object_hitbox):
            player.score += self.r
            player.reward += 5
            return True
        return False
