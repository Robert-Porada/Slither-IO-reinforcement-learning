import pygame


class FontRenderer:
    def __init__(self) -> None:
        self.color = (0, 255, 0)
        self.size = 40
        self.font = pygame.font.Font(None, self.size)

    def render_font(self, window, score):
        text = self.font.render(f"Score: {score}", True, self.color)
        window.blit(text, (10, 10))
