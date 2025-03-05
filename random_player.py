from abstract_player import AbstractPlayer
from dots_n_boxes import GameState, Direction
import random


class RandomPlayer(AbstractPlayer):
    def get_move(self, state: GameState) -> tuple[int, int, Direction]:
        moves = state.valid_moves()
        return random.choice(moves)
