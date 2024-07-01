import pygame


class Player:
    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        self.w = w
        self.h = h
        self.player_hitbox = pygame.Rect(x, y, w, h)
        image = pygame.image.load("resource/main_body.png")
        self.texture = pygame.transform.scale(image, (w, h))

        self.player_speed = 10
        self.boost_speed = 15
        self.score = 0

    def update(self) -> None:
        print(self.score)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.player_hitbox.x -= self.player_speed

        if keys[pygame.K_d]:
            self.player_hitbox.x += self.player_speed

        if keys[pygame.K_s]:
            self.player_hitbox.y += self.player_speed

        if keys[pygame.K_w]:
            self.player_hitbox.y -= self.player_speed

    def render(self, window: object, camera: object) -> None:
        window.blit(
            self.texture, camera.translate(self.player_hitbox.x, self.player_hitbox.y)
        )
