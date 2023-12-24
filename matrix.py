import numpy as np

class Position():
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def clone(self, x: int = None, y: int = None) -> "Position":
        return Position(x=x if x is not None else self.x, y=y if y is not None else self.y)
    
    def __str__(self) -> str:
        return f"{self.y},{self.x}"
    
    def __eq__(self, other: object) -> bool:
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))

def string_matrix_from_lines(lines: list) -> np.ndarray:
    m = [[char for char in l] for l in lines]
    return np.matrix(data=m, dtype=str)

def neighbours(matrix: np.ndarray, x: int, y: int) -> list: 
    y_limit, x_limit = [d - 1 for d in matrix.shape]
    neighbours = []
    rows = range(max(0, y - 1), min(y_limit, y + 1) + 1)
    for row in rows:
        columns = range(max(0, x - 1), min(x_limit, x + 1) + 1)
        for col in columns:
            if col == x and row == y: 
                continue
            neighbours.append(matrix.item(row, col))
    return neighbours

def neighbours_positions(matrix: np.ndarray, x: int, y: int) -> list[tuple[Position]]: 
    y_limit, x_limit = [d - 1 for d in matrix.shape]
    neighbours = []
    rows = range(max(0, y - 1), min(y_limit, y + 1) + 1)
    for row in rows:
        columns = range(max(0, x - 1), min(x_limit, x + 1) + 1)
        for col in columns:
            if col == x and row == y: 
                continue
            neighbours.append(Position(y=row, x=col))
    return neighbours

def column(array:list, column:int) -> list:
    return [array[row][column] for row in range(0, len(array))]

def in_grid(grid:list, pos:Position) -> bool:
    n_rows, n_cols = dimensions(grid)
    return pos.x >= 0 and pos.x < n_cols and pos.y >= 0 and pos.y < n_rows

def dimensions(grid:list) -> tuple:
    return (len(grid), len(grid[0]))
