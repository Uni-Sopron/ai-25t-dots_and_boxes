import math
import random

from abstract_player import AbstractPlayer
from dots_n_boxes import GameState, Direction


class MCTSPlayer(AbstractPlayer):
    def __init__(self, state: GameState, iterations=1_000) -> None:
        self.root = Node(state)
        self.iterations = iterations

    def get_move(self, state: GameState) -> tuple[int, int, Direction]:
        pass


class Node:
    def __init__(self, state: GameState, parent: "Node | None" = None) -> None:
        self.state = state
        self.parent = parent
        self.children = dict[tuple, Node]()  # move : node
        self.wins = 0.0
        self.total = 0
        self.c=math.sqrt(2)

    def select(self) -> "Node":
        """Choose a node with a potential child to explore.

        At every node, continue with the children maximizing the formula:
        child.wins/child.total + c * math.sqrt(math.log(self.total) / child.total)
        """
        if self.state.is_final():
            return self
        
        for move in self.state.valid_moves():
            if move not in self.children:
                return self
        
        max_points = "-inf"
        
        for move, child in self.children.items():
            current_point=child.wins/child.total + self.c * math.sqrt(math.log(self.total) / child.total)
            if current_point>max_points:
                max_points=current_point
               
        for node, point in self.children.items():
            if point==max_points:
                return node.select()

    def expand(self) -> "Node":
        """Expand the current node with a new child node."""
        pass

    def simulate(self) -> GameState:
        """Simulate the complete game from the current node with random moves."""
        pass

    def backpropagate(self, result: float) -> None:
        """Update the node's and parents' wins and total counts."""
        pass
