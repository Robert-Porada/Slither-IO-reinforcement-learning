import pygame


class MainGame:
    def __init__(self):
        self.window_dims = (1024, 768)
        self.window_color = (150, 150, 150)
        self.window = pygame.display.set_mode(self.window_dims)
        self.quit_game = False

    def play(self):
        while self.quit_game == False:
            self.update()
            self.render()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game = True

    def render(self):
        self.window.fill(self.window_color)

        pygame.display.update()
