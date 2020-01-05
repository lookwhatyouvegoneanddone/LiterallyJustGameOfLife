import pygame
import multiprocessing as mp

class GamePiece:
    alive = False
    width = 10
    height = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface):
        gray = (100, 100, 180)
        black = (0, 0, 0)
        if self.alive:
            colour = gray
        else:
            colour = black
        pygame.draw.rect(surface, colour, (self.x, self.y, self.width, self.height))


class GameHandler:

    def __init__(self, pieces):
        self.pieces = pieces

    def apply_rules_mp(self, num_threads):
        pool = mp.Pool(processes=num_threads)
        results = []
        for num_row in range(len(self.pieces)):
            for num_col in range(len(self.pieces[num_row])):
                asynced = pool.apply_async(self.check_cell, args = (num_row, num_col))
                for item in asynced.get():
                    results.append(item)
                print(results)

    def check_cell(self, num_row, num_col):
        """
        Returns an int with the number of 'alive' neighbors the cell at (num_row, num_col) has
        """
        neighbors_alive = 0

        """
        Checks 3 pieces above
        """

        if num_row > 0:  # Check that you're not in the first row
            if num_col > 0:  # Check that you're not in the first col
                if self.pieces[num_row - 1][num_col - 1].alive:  # Checks top left
                    neighbors_alive += 1
            if self.pieces[num_row - 1][num_col].alive:  # Checks top middle
                neighbors_alive += 1
            if num_col < len(self.pieces[0]) - 1:
                if self.pieces[num_row - 1][num_col + 1].alive:  # Checks top right
                    neighbors_alive += 1

        """
        Checks 2 in same row
        """

        if num_col > 0:
            if self.pieces[num_row][num_col - 1].alive:  # Checks middle left
                neighbors_alive += 1
        if num_col < len(self.pieces[num_row]) - 1:
            if self.pieces[num_row][num_col + 1].alive:  # Checks middle right
                neighbors_alive += 1

        """
        Checks 3 pieces below
        """

        if num_row < len(self.pieces) - 1:  # Check that you're not in the last row
            if num_col > 0:  # Check that you're not in the first col
                if self.pieces[num_row + 1][num_col - 1].alive:  # Checks bottom left
                    neighbors_alive += 1
            if self.pieces[num_row + 1][num_col].alive:  # Checks bottom middle
                neighbors_alive += 1
            if num_col < len(self.pieces[0]) - 1:
                if self.pieces[num_row + 1][num_col + 1].alive:  # Checks bottom right
                    neighbors_alive += 1

        if self.pieces[num_row][num_col].alive:
            if not (neighbors_alive == 2 or neighbors_alive == 3):
                # print(f"Killed cell at [{num_row}, {num_col}] with {neighbors_alive} neighbors")
                return [False, num_row, num_col]
        else:
            if neighbors_alive == 3:
                # print(f"Gave life to cell at [{num_row}, {num_col}] with {neighbors_alive} neighbors")
                return [True, num_row, num_col]

    def play_god(self, alive_list, dead_list):
        for cell in alive_list:
            row, col = cell
            self.pieces[row][col].alive = True

        for cell in dead_list:
            row, col = cell
            self.pieces[row][col].alive = False









