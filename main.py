from main_game import MainGame

action = [1, 0, 0, 1]

if __name__ == "__main__":
    game = MainGame()
    game.initialize()
    game.play(action)
