from copy import deepcopy
from enum import Enum


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class GameState:
    def __init__(self, height: int, width: int, frame = True, track_boxes = True) -> None:
        self.height = height
        self.width = width
        self.next_player = 0
        self.pts = [0, 0]
        self.walls = [0] * ((2 * height + 1) * (width + 1))
        if frame:
            for col in range(width):
                self._set_wall(0, col, Direction.UP)
                self._set_wall(height - 1, col, Direction.DOWN)
            for row in range(height):
                self._set_wall(row, 0, Direction.LEFT)
                self._set_wall(row, width - 1, Direction.RIGHT)
        self.track_boxes = track_boxes
        if track_boxes:
            self.boxes = [[], []]

    def copy(self) -> "GameState":
        return deepcopy(self)

    def valid_moves(self) -> list:
        moves = []
        for row in range(self.height):
            for col in range(self.width):
                if self._is_boxed(row, col):
                    continue
                for dir_ in Direction:
                    if not self._get_wall(row, col, dir_):
                        moves.append((row, col, dir_))
        return moves

    def move(self, row: int, col: int, dir_: Direction) -> "GameState":
        game = self.copy()
        pts = game._set_wall(row, col, dir_)
        if pts:
            game.pts[game.next_player] += pts
            if game.track_boxes:
                all_boxes = sum(game.boxes, [])
                for i in range(game.height):
                    for j in range(game.width):
                        if game._is_boxed(i, j) and (i, j) not in all_boxes:
                            game.boxes[game.next_player].append((i, j))
        else:
            game.next_player ^= 1
        return game

    def is_final(self) -> bool:
        n = self.height * self.width
        return sum(self.pts) == n or max(self.pts) > n // 2

    def __str__(self) -> str:
        top = "+".join(
            " -"[self._get_wall(0, col, Direction.UP)] for col in range(self.width)
        )
        top = "+" + top + "+"
        lines = [top]
        for row in range(self.height):
            line = " |"[self._get_wall(row, 0, Direction.LEFT)] + " "
            line += " ".join(
                " |"[self._get_wall(row, col, Direction.RIGHT)]
                for col in range(self.width)
            )
            lines.append(line)
            line = "+".join(
                " -"[self._get_wall(row, col, Direction.DOWN)]
                for col in range(self.width)
            )
            line = "+" + line + "+"
            lines.append(line)
        if self.track_boxes:
            for i, boxes in enumerate(self.boxes):
                for row, col in boxes:
                    line = lines[2 * row + 1]
                    prefix = line[:2 * col + 1]
                    suffix = line[2 * col + 2:]
                    lines[2 * row + 1] = prefix + str(i) + suffix
        for i, line in enumerate(lines):
            if i % 2 == 1:
                lines[i] = f"{i // 2:2} " + line
            else:
                lines[i] = "   " + line
        lines.insert(0, "    " + " ".join(f"{i:2}"[1] for i in range(self.width)))
        if self.width > 9:
            lines.insert(0, "    " + " ".join(f"{i:2}"[0] for i in range(self.width)))
        return "\n".join(lines)

    def _wall_index(self, row: int, col: int, dir_: Direction) -> int:
        i = 1 + 2 * row
        j = 1 + col + (dir_ == Direction.RIGHT)
        if dir_ == Direction.UP:
            i -= 1
        elif dir_ == Direction.DOWN:
            i += 1
        return i * (self.width + 1) + j

    def _get_wall(self, row: int, col: int, dir_: Direction) -> int:
        return self.walls[self._wall_index(row, col, dir_)]

    def _is_boxed(self, row: int, col: int) -> bool:
        return all(self._get_wall(row, col, dir_) for dir_ in Direction)

    def _set_wall(self, row: int, col: int, dir_: Direction, wall: int = 1) -> int:
        w = self._wall_index(row, col, dir_)
        if self.walls[w] == wall:
            raise ValueError("Wall already set")
        self.walls[w] = wall
        pts = int(self._is_boxed(row, col))
        if dir_ == Direction.UP and row > 0:
            pts += self._is_boxed(row - 1, col)
        elif dir_ == Direction.DOWN and row < self.height - 1:
            pts += self._is_boxed(row + 1, col)
        elif dir_ == Direction.LEFT and col > 0:
            pts += self._is_boxed(row, col - 1)
        elif dir_ == Direction.RIGHT and col < self.width - 1:
            pts += self._is_boxed(row, col + 1)
        return pts
