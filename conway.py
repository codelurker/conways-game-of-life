# May 20, 2012
# Conway's game of life simulator
'''
Each cell has eight neighbours, except the ones reside on the borders.
Rules:
1. Any live cell with fewer than two live neighbours dies, as if caused by under-population.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overcrowding.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
'''
import sys, pygame
from pygame.locals import *

class Game(object):
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.gridSize = 9
        self.colorFill = (0, 0, 0)
        self.colorUnfill = (255, 255, 255)
        self.matrix = []
        # row and col are the dimension of the grid
        self.row = self.height / (self.gridSize + 1)
        self.col = self.width / (self.gridSize + 1)

        self.initMatrix()

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        #self.background = pygame.Surface((self.width, self.height))
        #self.background.fill((255, 255, 255))
        self.screen.fill((255, 255, 255))

        self.drawGrid()

        self.clock = pygame.time.Clock()

    def initMatrix(self):
        for y in xrange(self.row):
            self.matrix.append([])
            for x in xrange(self.col):
                self.matrix[y].append(0)

    def drawGrid(self):
        for x in xrange(0, self.width, 10):
            pygame.draw.line(self.screen, (200, 200, 200), (x, 0), (x, self.height), 1)

        for y in xrange(0, self.height, 10):
            pygame.draw.line(self.screen, (200, 200, 200), (0, y), (self.width, y), 1)
        # reflesh the painting
        pygame.display.flip()

    def run(self):
        running = True

        while running:
            self.clock.tick(30)
            x, y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 2:
                        print 'middle button pressed, game started...'
                        self.conway()

                    idx_x = x / 10
                    idx_y = y / 10
                    if self.matrix[idx_y][idx_x] == 1:
                        pygame.draw.rect(self.screen, self.colorUnfill, (idx_x * 10 + 1, idx_y * 10 + 1, self.gridSize, self.gridSize))
                        self.matrix[idx_y][idx_x] = 0
                    else:
                        pygame.draw.rect(self.screen, self.colorFill, (idx_x * 10 + 1, idx_y * 10 + 1, self.gridSize, self.gridSize))
                        self.matrix[idx_y][idx_x] = 1
                    pygame.display.flip()

    def conway(self):
        newMatrix = []

        for r in xrange(self.row):
            newMatrix.append([])
            for c in xrange(self.col):
                newMatrix[r].append(0)

        while True:
            # make it 3fps
            self.clock.tick(3)
            for r in xrange(self.row):
                for c in xrange(self.col):
                    neighbours = self.getNeighbours(r, c)
                    # if this cell is alive
                    if self.matrix[r][c] == 1:
                        # die of under-popularion or overcrowding
                        if neighbours < 2 or neighbours > 3:
                            newMatrix[r][c] = 0
                        else :
                            newMatrix[r][c] = 1
                    # cell is dead
                    else :
                        if neighbours == 3:
                            newMatrix[r][c] = 1
                        else :
                            newMatrix[r][c] = 0

            for r in xrange(self.row):
                for c in xrange(self.col):
                    # replace the previous generation of the new generation
                    self.matrix[r][c] = newMatrix[r][c]
                    if newMatrix[r][c] == 1:
                        pygame.draw.rect(self.screen, self.colorFill, (c * 10 + 1, r * 10 + 1, self.gridSize, self.gridSize))
                    elif newMatrix[r][c] == 0:
                        pygame.draw.rect(self.screen, self.colorUnfill, (c * 10 + 1, r * 10 + 1, self.gridSize, self.gridSize))
            pygame.display.flip()
                        
    def getNeighbours(self, r, c):
        # 8 possible neighbours
        dr = [-1, -1, -1, 0, 1, 1, 1, 0]
        dc = [-1, 0, 1, 1, 1, 0, -1, -1]
        neighbours = 0

        for i in xrange(8):
            row = r + dr[i]
            col = c + dc[i]
            if row >= 0 and col >= 0 and row < self.row and col < self.col:
                if self.matrix[row][col] == 1:
                    neighbours += 1

        return neighbours

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
