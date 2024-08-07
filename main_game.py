import pygame
import random

from player import Player
from orb import Orb
from camera import Camera
from enemy_ai import Enemy
from font_render import FontRenderer
from walls import Wall

BACKGROUND_COLOR = (40, 60, 60)
WINDOW_DIMS = (1024, 768)

START_WIDTH = 50
START_HEIGHT = 50

PLAYER_START_POS_X = 0
PLAYER_START_POS_Y = 0

FPS = 120
NUM_ORBS = 100
MIN_ORB_SIZE = 10
MAX_ORB_SIZE = 40

NUM_OF_ENEMIES = 3

WALL_HEIGHT = 20
WALL_PADDING = 70

PLAYER_SEGMENT_FILE_PATH = "resource/main_body.png"
ENEMY_SEGMENT_FILE_PATH = "resource/main_body_enemy.png"
WALL_FILE_PATH = "resource/wall.png"

orb_color_texture_paths = [
    "resource/Orb_dark_blue.png",
    "resource/Orb_light_blue.png",
    "resource/Orb_Pink.png",
    "resource/Orb_teal.png",
]


class MainGame:
    def __init__(self) -> None:
        pygame.init()

        self.window_dims = WINDOW_DIMS
        self.window_color = BACKGROUND_COLOR
        self.window = pygame.display.set_mode(self.window_dims)
        self.quit_game = False
        self.clock = pygame.time.Clock()

        self.player = Player(
            PLAYER_START_POS_X,
            PLAYER_START_POS_Y,
            START_WIDTH,
            START_HEIGHT,
            PLAYER_SEGMENT_FILE_PATH,
        )

        self.camera = Camera(
            PLAYER_START_POS_X,
            PLAYER_START_POS_Y,
            (self.player.w, self.player.h),
            WINDOW_DIMS,
        )

        self.orbs = []
        self.enemies = []
        self.font_renderer = FontRenderer()

        # Creating walls
        self.wall_top = Wall(
            self.window_dims[0] * -1 - WALL_PADDING,
            self.window_dims[1] * -1 - WALL_PADDING,
            self.window_dims[0] * 2 + WALL_PADDING * 2,
            WALL_HEIGHT,
            WALL_FILE_PATH,
        )
        self.wall_right = Wall(
            self.window_dims[0] * 1 + WALL_PADDING,
            self.window_dims[1] * -1 - WALL_PADDING,
            WALL_HEIGHT,
            self.window_dims[1] * 2 + WALL_PADDING * 2 + WALL_HEIGHT,
            WALL_FILE_PATH,
        )
        self.wall_left = Wall(
            self.window_dims[0] * -1 - WALL_PADDING,
            self.window_dims[1] * -1 - WALL_PADDING,
            WALL_HEIGHT,
            self.window_dims[1] * 2 + WALL_PADDING * 2 + WALL_HEIGHT,
            WALL_FILE_PATH,
        )
        self.wall_bottom = Wall(
            self.window_dims[0] * -1 - WALL_PADDING,
            self.window_dims[1] * 1 + WALL_PADDING,
            self.window_dims[0] * 2 + WALL_PADDING * 2,
            WALL_HEIGHT,
            WALL_FILE_PATH,
        )
        self.walls = [self.wall_top, self.wall_right, self.wall_left, self.wall_bottom]

        self.action = [0, 0, 0, 0]
        self.game_over = False
        self.player_score_before_death = 0

    def initialize(self):
        self.player.frame_iteration = 0
        self.player.score = 0

        if self.player:
            del self.player
        self.player = Player(
            PLAYER_START_POS_X,
            PLAYER_START_POS_Y,
            START_WIDTH,
            START_HEIGHT,
            PLAYER_SEGMENT_FILE_PATH,
        )

        self.orbs.clear()
        for i in range(NUM_ORBS):
            randX = random.randint(self.window_dims[0] * -1, self.window_dims[0])
            randY = random.randint(self.window_dims[1] * -1, self.window_dims[1])
            randR = random.randint(MIN_ORB_SIZE, MAX_ORB_SIZE)
            randTexture = random.choice(orb_color_texture_paths)

            newOrb = Orb(randX, randY, randR, randTexture)
            self.orbs.append(newOrb)

        self.enemies.clear()
        for i in range(NUM_OF_ENEMIES):
            new_enemy = Enemy(
                random.randint(100, WINDOW_DIMS[0]),
                random.randint(100, WINDOW_DIMS[1]),
                START_WIDTH,
                START_HEIGHT,
                ENEMY_SEGMENT_FILE_PATH,
            )
            self.enemies.append(new_enemy)

    def play(self, action) -> None:
        if self.quit_game == False:
            self.update(action)
            self.render()
        return self.player.reward, self.game_over, self.player.score

    def update(self, action) -> None:
        self.game_over = False
        self.clock.tick(FPS)

        # Updating window events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game = True

        # Updating player events
        if self.player.update(self.enemies, self.walls, action, self.orbs):
            # if player dies:
            print("GAME OVER")
            print("RESTARTING GAME")
            # Not needed for ai
            # for segment in self.player.segments:
            #     segment_x = segment.object_hitbox.x
            #     segment_y = segment.object_hitbox.y
            #     randTexture = random.choice(orb_color_texture_paths)
            #     new_orb = Orb(segment_x, segment_y, 40, randTexture)
            #     self.orbs.append(new_orb)
            # del self.player.segments
            self.game_over = True
            # self.initialize()

        # Updating orb events
        for orb in self.orbs:
            if orb.update(self.player):
                self.orbs.remove(orb)
                if len(self.orbs) <= NUM_ORBS:
                    randX = random.randint(
                        self.window_dims[0] * -1, self.window_dims[0]
                    )
                    randY = random.randint(
                        self.window_dims[1] * -1, self.window_dims[1]
                    )
                    randR = random.randint(MIN_ORB_SIZE, MAX_ORB_SIZE)
                    randTexture = random.choice(orb_color_texture_paths)

                    newOrb = Orb(randX, randY, randR, randTexture)
                    self.orbs.append(newOrb)

            for enemy in self.enemies:
                if orb.update(enemy):
                    if orb in self.orbs:
                        self.orbs.remove(orb)
                    if len(self.orbs) <= NUM_ORBS:
                        randX = random.randint(
                            self.window_dims[0] * -1, self.window_dims[0]
                        )
                        randY = random.randint(
                            self.window_dims[1] * -1, self.window_dims[1]
                        )
                        randR = random.randint(MIN_ORB_SIZE, MAX_ORB_SIZE)
                        randTexture = random.choice(orb_color_texture_paths)

                        newOrb = Orb(randX, randY, randR, randTexture)
                        self.orbs.append(newOrb)

        # Updating enemy events
        for i, enemy in enumerate(self.enemies):
            if enemy.update(self.orbs, self.player):
                # if enemy dies:
                print("ENEMY KILLED")
                self.player.score += 100
                for segment in enemy.segments:
                    segment_x = segment.object_hitbox.x
                    segment_y = segment.object_hitbox.y
                    randTexture = random.choice(orb_color_texture_paths)
                    new_orb = Orb(segment_x, segment_y, 40, randTexture)
                    self.orbs.append(new_orb)
                del enemy
                self.enemies.pop(i)
                # add a new enemy
                new_enemy = Enemy(
                    random.randint(100, WINDOW_DIMS[0]),
                    random.randint(100, WINDOW_DIMS[1]),
                    START_WIDTH,
                    START_HEIGHT,
                    ENEMY_SEGMENT_FILE_PATH,
                )
                self.enemies.append(new_enemy)

        # Updating camera
        self.camera.update(self.player.object_hitbox.x, self.player.object_hitbox.y)

    def render(self) -> None:
        self.window.fill(self.window_color)
        self.player.render(self.window, self.camera)
        for orb in self.orbs:
            orb.render(self.window, self.camera)
        for enemy in self.enemies:
            enemy.render(self.window, self.camera)
        self.wall_top.render(self.window, self.camera)
        self.wall_right.render(self.window, self.camera)
        self.wall_left.render(self.window, self.camera)
        self.wall_bottom.render(self.window, self.camera)
        self.font_renderer.render_font(self.window, self.player.score)
        pygame.display.update()
