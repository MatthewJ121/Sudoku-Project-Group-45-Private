# main file to run the sudoku game
import pygame
from sudoku_generator import SudokuGenerator, generate_sudoku

cell_size = 50  # only change this one to make the cells smaller/bigger
width = cell_size * 9
height = cell_size * 9 + cell_size


def tempGen():
    list = []
    for i in range(1, 82, 9):
        list2 = []
        while i % 9 != 0:
            list2.append(i)
            i += 1
        list2.append(i)
        list.append(list2)
    return list


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.isSelecteed = False

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        pass
        # if self.sketched_value > 0:


class Board:
    def __init__(self, width: int, screen, difficulty: str):
        match difficulty:
            case "easy":
                self.list = generate_sudoku(width, 30)
            case "medium":
                self.list = generate_sudoku(width, 40)
            case "hard":
                self.list = generate_sudoku(width, 50)
            case "zero":
                self.list = generate_sudoku(width, 0)
            case "temp":
                self.list = tempGen()
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty

        self.selected_cell = None
        self.original_board = [row[:] for row in self.list]

    def draw(self):  # ONLY DRAWS LINES RN
        for i in range(1, width // cell_size + 1):  # vertical
            if i % 3 == 0:
                pygame.draw.line(self.screen, "black", (cell_size * i, 0), (cell_size * i, height - cell_size), 3)
            else:
                pygame.draw.line(self.screen, "black", (cell_size * i, 0), (cell_size * i, height - cell_size))

        for i in range(1, (height - cell_size) // cell_size + 1):  # horizontal
            if i % 3 == 0:
                pygame.draw.line(self.screen, "black", (0, cell_size * i), (width, cell_size * i), 3)
            else:
                pygame.draw.line(self.screen, "black", (0, cell_size * i), (width, cell_size * i))

    def select(self, row, col):
        # Marks the cell at(row, col) in the board as the current selected cell. Once a cell has been selected, the user can edit its value or sketched value.
        self.selected_cell = (row,col)

    def click(self, x, y):
        # If a tuple of(x, y) coordinates is within the displayed board, this function returns a tuple of the(row, col) of the cell which was clicked. Otherwise, this function returns None.
        if 0 <= x < self.width and 0<= y < self.height - cell_size:
            return y//cell_size, x//cell_size
        return None

    def clear(self):
        # Clears the value cell. Note that the user can only remove the cell values and sketched values that are filled by themselves.
        if self.selected_cell:
            row, col = self.selected_cell
            if self.original_board[row][col] == 0:
                self.list[row][col] = 0

    def sketch(self, value):
        # Sets the sketched value of the current selected cell equal to the user entered value. It will be displayed at the top left corner of the cell using the draw() function.

        # NOTE FROM ELIN: not sure if this is correct because it wants the draw function called but i'm not sure how to integrate it
        #needs cell class written in order to complete
        if self.selected_cell:
            row, col = self.selected_cell
            if self.original_board[row][col] == 0:
                self.list[row][col] = value

    def place_number(self, value):
        #Sets the value of the current selected cell equal to the user entered value. Called when the user presses the Enter key.
        if self.selected_cell:
            row, col = self.selected_cell
            if self.original_board[row][col] == 0:
                self.list[row][col] = value
        #NOTE FROM ELIN: "called when user presses enter key" would that be here or under a different function for pressing enter??

    def reset_to_original(self):
        #Resets all cells in the board to their original values (0 if cleared, otherwise the corresponding digit).
        self.list = [row[:] for row in self.original_board]

    def is_full(self):
        #Returns a Boolean value indicating whether the board is full or not.
        return not any(0 in row for row in self.list)


    def update_board(self):
        #Updates the underlying 2D board with the values in all cells.
        pass

        #NOTE FROM ELIN: is this needed because it should already be updated with the functions above no?

    def find_empty(self):
        #Finds an empty cell and returns its row and col as a tuple(x, y).
        for row in range(len(self.list)):
            for col in range(len(self.list[row])):
                if self.list[row][col] == 0:
                    return row, col
        return None
        #as a tuple?...


    def check_board(self):
        #Check whether the Sudoku board is solved correctly.

        def is_solved(arr):
            return sorted([x for x in arr if x!=0]) == list(range(1,10))

        #check rows and cols
        for i in range(9):
            if not is_solved(self.list[i]) or not is_solved([self.list[x][i] for x in range(9)]):
                return False

        #check 3x3 grids
        for grid_row in range(0,9,3):
            for grid_col in range (0,9,3):
                grid = [
                    self.list[r][c]
                    for r in range(grid_row, grid_row+3)
                    for c in range(grid_col, grid_col+3)
                ]
                if not is_solved(grid):
                    return False

        return True

def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        board = Board(9, screen, "temp")  # temporary call, should be done through the main menu
        # cell definition goes here
        clock = pygame.time.Clock()
        currentCell = [0, 0]
        running = True
        while running:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        running = False
                    case pygame.MOUSEBUTTONDOWN:
                        clickX, clickY = event.pos
                        selected = board.click(clickX, clickY)
                        if selected:
                            currentCell = [selected[0], selected[1]]
                            board.select(selected[0], selected[1])

                        '''
                        clickX = list(event.pos)[0]
                        clickY = list(event.pos)[1]
                        cellRow = clickX // cell_size
                        cellCol = clickY // cell_size
                        currentCell = [cellRow, cellCol]
                        '''
                    # cell navigation using arrow keys, updates currentCell [intX, intY]
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_RIGHT:
                                if currentCell[0] < 8:
                                    currentCell[0] += 1
                            case pygame.K_LEFT:
                                if currentCell[0] > 0:
                                    currentCell[0] -= 1
                            case pygame.K_UP:
                                if currentCell[1] > 0:
                                    currentCell[1] -= 1
                            case pygame.K_DOWN:
                                if currentCell[1] < 8:
                                    currentCell[1] += 1
                            case pygame.K_f:
                                print(currentCell)
                    case _:
                        continue

            screen.fill("white")
            board.draw()
            pygame.display.flip()
            clock.tick(60)
        generate_sudoku(9, 0)
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
