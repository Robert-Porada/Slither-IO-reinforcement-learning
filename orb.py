import pygame

class Orb:
    def __init__(self, x: int, y: int, r: int, texture_path) -> None:
        self.r = r
        self.orb_hitbox = pygame.Rect(x, y, r, r)
        image = pygame.image.load(texture_path)
        self.texture = pygame.transform.scale(image, (r, r))

    def update(self, player) -> bool:
        if self.orb_hitbox.colliderect(player.player_hitbox):
            player.score += self.r
            return True
        return False

    def render(self, window: object, camera: object) -> None:
        window.blit(self.texture, camera.translate(self.orb_hitbox.x, self.orb_hitbox.y))