import timeit

class Sudoku:
    def __init__(self):
        self.grid = get_grid()
        self.solved = False
        # performs validity check before solving to save time on illegal grid
        self.valid = self.is_valid()

    def __str__(self):
        grid_string = ''
        for i in range(len(self.grid)):
            line_string = ''
            if i % 3 == 0 and i != 0:
                line_string += "----------------------\n"

            for j in range(len(self.grid[i])):
                if j % 3 == 0 and j != 0:
                    line_string += "| "
                line_string += str(self.grid[i][j]) + ' '
            grid_string += line_string + '\n'
        return grid_string

    def is_valid(self):
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] != 0:
                    for k in range(9):
                        if k != row:
                            if self.grid[k][col] == self.grid[row][col]:
                                return False
                        if k != col:
                            if self.grid[row][k] == self.grid[row][col]:
                                return False
                        if k % 3 != row % 3 and k % 3 != col % 3:
                            if self.grid[(row // 3) * 3 + (k // 3)][(col // 3) * 3 + (k % 3)] == self.grid[row][col]:
                                return False
        return True

    def get_possible_vals(self, row, col):
        possible_bool = [True]*10
        for i in range(9):
            if i != row:
                possible_bool[self.grid[i][col]] = False
            if i != col:
                possible_bool[self.grid[row][i]] = False
            if i % 3 != row % 3 or i % 3 != col % 3:
                    possible_bool[self.grid[(row//3)*3+(i//3)][(col//3)*3+(i % 3)]] = False
            
        possible_bool[0] = False

        possible_vals = [i for i, x in enumerate(possible_bool) if x]
        return possible_vals

    def recursive_solve(self, row=0, col=0):
        if not self.valid:
            return
        if row == 9 and col == 0:
            self.solved = True
            return

        next_row, next_col = (row + 1, 0) if col % 8 == 0 and col != 0 else (row, col + 1)

        if self.grid[row][col] == 0:
            possible_vals = self.get_possible_vals(row, col)
            for i in range(len(possible_vals)):
                self.grid[row][col] = possible_vals[i]
                self.recursive_solve(next_row, next_col)
                if self.solved:
                    return
            self.grid[row][col] = 0
        else:
            self.recursive_solve(next_row, next_col)
            return

def get_grid():
    grid = []
    grid_string = input("Enter the sudoku string with spaces separating the lines: \n")
    grid_string = grid_string.split()
    for i in range(9):
        grid.append([])
        for j in range(9):
            grid[i].append(int(grid_string[i][j]))
    return grid

if __name__ == "__main__":
    current_sudoku = Sudoku()

    start = timeit.default_timer()
    current_sudoku.recursive_solve()
    taken = timeit.default_timer() - start

    print(current_sudoku)
    if current_sudoku.solved:
        print("Solution found in " + str(round(taken, 4)) + " seconds")
    else:
        print("No solution possible!!")
