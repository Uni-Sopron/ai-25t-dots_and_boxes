from abc import ABC, abstractmethod

from dots_n_boxes import GameState, Direction


class AbstractPlayer(ABC):
    @abstractmethod
    def get_move(self, state: GameState) -> tuple[int, int, Direction]: ...
