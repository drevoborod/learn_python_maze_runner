from typing import Protocol


type Point = tuple[int, int]


class Maze(Protocol):
    def generate(self) -> tuple[list[Point], list[Point], int, int]:
        pass


class RandomMaze(Maze):
    def __init__(self, wall_width: int, wall_height: int):
        self.wall_width = wall_width
        self.wall_height = wall_height

    def generate(self) -> tuple[list[Point], list[Point], int, int]:
        raise NotImplementedError


class ConfiguredMaze(Maze):
    def __init__(self, filename: str):
        self.file = open(filename, "r")

    def generate(self) -> tuple[list[Point], list[Point], int, int]:
        raise NotImplementedError


class FixedMaze(Maze):
    def __init__(self, wall_width: int, wall_height: int):
        self.wall_width = wall_width
        self.wall_height = wall_height

    def generate(self) -> tuple[list[Point], list[Point], int, int]:
        matrix = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
        maze_coords = []
        empty_coords = []
        for row_num, row in enumerate(matrix):
            for col_num, col in enumerate(row):
                coords = (col_num * self.wall_width, row_num * self.wall_height)
                if col == 1:
                    maze_coords.append(coords)
                else:
                    empty_coords.append(coords)
        return maze_coords, empty_coords, len(matrix[0]), len(matrix)
