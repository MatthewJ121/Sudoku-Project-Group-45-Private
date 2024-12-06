#main file to run the sudoku game
import pygame
from sudoku_generator import SudokuGenerator,generate_sudoku

cell_size = 50 #only change this one to make the cells smaller/bigger
width = cell_size*9
height = cell_size*9+cell_size

def tempGen():
    list=[]
    for i in range(1,82,9):
        list2 = []
        while i%9!=0:
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
        pass

    def set_sketched_value(self, value):
        pass

    def draw(self):
        pass

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
                self.list = tempGen
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty

    def draw(self): #ONLY DRAWS LINES RN
        for i in range(1,width//cell_size+1): #vertical
            if i%3==0:
                pygame.draw.line(self.screen, "black", (cell_size*i,0), (cell_size*i,height-cell_size), 3)
            else:
                pygame.draw.line(self.screen, "black", (cell_size*i,0), (cell_size*i,height-cell_size))

        for i in range(1,(height-cell_size)//cell_size+1): #horizontal
            if i%3==0:
                pygame.draw.line(self.screen, "black", (0,cell_size*i), (width,cell_size*i), 3)
            else:
                pygame.draw.line(self.screen, "black", (0,cell_size*i), (width,cell_size*i))


def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((width,height)) 
        board = Board(9, screen, "temp") #temporary call, should be done through the main menu
        #cell definition goes here
        clock = pygame.time.Clock()
        currentCell = [0,0]
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
                        cellRow = clickX//cell_size
                        cellCol = clickY//cell_size
                        currentCell = [cellRow,cellCol]
                    
                    #checks all key user inputes for arrow nav and cell writing
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_RIGHT: #arrow keys for naviation
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

                            case pygame.K_RETURN: #enter sketch
                                print(f"submitted {sketchNum} at {currentCell}") #TODO replace with call to board.sketch

                            case pygame.K_BACKSPACE:
                                pass
                                #TODO make call to the clear function/whatever wipes the cells sketch/entered number

                            case _: #checks for number inputs to sketch
                                try:
                                    sketchNum = int(event.unicode)
                                    if sketchNum == 0:
                                        sketchNum = None
                                    print(f"num pressed: {sketchNum}") #TODO replace with call to board.place_number
                                except: #not a number
                                    continue
                    case _:
                        continue                       

            screen.fill("white")
            board.draw()
            pygame.display.flip()
            clock.tick(60)
        generate_sudoku(9,0)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()