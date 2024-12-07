# main file to run the sudoku game
import pygame,sys
from sudoku_generator import SudokuGenerator, generate_sudoku

cell_size = 60  # only change this one to make the cells smaller/bigger
width = cell_size * 9
height = cell_size * 9 + cell_size

LINE_COLOR = (255, 255, 255)

# UI functionality is below
def draw_game_start(screen):  # creates the game start screen
    # title font
    start_title_font = pygame.font.Font(None, 100)
    game_mode_font = pygame.font.Font(None, 75)
    button_font = pygame.font.Font(None, 50)

    # background color
    screen.fill("lightblue")

    # title
    title_surface = start_title_font.render("Sudoku!", 0, ("black"))
    title_rectangle = title_surface.get_rect(center=(width // 2, height // 2 - 100))
    screen.blit(title_surface, title_rectangle)

    # game modes
    game_mode_surface = game_mode_font.render("Select Game Mode:", 0, ("black"))
    game_mode_rectangle = game_mode_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(game_mode_surface, game_mode_rectangle)

    # buttons and text
    easy_text = button_font.render("Easy", 0, ("black"))
    medium_text = button_font.render("Medium", 0, ("black"))
    hard_text = button_font.render("Hard", 0, ("black"))

    # text and button background color
    easy_surface = pygame.Surface((easy_text.get_size()[0] + 20, easy_text.get_size()[1] + 20))
    easy_surface.fill(LINE_COLOR)
    easy_surface.blit(easy_text, (10, 10))
    medium_surface = pygame.Surface((medium_text.get_size()[0] + 20, medium_text.get_size()[1] + 20))
    medium_surface.fill(LINE_COLOR)
    medium_surface.blit(medium_text, (10, 10))
    hard_surface = pygame.Surface((hard_text.get_size()[0] + 20, hard_text.get_size()[1] + 20))
    hard_surface.fill(LINE_COLOR)
    hard_surface.blit(hard_text, (10, 10))

    # button rectangle
    easy_rectangle = easy_surface.get_rect(center=(width // 2 - 200, height // 2 + 100))
    medium_rectangle = medium_surface.get_rect(center=(width // 2, height // 2 + 100))
    hard_rectangle = hard_surface.get_rect(center=(width // 2 + 200, height // 2 + 100))

    # buttons
    screen.blit(easy_surface, easy_rectangle)
    screen.blit(medium_surface, medium_rectangle)
    screen.blit(hard_surface, hard_rectangle)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rectangle.collidepoint(event.pos):
                    # checks if mouse on easy button
                    return "easy"  # returns to main if the mouse on start button
                elif medium_rectangle.collidepoint(event.pos):
                    # returns to main if the mouse on medium button
                    return "medium"
                elif hard_rectangle.collidepoint(event.pos):
                    return "hard"
        pygame.display.update()

def draw_ingame_options(screen): #creates buttons and text and colors for in game options
    button_font = pygame.font.Font(None, 50)
    reset_text = button_font.render("Reset", 0, (255, 255, 255))
    restart_text = button_font.render("Restart", 0, (255, 255, 255))
    exit_text = button_font.render("Exit", 0, (255, 255, 255))

    reset_surface = pygame.Surface((reset_text.get_size()[0] + 20, reset_text.get_size()[1] + 20))
    reset_surface.fill(LINE_COLOR)
    reset_surface.blit(reset_text, (10, 10))
    restart_surface = pygame.Surface((restart_text.get_size()[0] + 20, restart_text.get_size()[1] + 20))
    restart_surface.fill(LINE_COLOR)
    restart_surface.blit(restart_text, (10, 10))
    exit_surface = pygame.Surface((exit_text.get_size()[0] + 20, exit_text.get_size()[1] + 20))
    exit_surface.fill(LINE_COLOR)
    exit_surface.blit(exit_text, (10, 10))

    reset_rectangle = reset_surface.get_rect(center=(width // 2 - 200, height - 25))
    restart_rectangle = restart_surface.get_rect(center=(width // 2, height - 25))
    exit_rectangle = exit_surface.get_rect(center=(width // 2 + 200, height - 25))

    # buttons
    screen.blit(reset_surface, reset_rectangle)
    screen.blit(restart_surface, restart_rectangle)
    screen.blit(exit_surface, exit_rectangle)

    return reset_rectangle, restart_rectangle, exit_rectangle

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
        self.isSelected = False
        self.sketched_value = 0

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value
        self.set_cell_value(0) #so the draw function knows to sketch, not place
        
    def get_sketched_value(self):
        return self.sketched_value
    
    def get_cell_value(self):
        return self.cell_value

    def draw(self):
        #draw cell
        cell = pygame.Rect(self.col * cell_size, self.row * cell_size, cell_size, cell_size)
        #highlight
        if self.isSelected:
            pygame.draw.rect(self.screen, "yellow", cell)
        if self.value != 0: #draw value if cell is uneditted and ungenerated
            font = pygame.font.Font(None, cell_size//2)
            text = font.render(str(self.value), True, "black")
            self.screen.blit(
                text,
                (self.col*cell_size+cell_size/3, self.row*cell_size+cell_size/3)
            )
        #draw sketch if no value given
        elif self.sketched_value != 0:
            font = pygame.font.Font(None, cell_size-(cell_size//2))
            text = font.render(str(self.sketched_value), True, "light grey")
            self.screen.blit(
                text,
                (self.col*cell_size+cell_size/4, self.row*cell_size+cell_size/4)
            )
            
        pygame.draw.rect(self.screen, "black", cell, 1)

class Board:
    def __init__(self, width: int, screen, difficulty: str):
        difficulty_map = {
            "easy": 30,
            "medium": 40,
            "hard": 50,
        }
        empty_cells = difficulty_map.get(difficulty, 30)

        self.list = tempGen()
        #TEMPORRARY
        self.list[0][1] = 0
        self.list[0][8] = 0
        self.list[5][5] = 0

        self.original_board = self.list
        self.width = width
        self.height = height
        self.screen = screen
        self.currentPos = [0,0]

        self.cells = [[Cell(self.list[row][col], row, col, self.screen) #constructor
                       for col in range(len(self.list[0]))] #for every col, 
                       for row in range(len(self.list))] #for every row
        self.selected_cell = self.cells[0][0]

    def draw(self):
        # Draw all cells with their numbers
        for row in range(len(self.list)):
            for col in range(len(self.list[0])):
                self.cells[row][col].draw()

        # Draw grid lines (thicker for 3x3 blocks)
        for i in range(1, 10):
            line_thickness = cell_size//12 if i % 3 == 0 else cell_size//30 #dynamic line thickness 
            line_color = "black" if i%3 == 0 else "grey30"

            # Vertical lines
            pygame.draw.line(
                self.screen, line_color, (i * cell_size, 0), (i * cell_size, height - cell_size), line_thickness
            )
            # Horizontal lines
            pygame.draw.line(
                self.screen, line_color, (0, i * cell_size), (width, i * cell_size), line_thickness
            )

    def select(self, row, col):
        # Marks the cell at(row, col) in the board as the current selected cell. Once a cell has been selected, the user can edit its value or sketched value.
        '''if self.selected_cell:
            previous_row = self.selected_cell[0] 
            previous_col = self.selected_cell[1]'''
        self.selected_cell.isSelected = False

        self.selected_cell = self.cells[row][col]
        print(f"attemted to select {row},{col}")
        self.currentPos = [row,col]
        self.selected_cell.isSelected = True

    def click(self, x, y):
        # If a tuple of(x, y) coordinates is within the displayed board, this function returns a tuple of the(row, col) of the cell which was clicked. Otherwise, this function returns None.
        if 0 <= x < self.width and 0<= y < self.height - cell_size:
            return y//cell_size, x//cell_size
        return None

    def clear(self): #TODO
        # Clears the value cell. Note that the user can only remove the cell values and sketched values that are filled by themselves.
        if self.selected_cell:
            row, col = self.selected_cell
            if self.original_board[row][col] == 0:
                self.list[row][col].set_cell_value(0)

    def sketch(self, value):
        # Sets the sketched value of the current selected cell equal to the user entered value. It will be displayed at the top left corner of the cell using the draw() function.

        # NOTE FROM ELIN: not sure if this is correct because it wants the draw function called but i'm not sure how to integrate it
        #needs cell class written in order to complete
        print(f"called sketch, orginal board at pos is {self.original_board[self.currentPos[0]][self.currentPos[1]]}, currentPos: {self.currentPos}")
        if self.original_board[self.currentPos[0]][self.currentPos[1]] == 0:
            self.selected_cell.set_sketched_value(value)
            print("successful sketch call")

    def place_number(self):
        #Sets the value of the current selected cell equal to the user entered value. Called when the user presses the Enter key.
        print("attempting to place")
        print(f"currentPos: {self.currentPos}")
        if self.original_board[self.currentPos[0]][self.currentPos[1]] == 0:
            self.selected_cell.set_cell_value(self.selected_cell.get_sketched_value())
            print("placed")


    def get_cell_value(self):
        return self.selected_cell.get_cell_value()
    
    def get_sketched_value(self):
        return self.selected_cell.get_sketched_value()

    def reset_to_original(self):
        #Resets all cells in the board to their original values (0 if cleared, otherwise the corresponding digit).
        for row in range(9):
            for col in range(9):
                self.cells[row][col].set_cell_value(self.original_board[row][col])

    def is_full(self):
        #Returns a Boolean value indicating whether the board is full or not.
        return not any(0 in row for row in self.list)


    def update_board(self):
        #Updates the underlying 2D board with the values in all cells.
        pass

        #NOTE FROM ELIN: is this needed because it should already be updated with the functions above no?

    def find_empty(self):
        #Finds an empty cell and returns its row and col as a tuple(x, y).
        for row in range(9):
            for col in range(9):
                if self.list[row][col].value == 0:
                    return row, col
        return None
        #as a tuple?...

    def check_board(self):
        #Check whether the Sudoku board is solved correctly.

        def is_solved(arr):
            return sorted([x for x in arr if x!=0]) == list(range(1,10))

        #check rows and cols
        for i in range(9):
            if not is_solved([cell.value for cell in self.cells[i]]) or not is_solved(
                [self.cells[row][i].value for row in range(9)]
            ):
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
        
    def is_game_over(self):
        if not self.check_board():
            if self.is_full():
                return True
        return False

    def game_over_screen(self):
        self.width = min(width, 800)
        self.height = min(height, 600)

        #screen
        self.screen.fill("#0000CD")
        pygame.draw.rect(self.screen, ("#0000CD"), (0, 0, self.width, self.height))
        font = pygame.font.Font(None, 100)
        text = font.render("GAME OVER!", True, ("red"))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 3))
        self.screen.blit(text, text_rect)

        #button
        button_color = ("red")  # Green color
        restart_button = pygame.Rect(self.width // 4, self.height // 2, self.width // 2, 50)
        pygame.draw.rect(self.screen, button_color, restart_button)
        button_font = pygame.font.Font(None, 36)
        button_text = button_font.render("Restart Game", True, ("white"))
        button_text_rect = button_text.get_rect(center=restart_button.center)
        self.screen.blit(button_text, button_text_rect)

        pygame.display.flip()

        restart = False
        while not restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    if restart_button.collidepoint(mouseX, mouseY):
                        restart = True

        #restart game
        self.__init__(9, self.screen, "temp")

    def game_is_won(self):
        if self.check_board():
            if self.is_full():
                return True
        return False

    def draw_game_win(self):
        self.width = min(width, 800)
        self.height = min(height, 600)

        # screen
        self.screen.fill("#0000CD")
        pygame.draw.rect(self.screen, ("#0000CD"), (0, 0, self.width, self.height))
        font = pygame.font.Font(None, 100)
        text = font.render("YOU WIN!!!", True, ("red"))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 3))
        self.screen.blit(text, text_rect)

        # button
        button_color = ("red")  # Green color
        exit_game_button = pygame.Rect(self.width // 4, self.height // 2, self.width // 2, 50)
        pygame.draw.rect(self.screen, button_color, exit_game_button)
        button_font = pygame.font.Font(None, 36)
        button_text = button_font.render("Exit Game", True, ("white"))
        button_text_rect = button_text.get_rect(center=exit_game_button.center)
        self.screen.blit(button_text, button_text_rect)

        pygame.display.flip()

        exit_game = False
        while not exit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    if exit_game_button.collidepoint(mouseX, mouseY):
                        exit_game = True

        # exit game
        self.__init__(9, self.screen, "temp")

def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        draw_game_start(screen)
        #menu options...what happens with each button click:
        
        board = Board(9, screen, "temp")  # temporary call, should be done through the main menu
        # cell definition goes here
        clock = pygame.time.Clock()
        currentCell = [0, 0]
        running = True
        sketchNum = None #used in cell editting
        while running:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        running = False
                    
                    case pygame.MOUSEBUTTONDOWN: #cell nav by mouse
                        clickX = list(event.pos)[0]
                        clickY = list(event.pos)[1]
                        cellCol = clickX // cell_size
                        cellRow = clickY // cell_size
                        currentCell = [cellRow, cellCol]
                        board.select(cellRow, cellCol) 
                    
                    # checks all key user inputes for arrow nav and cell writing
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_RIGHT: #arrow keys for naviation
                                if currentCell[1] < 8:
                                    currentCell[1] += 1
                                    board.select(currentCell[0], currentCell[1])
                                
                            case pygame.K_LEFT:
                                if currentCell[1] > 0:
                                    currentCell[1] -= 1
                                    board.select(currentCell[0], currentCell[1])
                                    
                            case pygame.K_UP:
                                if currentCell[0] > 0:
                                    currentCell[0] -= 1
                                    board.select(currentCell[0], currentCell[1])
                                
                            case pygame.K_DOWN:
                                if currentCell[0] < 8:
                                    currentCell[0] += 1
                                    board.select(currentCell[0], currentCell[1])

                            case pygame.K_RETURN: #enter sketch
                                board.place_number()
                                print(f"submitted {board.get_sketched_value()} at {currentCell}") #TODO replace with call to board.place_number

                            case pygame.K_BACKSPACE:
                                pass
                                #TODO make call to the clear function/whatever wipes the cells sketch/entered number

                            case pygame.K_d:
                                running = False
                                print("tried to kms")

                            case _: #checks for number inputs to sketch
                                try:
                                    sketchNum = int(event.unicode)
                                    if sketchNum == 0: #0 is not a number for this
                                        continue
                                    board.sketch(sketchNum)
                                    print(f"sketched {sketchNum} at {currentCell}")
                                except: #not a number
                                    continue
                    case _:
                        continue

            if board.is_game_over():
                board.game_over_screen()
            if board.game_is_won():
                board.draw_game_win()

            screen.fill("whitesmoke")
            board.draw()
            pygame.display.flip()
            clock.tick(60)
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
