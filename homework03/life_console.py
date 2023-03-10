import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for x in range(self.life.rows):
            for y in range(self.life.cols):
                if self.life.curr_generation[x][y] == 1:
                    screen.addch(x + 1, y + 1, "#")
                else:
                    screen.addch(x + 1, y + 1, " ")

    def run(self) -> None:
        screen = curses.initscr()
        # PUT YOUR CODE HERE
        while True:
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            self.life.step()
            if screen.getch() == 32:  # space
                curses.endwin()
                break


if __name__ == "__main__":
    life = GameOfLife((24, 80), max_generations=50)
    ui = Console(life)
    ui.run()
