#main file to run the sudoku game
import pygame
from sudoku_generator import SudokuGenerator

def Cell():
    pass

def Board():
    pass

def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((640,710))
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill("white") # can also be RGB value
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()