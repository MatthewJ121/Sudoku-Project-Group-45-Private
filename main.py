# main file to run the sudoku game
import pygame,sys
from sudoku_generator import SudokuGenerator, generate_sudoku

cell_size = 70  # only change this one to make the cells smaller/bigger
width = cell_size * 9
height = cell_size * 9

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
    title_surface = start_title_font.render("Sudoku!", True, ("black"))
    title_rectangle = title_surface.get_rect(center=(width // 2, height // 2 - 100))
    screen.blit(title_surface, title_rectangle)

    # game modes
    game_mode_surface = game_mode_font.render("Select Game Mode:", True, ("black"))
    game_mode_rectangle = game_mode_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(game_mode_surface, game_mode_rectangle)

    # buttons and text
    easy_text = button_font.render("Easy", True, ("black"))
    medium_text = button_font.render("Medium", True, ("black"))
    hard_text = button_font.render("Hard", True, ("black"))

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
    # global since we want while loop later to manipulate them
    global reset_rectangle, restart_rectangle, exit_rectangle
    button_font = pygame.font.Font(None, 50)

    # Initialize buttons
    # Initialize text first
    reset_text = button_font.render("Reset", True, ("black"))
    restart_text = button_font.render("Restart", True, ("black"))
    exit_text = button_font.render("Exit", True, ("black"))

    # Initialize button background color and text
    reset_surface = pygame.Surface((reset_text.get_size()[0] + 20, reset_text.get_size()[1] + 20))
    reset_surface.fill("light blue")
    reset_surface.blit(reset_text, (10, 10))
    restart_surface = pygame.Surface((restart_text.get_size()[0] + 20, restart_text.get_size()[1] + 20))
    restart_surface.fill("light blue")
    restart_surface.blit(restart_text, (10, 10))
    exit_surface = pygame.Surface((exit_text.get_size()[0] + 20, exit_text.get_size()[1] + 20))
    exit_surface.fill("light blue")
    exit_surface.blit(exit_text, (10, 10))

    # Initialize button rectangle
    reset_rectangle = reset_surface.get_rect(center=(width // 2 - 200, height + 50))
    restart_rectangle = restart_surface.get_rect(center=(width // 2, height + 50))
    exit_rectangle = exit_surface.get_rect(center=(width // 2 + 200, height + 50))

    # Draw buttons
    screen.blit(reset_surface, reset_rectangle)
    screen.blit(restart_surface, restart_rectangle)
    screen.blit(exit_surface, exit_rectangle)

#temporary function used for debugging
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
    def __init__(self, value, row, col, screen, isOriginal):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.isSelected = False
        self.sketched_value = 0
        self.isOriginal = isOriginal

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value
        self.set_cell_value(0) #so the draw function knows to sketch, not place
        
    def get_sketched_value(self):
        return self.sketched_value
    
    def get_cell_value(self):
        return self.value

    def draw(self):
        #draw cell
        cell = pygame.Rect(self.col * cell_size, self.row * cell_size, cell_size, cell_size)
        #highlight
        if self.isSelected:
            color = "yellow"
        elif self.isOriginal:
            color = "grey85"
        else:
            color = "whitesmoke"
        pygame.draw.rect(self.screen, color, cell)
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
            "test": 3
        }
        empty_cells = difficulty_map.get(difficulty, 30)
        result = generate_sudoku(9,empty_cells)
        self.list = result[1]
        self.preRemoval = result[0]

        self.original_board = self.list
        self.width = width
        self.height = height
        self.screen = screen
        self.currentPos = [0,0]

        self.cells = [[Cell(self.list[row][col], row, col, self.screen,
                            True if self.original_board[row][col] != 0 else False #sets isOriginal
                            ) #constructor
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
                self.screen, line_color, (i * cell_size, 0), (i * cell_size, height), line_thickness
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

    def clear(self): 
        # Clears the value cell. Note that the user can only remove the cell values and sketched values that are filled by themselves.
        if self.original_board[self.currentPos[0]][self.currentPos[1]] == 0:
            self.selected_cell.set_cell_value(0)
            self.selected_cell.set_sketched_value(0)

    def sketch(self, value):
        # Sets the sketched value of the current selected cell equal to the user entered value. It will be displayed at the top left corner of the cell using the draw() function.
        if self.original_board[self.currentPos[0]][self.currentPos[1]] == 0:
            self.selected_cell.set_sketched_value(value)

    def place_number(self):
        #Sets the value of the current selected cell equal to the user entered value. Called when the user presses the Enter key.
        if self.original_board[self.currentPos[0]][self.currentPos[1]] == 0:
            self.selected_cell.set_cell_value(self.selected_cell.get_sketched_value())

    def get_cell_value(self):
        return self.selected_cell.get_cell_value()
    
    def get_sketched_value(self):
        return self.selected_cell.get_sketched_value()

    def reset_to_original(self):
        #Resets all cells in the board to their original values (0 if cleared, otherwise the corresponding digit).
        for row in range(9):
            for col in range(9):
                if self.original_board[row][col] == 0:
                    self.cells[row][col].set_cell_value(0)
                    self.cells[row][col].set_sketched_value(0)
        #Updates the underlying 2D board with the values in all cells.
        pass

        #NOTE FROM ELIN: is this needed because it should already be updated with the functions above no?
        
    def is_full(self):
        #Returns a Boolean value indicating whether the board is full or not.
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].get_cell_value() == 0:
                    return False
        return True
    
    def check_board(self):
        #Check whether the Sudoku board is solved correctly.
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].get_cell_value() != self.preRemoval[row][col]:
                    return False
        return True
        
        '''def is_solved(arr):
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

        return True'''
        
    def is_game_over(self):
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
        button_color = ("red")  
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
        self.reset_to_original()

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
        button_color = ("red")
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
        draw_game_start(self.screen)

def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((width, height + cell_size*2))
        board = Board(9, screen, draw_game_start(screen))  #draw_game_start returns difficulty
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
                        if clickX <= width and clickY <= height:
                            cellCol = clickX // cell_size
                            cellRow = clickY // cell_size
                            currentCell = [cellRow, cellCol]
                            board.select(cellRow, cellCol) 

                        #detection for pressing the 3 in_game_options
                        if reset_rectangle.collidepoint(event.pos):
                            board.reset_to_original()
                        elif restart_rectangle.collidepoint(event.pos):
                            board = Board(9, screen, draw_game_start(screen))
                        elif exit_rectangle.collidepoint(event.pos):
                            sys.exit()
                    
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
                                print("pre removal:")
                                for row in board.preRemoval:
                                    print(row)
                                print("current")
                                for row in board.cells:
                                    for col in row:
                                        print(col.get_cell_value(),end=" ")
                                    print("") 

                            case pygame.K_BACKSPACE:
                                board.clear()

                            case _: #checks for number inputs to sketch
                                try:
                                    sketchNum = int(event.unicode)
                                    if sketchNum == 0: #0 is not a number for this
                                        continue
                                    board.sketch(sketchNum)
                                except: #not a number
                                    continue
                    case _:
                        continue

            if board.is_game_over():
                if board.check_board():
                    board.draw_game_win()
                else:
                    board.game_over_screen()

            screen.fill("whitesmoke")
            board.draw()
            draw_ingame_options(screen)
            pygame.display.update()
            clock.tick(60)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
