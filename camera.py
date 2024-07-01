import pygame


class Camera:
    def __init__(self, x: int, y: int, player_dims: tuple, window_dims: tuple) -> None:
        self.x = x
        self.y = y
        self.player_dims = player_dims
        self.window_dims = window_dims

    def update(self, playerx, playery):
        self.x = playerx
        self.y = playery

    def translate(self, x, y):
        return (
            x - self.x + self.window_dims[0] / 2 - self.player_dims[0] / 2,
            y - self.y + self.window_dims[1] / 2 - self.player_dims[1] / 2,
        )
