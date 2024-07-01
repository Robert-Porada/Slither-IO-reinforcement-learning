import pygame

class Orb:
    def __init__(self, x: int, y: int, r: int, texture_path) -> None:
        self.x = x
        self.y = y
        self.r = r
        self.player_hitbox = pygame.Rect(self.x, self.y, self.r, self.r)
        image = pygame.image.load(texture_path)
        self.texture = pygame.transform.scale(image, (self.r, self.r))

    def update(self, player) -> bool:
        if self.player_hitbox.colliderect(player.player_hitbox):
            player.score += self.r
            return True
        return False

    def render(self, window: object) -> None:
        window.blit(self.texture, (self.player_hitbox.x, self.player_hitbox.y))