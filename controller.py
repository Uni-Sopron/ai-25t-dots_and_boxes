from dots_n_boxes import GameState
from abstract_player import AbstractPlayer


class Controller:
    def __init__(self, player1: AbstractPlayer, player2: AbstractPlayer, game: GameState) -> None:
        self.players = player1, player2
        self.game = game

    def play(self) -> tuple[int, int]:
        while not self.game.is_final():
            move = self.players[self.game.next_player].get_move(self.game)
            if move not in self.game.valid_moves():
                raise ValueError("Invalid move")
            self.game = self.game.move(*move)
        return self.game.pts[0], self.game.pts[1]
