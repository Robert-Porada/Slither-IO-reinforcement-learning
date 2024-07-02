import pygame



class Object:
    def __init__(self, x, y, w, h, texture_path) -> None:
        self.object_hitbox = pygame.Rect(x, y, w, h)
        image = pygame.image.load(texture_path)
        self.texture = pygame.transform.scale(image, (w, h))
    
    def render(self, window: object, camera: object) -> None:
        window.blit(self.texture, camera.translate(self.object_hitbox.x, self.object_hitbox.y))