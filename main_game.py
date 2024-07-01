import pygame
import random

from player import Player
from orb import Orb


START_WIDTH = 50
START_HEIGHT = 50
FPS = 60
NUM_ORBS = 10
MIN_ORB_SIZE = 10
MAX_ORB_SIZE = 40

orb_color_texture_paths = [
    "resource/Orb_dark_blue.png",
    "resource/Orb_light_blue.png",
    "resource/Orb_Pink.png",
    "resource/Orb_teal.png",
]


class MainGame:
    def __init__(self) -> None:
        self.window_dims = (1024, 768)
        self.window_color = (40, 60, 60)
        self.window = pygame.display.set_mode(self.window_dims)
        self.quit_game = False
        self.clock = pygame.time.Clock()

        self.player = Player(
            0,
            0,
            START_WIDTH,
            START_HEIGHT,
        )

        self.orbs = []

    def initialize(self):
        for i in range(NUM_ORBS):
            randX = random.randint(0, self.window_dims[0])
            randY = random.randint(0, self.window_dims[1])
            randR = random.randint(MIN_ORB_SIZE, MAX_ORB_SIZE)
            randTexture = random.choice(orb_color_texture_paths)

            newOrb = Orb(randX, randY, randR, randTexture)
            self.orbs.append(newOrb)
        self.play()

    def play(self) -> None:
        while self.quit_game == False:
            self.update()
            self.render()

    def update(self) -> None:
        self.clock.tick(FPS)

        # Updating window events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game = True

        # Updating player events
        self.player.update()

        # Updating orb events
        for orb in self.orbs:
            if orb.update(self.player):
                self.orbs.remove(orb)
                randX = random.randint(0, self.window_dims[0])
                randY = random.randint(0, self.window_dims[1])
                randR = random.randint(MIN_ORB_SIZE, MAX_ORB_SIZE)
                randTexture = random.choice(orb_color_texture_paths)

                newOrb = Orb(randX, randY, randR, randTexture)
                self.orbs.append(newOrb)

    def render(self) -> None:
        self.window.fill(self.window_color)
        self.player.render(self.window)
        for orb in self.orbs:
            orb.render(self.window)
        pygame.display.update()
