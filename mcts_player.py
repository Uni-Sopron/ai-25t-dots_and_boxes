import math
import random

from abstract_player import AbstractPlayer
from dots_n_boxes import GameState, Direction

Move = tuple[int, int, Direction]


class MCTSPlayer(AbstractPlayer):
    def __init__(self, state: GameState, iterations=1_000) -> None:
        self.root = Node(state)
        self.iterations = iterations

    def get_move(self, state: GameState) -> Move:
        self.root = Node(state)
        # TODO search node of current state in existing tree
        #     instead of building a new tree:
        # self.root = self.find_node(state)
        for _ in range(self.iterations):
            node = self.root.select()
            if node.state.is_final():
                break
            child = node.expand()
            result_state = child.simulate()
            result = result_state.pts[1] - result_state.pts[0]
            winner = 1 if result > 0 else 0 if result < 0 else -1
            child.backpropagate(winner)

        def simulation_count(move) -> int:
            return self.root.children[move].total

        best_move = max(self.root.children, key=simulation_count)
        return best_move


class Node:
    C = math.sqrt(2)
    def __init__(self, state: GameState, parent: "Node | None" = None) -> None:
        self.state = state
        self.parent = parent
        self.children = dict[Move, Node]()  # move : node
        self.wins = 0.0
        self.total = 0

    def select(self) -> "Node":
        """Choose a node with a potential child to explore.

        At every node, continue with the children maximizing the formula:
        child.wins/child.total + c * math.sqrt(math.log(self.total) / child.total)
        """
        if self.state.is_final():
            return self
        
        if len(self.children)<len(self.state.valid_moves()):
            return self
        
        max_points = float("-inf")
        children = list(self.children.values())
        best_child = children[0]
        max_points = best_child.wins / best_child.total + self.C * math.sqrt(math.log(self.total) / best_child.total)
        
        for child in children[1:]:
            current_point = child.wins / child.total + self.C * math.sqrt(math.log(self.total) / child.total)
            if current_point > max_points:
                max_points = current_point
                best_child = child
        
        return best_child.select()
               

    def expand(self) -> "Node":
        """Expand the current node with a new child node."""
        pass

    def simulate(self) -> GameState:
        """Simulate the complete game from the current node with random moves."""
        pass

    def backpropagate(self, winner: int) -> None:
        """Update the node's and parents' wins and total counts.

        :param winner: index of winning player, or -1 if it's a tie
        """
        outcome = 0.5 if winner == -1 else 1.0
        node = self
        while node is not None:
            node.total += 1
            if node.state.next_player == winner:
                node.wins += outcome
            else:
                node.wins += 1.0 - outcome
            node = node.parent
