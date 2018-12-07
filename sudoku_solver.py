
grid = [[0, 9, 0, 0, 0, 4, 5, 0, 0],
        [7, 4, 0, 0, 0, 0, 8, 6, 0],
        [0, 0, 0, 5, 3, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 9, 0, 4, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 2],
        [4, 5, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 8, 0, 0, 0],
        [0, 2, 3, 0, 0, 0, 0, 8, 5],
        [0, 0, 1, 4, 0, 0, 0, 3, 0]]

# keeps track of possible numbers for each cell
options = [[set(range(1,10)) if i==0 else set() for i in row] for row in grid]


def square(row, col):
    # generates indeces of the 9 cells in a square
    for i in range(9):
        r = 3 * (row // 3) + (i // 3)
        c = 3 * (col // 3) + (i % 3)
        yield (r, c)

def solve_state():
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                # "write down" all possible options for the current cell
                row = [grid[i][k] for k in range(9)]
                col = [grid[k][j] for k in range(9)]
                sqr = [grid[r][c] for r, c in square(i, j)]
                opts = options[i][j]
                opts.difference_update(row, col, sqr)
                # if there's only one legal number, fill this cell with it
                if len(opts) == 1:
                    grid[i][j] = opts.pop()
                else:
                    # check if any of the options for this cell is unique in its row, column or square
                    row_opts = set.union(*[options[i][k] for k in range(9) if k != j])
                    col_opts = set.union(*[options[k][j] for k in range(9) if k != i])
                    sqr_opts = set.union(*[options[r][c] for r, c in square(i, j) if (r,c) != (i,j)])
                    unique_in_row = opts.difference(row_opts)
                    unique_in_col = opts.difference(col_opts)
                    unique_in_sqr = opts.difference(sqr_opts)
                    # if one of the options in this cell is unique, fill the cell with it
                    if len(unique_in_row) == 1:
                        grid[i][j] = unique_in_row.pop()
                        options[i][j] = set()
                    elif len(unique_in_col) == 1:
                        grid[i][j] = unique_in_col.pop()
                        options[i][j] = set()
                    elif len(unique_in_sqr) == 1:
                        grid[i][j] = unique_in_sqr.pop()
                        options[i][j] = set()
            elif len(options[i][j]) > 0:
                # a cell that is already filled shouldn't have any more options
                options[i][j] = set()

def finished():
    for row in grid:
        for cell in row:
            if cell == 0:
                return False
    return True

def print_grid():
    row_sep = "+-----"*3 + "+"
    for i, row in enumerate(grid):
        if i%3 == 0:
            print(row_sep)
        row_str = "|".join([" ".join(map(str,row[j:j+3])) for j in (0,3,6)])
        print("|"+row_str+"|")
    print(row_sep)


count = 0   # keeps track of number of iterations
while not finished():
    prev_state = [[i for i in row] for row in grid] # to detect unsolvable grids
    solve_state()
    count += 1
    # check if the state of the grid has changed
    changed = False
    for i in range(9):
        for j in range(9):
            if grid[i][j] != prev_state[i][j]:
                changed = True
    # if no new cells were found, the grid is unsolvable
    if not changed:
        break
print_grid()
print(count)
        
