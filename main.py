from human_player import HumanPlayer
from random_player import RandomPlayer
from controller import Controller
from dots_n_boxes import GameState

if __name__ == "__main__":
    player1 = HumanPlayer()
    player2 = RandomPlayer()
    game = GameState(3, 4, frame=True, track_boxes=True)
    controller = Controller(player1, player2, game)
    result = controller.play()
    print(controller.game)
    print("Game over!")
    print(f"Player 0: {result[0]} points")
    print(f"Player 1: {result[1]} points")
