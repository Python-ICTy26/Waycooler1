import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            list_grid = [
                [random.choice([0, 1]) for _ in range(self.rows)] for _ in range(self.cols)
            ]
        else:
            list_grid = [[0 for _ in range(self.rows)] for _ in range(self.cols)]
        return list_grid

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        neighbours = []
        positions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for i in positions:
            row_pos, col_pos = row + i[0], col + i[1]
            if row_pos < 0 or row_pos >= self.rows or col_pos < 0 or col_pos >= self.cols:
                continue
            else:
                neighbours.append(self.curr_generation[row_pos][col_pos])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = []
        for i in range(self.rows):
            line = []
            for j in range(self.cols):
                if self.curr_generation[i][j] == 0:
                    if sum(self.get_neighbours((i, j))) == 3:
                        line.append(1)
                    else:
                        line.append(0)
                else:
                    if (
                        sum(self.get_neighbours((i, j))) == 2
                        or sum(self.get_neighbours((i, j))) == 3
                    ):
                        line.append(1)
                    else:
                        line.append(0)
            new_grid.append(line)
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1


    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations >= self.max_generations:
            return True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.curr_generation != self.prev_generation:
            return True
        else:
            return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        file = open(filename).readlines()
        grid_list = []
        for i in range(len(file)):
            x = list(map(int, file[i].split()))
            grid_list.append(x)
        life = GameOfLife(size=(len(grid_list), len(grid_list[0])), randomize=False)
        life.curr_generation = grid_list
        return life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as file:
            for i in self.curr_generation:
                file.write("".join([str(j) for j in i]) + "\n")
