import timeit


class Square:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Sudoku:
    def __init__(self):
        self.grid = self.get_grid()
        self.solved = False
        self.solvable = self.is_solvable()

    def __str__(self):
        grid_string = ''
        for i in range(len(self.grid)):
            line_string = ''
            if i % 3 == 0 and i != 0:
                line_string += "----------------------\n"

            for j in range(len(self.grid[i])):
                if j % 3 == 0 and j != 0:
                    line_string += "| "
                line_string += str(self.grid[i][j].value) + ' '
            grid_string += line_string + '\n'
        return grid_string

    def get_grid(self):
        grid = []
        grid_string = input("Enter the sudoku string with spaces separating the lines: \n")
        grid_string = grid_string.split()
        for i in range(9):
            grid.append([])
            for j in range(9):
                grid[i].append(Square(int(grid_string[i][j])))
        return grid

    def is_solvable(self):
        for i in range(9):
            row = i
            for j in range(9):
                col = j
                if self.grid[i][j].value != 0:
                    for k in range(9):
                        if k != row:
                            if self.grid[k][col].value == self.grid[row][col].value:
                                return False
                        if k != col:
                            if self.grid[row][k].value == self.grid[row][col].value:
                                return False
                        if k % 3 != row % 3 and k % 3 != col % 3:
                            if self.grid[(row // 3) * 3 + (k // 3)][(col // 3) * 3 + (k % 3)].value == self.grid[row][col].value:
                                return False
        return True

    def get_possible_vals(self, row, col):
        possible_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(9):
            if i != row:
                if self.grid[i][col].value in possible_vals:
                    possible_vals.remove(self.grid[i][col].value)
            if i != col:
                if self.grid[row][i].value in possible_vals:
                    possible_vals.remove(self.grid[row][i].value)
            if i % 3 != row % 3 or i % 3 != col % 3:
                if self.grid[(row//3)*3+(i//3)][(col//3)*3+(i % 3)].value in possible_vals:
                    possible_vals.remove(self.grid[(row//3)*3+(i//3)][(col//3)*3+(i % 3)].value)
        return possible_vals

    def get_next_pos(self, row, col):
        if col % 8 == 0 and col != 0:
            next_row = row + 1
            next_col = 0
        else:
            next_row = row
            next_col = col + 1
        return next_row, next_col

    def recursive_solve_sudoku(self, row=0, col=0):
        if not self.solvable:
            return
        if row == 9 and col == 0:
            self.solved = True
            return

        next_row, next_col = self.get_next_pos(row, col)

        if self.grid[row][col].value == 0:
            possible_vals = self.get_possible_vals(row, col)
            for i in range(len(possible_vals)):
                self.grid[row][col].value = possible_vals[i]
                self.recursive_solve_sudoku(next_row, next_col)
                if self.solved:
                    return
            self.grid[row][col].value = 0
        else:
            self.recursive_solve_sudoku(next_row, next_col)
            return


if __name__ == "__main__":
    current_sudoku = Sudoku()
    start = timeit.default_timer()
    current_sudoku.recursive_solve_sudoku()
    taken = timeit.default_timer() - start
    print(current_sudoku)
    if current_sudoku.solved:
        print("Solution found in " + str(round(taken, 4)) + " seconds")
    elif not current_sudoku.solvable:
        print("No solution possible!!")
    else:
        print("No solution found!!")
