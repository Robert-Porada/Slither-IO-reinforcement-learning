import torch
import random
import numpy as np
from collections import deque
from main_game import MainGame
from model import Linear_Qnet, QTrainer
from plot_helper import plot

MAX_MEMORY = 1_000_000
BATCH_SIZE = 128

LR = 0.001

ACTION = [0, 0, 0, 0]


class Agent:
    def __init__(self) -> None:
        self.number_of_games = 0
        self.epsilon = 0
        self.gamma = 0.99  # Discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_Qnet(9, 256, 4)
        self.trainer = QTrainer(self.model, LR, self.gamma)

    def get_state(self, game):
        state = []
        # Player movement angle normalized
        movement_angle_raw = game.player.movement_angle
        movement_angle_norm = movement_angle_raw / 2 * np.pi
        state.append(movement_angle_norm)

        # X and Y positions of the closest orb [2 values]
        closest_orb_pos = game.player.closest_orb_pos
        if closest_orb_pos:
            closest_orb_1_x = closest_orb_pos[0]
            closest_orb_1_y = closest_orb_pos[1]
            state.append(closest_orb_1_x)
            state.append(closest_orb_1_y)
        else:
            state.append(0)
            state.append(0)

        # X and Y positions of closest enemy segment [2 values]
        closest_enemy_segments_pos = game.player.closest_enemy_segments_pos
        if closest_enemy_segments_pos:
            closest_enemy_segment_1_x = closest_enemy_segments_pos[0]
            closest_enemy_segment_1_y = closest_enemy_segments_pos[1]
            state.append(closest_enemy_segment_1_x)
            state.append(closest_enemy_segment_1_y)
        else:
            state.append(0)
            state.append(0)

        # Player - wall distance for all the walls [4 values]
        player_wall_distance = game.player.distance_from_walls
        if player_wall_distance:
            top_wall_distance = player_wall_distance[0]
            right_wall_distance = player_wall_distance[1]
            left_wall_distance = player_wall_distance[2]
            bottom_wall_distance = player_wall_distance[3]
            state.append(top_wall_distance)
            state.append(right_wall_distance)
            state.append(left_wall_distance)
            state.append(bottom_wall_distance)
        else:
            state.append(0)
            state.append(0)
            state.append(0)
            state.append(0)

        return np.array(state, dtype=float)

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        # Exploration exploitations tradeoff
        self.epsilon = 500 - self.number_of_games
        final_move = [0, 0, 0, 0]
        if random.randint(0, 700) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
            final_move[3] = random.randint(0, 1)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction[:3]).item()
            final_move[move] = 1
            if prediction[3] > 0.5:
                final_move[3] = 1

        return final_move

    def get_action_from_model_only(self, state, model):
        final_move = [0, 0, 0, 0]
        state0 = torch.tensor(state, dtype=torch.float)
        prediction = self.model(state0)
        move = torch.argmax(prediction[:3]).item()
        final_move[move] = 1
        if prediction[3] > 0.5:
            final_move[3] = 1
        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = MainGame()
    game.initialize()

    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move based on state
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, game_over, score = game.play(final_move)

        state_new = agent.get_state(game)
        #
        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)
        #
        # rememver
        agent.remember(state_old, final_move, reward, state_new, game_over)
        #
        if game_over:
            # train the long memory, plot the result
            game.initialize()
            agent.number_of_games += 1
            agent.train_long_memory()
            #
            if score > record:
                record = score
                agent.model.save()
            print("Game", agent.number_of_games, "Score", score, "Record:", record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.number_of_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


def play(model_path):
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    model = Linear_Qnet(9, 256, 4)
    model.load(model_path)
    agent = Agent()
    game = MainGame()
    game.initialize()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move based on state
        final_move = agent.get_action_from_model_only(state_old, model)

        # perform move and get new state
        reward, game_over, score = game.play(final_move)

        if game_over:
            # train the long memory, plot the result
            game.initialize()
            agent.number_of_games += 1
            if score > record:
                record = score
            print("Game", agent.number_of_games, "Score", score, "Record:", record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.number_of_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == "__main__":
    # train()
    play(model_path="model/model_9_256_256_4.pth")
