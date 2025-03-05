from abstract_player import AbstractPlayer
from dots_n_boxes import GameState, Direction


class HumanPlayer(AbstractPlayer):
    def get_move(self, state: GameState) -> tuple[int, int, Direction]:
        print(state)
        print(f"Player 0: {state.pts[0]} points")
        print(f"Player 1: {state.pts[1]} points")
        print(f"Player {state.next_player}'s turn")
        row = int(input("Row: "))
        col = int(input("Col: "))
        dir_str = ""
        while dir_str not in "urdl" or len(dir_str) != 1:
            dir_str = input("Dir (u/r/d/l): ")
        if dir_str == "u":
            dir_ = Direction.UP
        elif dir_str == "r":
            dir_ = Direction.RIGHT
        elif dir_str == "d":
            dir_ = Direction.DOWN
        elif dir_str == "l":
            dir_ = Direction.LEFT
        move = row, col, dir_
        if move not in state.valid_moves():
            print("Invalid move, try again!")
            return self.get_move(state)
        return move
