import pygame
import numpy as np

from object import Object
from segment import Segment


class Enemy(Object):
    def __init__(self, x: int, y: int, w: int, h: int, texture_path: str) -> None:
        super().__init__(x, y, w, h, texture_path)
        self.w = w
        self.h = h

        self.player_speed = 3

        self.movement_vector = [0, -1]

        self.score = 0

        self.min_snake_len = 4
        self.segment_dis = self.w / 3
        self.segments = []

    def update(self, orbs) -> None:
        # find closest orb
        closest_orb = orbs[0]
        dist = float("INFINITY")
        for orb in orbs:
            dist_to_orb = (
                (orb.object_hitbox.x - self.object_hitbox.x) ** 2
                + (orb.object_hitbox.y - self.object_hitbox.y) ** 2
            ) ** (1 / 2)
            if dist_to_orb < dist:
                dist = dist_to_orb
                closest_orb = orb

        # calculate direction
        vector_len = (
            (closest_orb.object_hitbox.x - self.object_hitbox.x) ** 2
            + (closest_orb.object_hitbox.y - self.object_hitbox.y) ** 2
        ) ** (1 / 2)
        if vector_len != 0:
            self.movement_vector = [
                (closest_orb.object_hitbox.x - self.object_hitbox.x) / vector_len,
                (closest_orb.object_hitbox.y - self.object_hitbox.y) / vector_len,
            ]

        # moving the player
        self.object_hitbox.x += self.movement_vector[0] * self.player_speed
        self.object_hitbox.y += self.movement_vector[1] * self.player_speed

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
                "resource/main_body_enemy.png",
            )
            self.segments.append(new_segment)
        elif self.score // 100 + self.min_snake_len < len(self.segments):
            self.segments.pop()
