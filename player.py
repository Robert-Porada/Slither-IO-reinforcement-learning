import pygame
import numpy as np

from object import Object
from segment import Segment

MAX_COL_CHECK_DISCT = 1000

class Player(Object):
    def __init__(self, x: int, y: int, w: int, h: int, texture_path: str) -> None:
        super().__init__(x, y, w, h, texture_path)
        self.w = w
        self.h = h

        self.angle_delta = np.pi / 50
        self.movement_angle = np.pi * 3 / 2

        self.player_speed = 5
        self.regular_speed = 5
        self.boost_speed = 10
        self.movement_vector = [0, -1]

        self.score = 0

        self.min_snake_len = 4
        self.segment_dis = self.w / 3
        self.segments = []

    def update(self, enemies) -> bool:
        print(self.score)
        keys = pygame.key.get_pressed()

        # moving the player
        if keys[pygame.K_SPACE] and self.score > 0:
            self.player_speed = self.boost_speed
            self.object_hitbox.x += self.movement_vector[0] * self.player_speed
            self.object_hitbox.y += self.movement_vector[1] * self.player_speed
            self.score -= 1
        else:
            self.player_speed = self.regular_speed
            self.object_hitbox.x += self.movement_vector[0] * self.player_speed
            self.object_hitbox.y += self.movement_vector[1] * self.player_speed

        # changing the angle of player movement
        if keys[pygame.K_a]:
            self.movement_angle -= self.angle_delta
        if keys[pygame.K_d]:
            self.movement_angle += self.angle_delta

        self.movement_vector[0] = np.cos(self.movement_angle)
        self.movement_vector[1] = np.sin(self.movement_angle)

        # adding or removing a segment
        self.add_or_remove_player_segments()

        # Updating segments
        for i, segment in enumerate(self.segments):
            if i == 0:
                segment.update(
                    [self.object_hitbox.x, self.object_hitbox.y],
                    self.segment_dis,
                    self.player_speed,
                )
            else:
                segment.update(
                    [
                        self.segments[i - 1].object_hitbox.x,
                        self.segments[i - 1].object_hitbox.y,
                    ],
                    self.segment_dis,
                    self.player_speed,
                )
        
        for enemy in enemies:
            dist_to_enemy = ((enemy.object_hitbox.x - self.object_hitbox.x)**2 + (enemy.object_hitbox.y - self.object_hitbox.y)**2)**(1/2)
            if dist_to_enemy < MAX_COL_CHECK_DISCT:
                for segment in enemy.segments:
                    if self.object_hitbox.colliderect(segment.object_hitbox):
                        return True
        return False

    def render(self, window: object, camera: object) -> None:
        window.blit(
            self.texture, camera.translate(self.object_hitbox.x, self.object_hitbox.y)
        )
        for segment in self.segments:
            window.blit(
                segment.texture,
                camera.translate(segment.object_hitbox.x, segment.object_hitbox.y),
            )

    def add_or_remove_player_segments(self):
        if self.score // 100 + self.min_snake_len > len(self.segments):
            if len(self.segments) == 0:
                new_x = (
                    self.object_hitbox.x
                    - self.movement_vector[0]
                    * self.object_hitbox.w
                    * self.segment_dis
                    / self.w
                )
                new_y = (
                    self.object_hitbox.y
                    - self.movement_vector[1]
                    * self.object_hitbox.h
                    * self.segment_dis
                    / self.w
                )
            else:
                new_x = (
                    self.segments[-1].object_hitbox.x
                    - self.movement_vector[0]
                    * self.segments[-1].object_hitbox.w
                    * self.segment_dis
                    / self.w
                )
                new_y = (
                    self.segments[-1].object_hitbox.y
                    - self.movement_vector[1]
                    * self.segments[-1].object_hitbox.h
                    * self.segment_dis
                    / self.w
                )
            new_segment = Segment(
                new_x,
                new_y,
                self.w,
                self.h,
                "resource/main_body.png",
            )
            self.segments.append(new_segment)
        elif self.score // 100 + self.min_snake_len < len(self.segments):
            self.segments.pop()
