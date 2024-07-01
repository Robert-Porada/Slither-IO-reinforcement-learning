import pygame
import numpy as np


class Player:
    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        self.w = w
        self.h = h
        self.player_hitbox = pygame.Rect(x, y, w, h)
        image = pygame.image.load("resource/main_body.png")
        self.texture = pygame.transform.scale(image, (w, h))

        self.angle_delta = np.pi / 50
        self.movement_angle = np.pi / 2

        self.player_speed = 5
        self.boost_speed = 10
        self.movement_vector = [0, -1]
        self.score = 0

    def update(self) -> None:
        print(self.score)
        keys = pygame.key.get_pressed()

        # moving the player
        if keys[pygame.K_SPACE]:
            self.player_hitbox.x += self.movement_vector[0] * self.boost_speed
            self.player_hitbox.y += self.movement_vector[1] * self.boost_speed
        else:
            self.player_hitbox.x += self.movement_vector[0] * self.player_speed
            self.player_hitbox.y += self.movement_vector[1] * self.player_speed

        # changing the angle of player movement
        if keys[pygame.K_a]:
            self.movement_angle += self.angle_delta
        if keys[pygame.K_d]:
            self.movement_angle -= self.angle_delta

        self.movement_vector[0] = np.cos(self.movement_angle)
        self.movement_vector[1] = np.sin(self.movement_angle)

    def render(self, window: object, camera: object) -> None:
        window.blit(
            self.texture, camera.translate(self.player_hitbox.x, self.player_hitbox.y)
        )
