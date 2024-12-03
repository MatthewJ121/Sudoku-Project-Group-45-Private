#main file to run the sudoku game
import pygame
from sudoku_generator import SudokuGenerator
from sudoku_generator import generate_sudoku
cell_size = 50 #only change this one to make the cells smaller/bigger
width = cell_size*9
height = cell_size*9+cell_size

class Cell:
    pass

class Board: #idk if width/height are in pixels or cells, rn its pixels -matthew
    def __init__(self, width, height, screen, difficulty="easy"):
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
        board = Board(width, height, screen)
        #cell definition goes here
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill("white")
            board.draw()
            pygame.display.flip()
            clock.tick(60)
        generate_sudoku(9,0)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()