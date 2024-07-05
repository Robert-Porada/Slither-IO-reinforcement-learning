import pygame
import numpy as np

from object import Object
from segment import Segment

MAX_COL_CHECK_DISCT = 1000
WINDOW_DIMS = (1024, 768)

START_WIDTH = 50
START_HEIGHT = 50


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

        self.reward = 0
        self.frame_iteration = 0

        self.closest_orbs = []
        self.closest_orb_pos = []
        self.closest_enemy_segments = []
        self.closest_enemy_segments_pos = []
        self.distance_from_walls = []

    def update(self, enemies, walls, action: list, orbs) -> bool:
        self.frame_iteration += 1
        self.reward = 0
        # action = [left, right, straight, boost] in bool

        # find three closest orb local pos
        self.find_closest_orbs_local_pos(orbs)

        # find three closest enemy segments local pos
        self.find_closest_enemies_local_pos(enemies)

        # find distance from walls
        self.find_distance_from_walls(walls)

        # Moving the player based on action
        if action[3] and self.score > 0:
            self.player_speed = self.boost_speed
            self.object_hitbox.x += self.movement_vector[0] * self.player_speed
            self.object_hitbox.y += self.movement_vector[1] * self.player_speed
            self.score -= 1
        else:
            self.player_speed = self.regular_speed
            self.object_hitbox.x += self.movement_vector[0] * self.player_speed
            self.object_hitbox.y += self.movement_vector[1] * self.player_speed

        # changing player direction based on action
        if action[0]:
            self.movement_angle -= self.angle_delta
            self.movement_angle = self.movement_angle % (2 * np.pi)
        if action[1]:
            self.movement_angle += self.angle_delta
            self.movement_angle = self.movement_angle % (2 * np.pi)

        # reading keyboard inputs
        # keys = pygame.key.get_pressed()

        # moving the player manualy
        # if keys[pygame.K_SPACE] and self.score > 0:
        #     self.player_speed = self.boost_speed
        #     self.object_hitbox.x += self.movement_vector[0] * self.player_speed
        #     self.object_hitbox.y += self.movement_vector[1] * self.player_speed
        #     self.score -= 1
        # else:
        #     self.player_speed = self.regular_speed
        #     self.object_hitbox.x += self.movement_vector[0] * self.player_speed
        #     self.object_hitbox.y += self.movement_vector[1] * self.player_speed

        # changing the angle of player movement manualy
        # if keys[pygame.K_a]:
        #     self.movement_angle -= self.angle_delta
        # if keys[pygame.K_d]:
        #     self.movement_angle += self.angle_delta

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

        # checking for collisions
        # with enemy
        for enemy in enemies:
            dist_to_enemy = (
                (enemy.object_hitbox.x - self.object_hitbox.x) ** 2
                + (enemy.object_hitbox.y - self.object_hitbox.y) ** 2
            ) ** (1 / 2)
            if dist_to_enemy < MAX_COL_CHECK_DISCT:
                for segment in enemy.segments:
                    # player is killed on collision or dies of starvation
                    if (
                        self.object_hitbox.colliderect(segment.object_hitbox)
                        or self.frame_iteration > 300 + self.score * 0.75
                    ):
                        self.reward = -10
                        return True
        # with walls
        for wall in walls:
            if self.object_hitbox.colliderect(wall.object_hitbox):
                self.reward = -10
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

    def find_closest_orbs_local_pos(self, orbs):
        self.closest_orb = orbs[0]
        dist = float("INFINITY")
        for orb in orbs:
            dist_to_orb = (
                (orb.object_hitbox.x - self.object_hitbox.x) ** 2
                + (orb.object_hitbox.y - self.object_hitbox.y) ** 2
            ) ** (1 / 2)
            if dist_to_orb < dist:
                dist = dist_to_orb
                self.closest_orb = orb
            self.closest_orb_pos = [
                (
                    self.closest_orb.object_hitbox.x
                    - self.object_hitbox.x
                    - self.w / 2
                    - self.closest_orb.r / 2
                )
                / WINDOW_DIMS[0],
                (
                    self.closest_orb.object_hitbox.y
                    - self.object_hitbox.y
                    - self.h / 2
                    - self.closest_orb.r / 2
                )
                / WINDOW_DIMS[1],
            ]

    def find_closest_enemies_local_pos(self, enemies):
        self.closest_enemy_segment = enemies[0]
        dist = float("INFINITY")
        for enemy in enemies:
            for segment in enemy.segments:
                dist_to_segment = (
                    (segment.object_hitbox.x - self.object_hitbox.x) ** 2
                    + (segment.object_hitbox.y - self.object_hitbox.y) ** 2
                ) ** (1 / 2)
                if dist_to_segment < dist:
                    dist = dist_to_segment
                    self.closest_enemy_segment = segment
            self.closest_enemy_segments_pos = [
                (
                    self.closest_enemy_segment.object_hitbox.x
                    - self.object_hitbox.x
                    - self.w / 2
                    - self.closest_enemy_segment.w / 2
                )
                / WINDOW_DIMS[0],
                (
                    self.closest_enemy_segment.object_hitbox.y
                    - self.object_hitbox.y
                    - self.h / 2
                    - self.closest_enemy_segment.h / 2
                )
                / WINDOW_DIMS[1],
            ]

    def find_distance_from_walls(self, walls):
        self.distance_from_walls = []
        top_dist = (
            walls[0].object_hitbox.y
            - self.object_hitbox.y
            - self.h / 2
            - walls[0].h / 2
        )
        right_dist = (
            walls[1].object_hitbox.x
            - self.object_hitbox.x
            - self.w / 2
            + walls[1].w / 2
        )
        left_dist = (
            walls[2].object_hitbox.x
            - self.object_hitbox.x
            - self.w / 2
            - walls[2].w / 2
        )
        botoom_dist = (
            walls[3].object_hitbox.y
            - self.object_hitbox.y
            - self.h / 2
            - walls[3].h / 2
        )
        self.distance_from_walls.append(np.abs(top_dist / (WINDOW_DIMS[1] * 2)))
        self.distance_from_walls.append(np.abs(right_dist / (WINDOW_DIMS[0] * 2)))
        self.distance_from_walls.append(np.abs(left_dist / (WINDOW_DIMS[0] * 2)))
        self.distance_from_walls.append(np.abs(botoom_dist / (WINDOW_DIMS[1] * 2)))
