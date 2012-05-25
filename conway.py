#!/usr/bin/env python

# Copyright (c) 2012 Dougam Ngou <wvvwwwvvvv@gmail.com>
# Conway's game of life simulator

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

''' -------------------------------------------------------------------
Each cell has eight neighbours, except the ones reside on the borders.
Rules:
1. Any live cell with fewer than two live neighbours dies, 
    as if caused by under-population.
2. Any live cell with two or three live neighbours lives on 
    to the next generation.
3. Any live cell with more than three live neighbours dies, 
    as if by overcrowding.
4. Any dead cell with exactly three live neighbours becomes 
    a live cell, as if by reproduction.
    ------------------------------------------------------------------
'''

import sys, pygame
import random
from pygame.locals import *

class Game(object):
    def __init__(self):
        # dimension of the game window
        self.width = 1280
        self.height = 720
        # start position of the cells
        self.offset_x = 20
        self.offset_y = 60
        # length of the square cells
        self.gridSize = 9
        self.colorFill = (0, 0, 0)
        self.colorUnfill = (255, 255, 255)
        # state of the cells is stored in matrix
        self.matrix = []
        # restore the state of the next generation
        self.next_matrix = []
        # row and col are the dimension of the matrix
        self.row = (self.height - self.offset_x - 
            self.offset_y) / (self.gridSize + 1)
        self.col = (self.width-2*self.offset_x) / (self.gridSize + 1)

        self.initMatrix()

        pygame.init()
        pygame.display.set_caption("Conway's game of life simulator")
        self.screen = pygame.display.set_mode((self.width, self.height))
        #self.background = pygame.Surface((self.width, self.height))
        #self.background.fill((255, 255, 255))
        self.screen.fill((255, 255, 255))

        self.draw_help_text()
        self.drawGrid(self.offset_x, self.offset_y)

        self.clock = pygame.time.Clock()

    def initMatrix(self):
        for y in xrange(self.row):
            self.matrix.append([])
            self.next_matrix.append([])
            for x in xrange(self.col):
                self.matrix[y].append(False)
                self.next_matrix[y].append(False)

    def drawGrid(self, offset_x, offset_y):

        width = self.width - offset_x * 2
        height = self.height - offset_x - offset_y

        grey = (200, 200, 200)
        dark = (120, 120, 120)
        
        # draw vertical lines
        for x in xrange(offset_x + 10, width + offset_x, 10):
            pygame.draw.line(self.screen, grey, (x, offset_y), 
                (x, offset_y + height), 1)
        # draw horizontal lines
        for y in xrange(offset_y + 10, height + offset_y, 10):
            pygame.draw.line(self.screen, grey, (offset_x, y), 
                (width + offset_x, y), 1)

        # draw the thick borders of the grid: top, buttom, left, right
        pygame.draw.line(self.screen, dark, (offset_x - 2, offset_y - 1),
            (offset_x + width + 2, offset_y - 1), 3)
        pygame.draw.line(self.screen, dark, (offset_x - 2, offset_y + 
            height + 1), (offset_x + width + 2, offset_y + height + 1), 3)
        pygame.draw.line(self.screen, dark, (offset_x - 1, offset_y - 1), 
            (offset_x - 1, offset_y + height + 1), 3)
        pygame.draw.line(self.screen, dark, (offset_x + width + 1, 
            offset_y - 1), (offset_x + 1 + width, offset_y + height + 1), 3)

        # refresh the painting
        pygame.display.flip()

    def draw_help_text(self):
        title = 'Conway\'s game of life'
        help_text = ['Mouse click to toggle cell state',
            '<SPACE> to start or pause the game', 
            '<d> or <1~9> to set random state', 
            '<r> to reset and <q> to quit']
        
        myfont = pygame.font.SysFont('Purisa', 20, True)
        text = myfont.render(title, 1, (255, 150, 0))
        self.screen.blit(text, (470, 10))

        myfont = pygame.font.SysFont('DejaVu Sans Mono', 10)
        y = 10
        for line in help_text:
            text = myfont.render(line, True, (255, 0, 0))
            self.screen.blit(text, (25, y))
            y += 10
            
    def random_state(self, mode):
        # the probability whether a cell is initially alive
        probability = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

        if mode == 0:
            idx = int(random.random() * 10)
        elif mode >= 0 and mode <= 9:
            idx = mode

        for r in xrange(self.row):
            for c in xrange(self.col):
                if probability[idx] > random.random():
                    self.matrix[r][c] = True
                else:
                    self.matrix[r][c] = False

        
    def handle_keyboard(self, event):
        
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
        elif event.key == pygame.K_r:
            print 'reseting grid...'
            self.reset_grid()
        elif event.key == pygame.K_SPACE:
            print 'space key pressed, game started...'
            self.conway()
        elif event.key == pygame.K_q:
            pygame.quit()
        # set random probability
        elif event.key == pygame.K_d:
            self.random_state(0)
            self.print_state()
        # set defined probability
        elif event.key >= pygame.K_1 and event.key <= K_9:
            self.random_state(int(event.key - K_1 + 1))
            self.print_state()
    
    # set the state of every cell to be 'dead'
    def reset_grid(self):

        for r in xrange(self.row):
            for c in xrange(self.col):
                if self.matrix[r][c] == True:
                    self.matrix[r][c] = False
                    rect = (c * (self.gridSize + 1)  + self.offset_x + 1, 
                        r *(self.gridSize + 1) + self.offset_y + 1,
                        self.gridSize, self.gridSize)
                    pygame.draw.rect(self.screen, self.colorUnfill, rect)
        # refresh the display
        pygame.display.flip()

    def run(self):

        sz = self.gridSize + 1
        while True:
            # make it 30 frame per second
            self.clock.tick(30)
            x, y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.KEYDOWN:
                    self.handle_keyboard(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # event outside the cell borders, ignore it
                    if (x > self.width - self.offset_x 
                        or y > self.height - self.offset_x
                        or x < self.offset_x or y < self.offset_y):
                        continue
                    # get the corresponding matrix index
                    idx_x = (x - self.offset_x) / sz
                    idx_y = (y - self.offset_y) / sz
                    rect = (x / sz * sz + 1, y / sz * sz + 1, 
                        self.gridSize, self.gridSize)
                    # flip the cell state
                    if self.matrix[idx_y][idx_x] == True:
                        pygame.draw.rect(self.screen, self.colorUnfill, rect)
                        self.matrix[idx_y][idx_x] = False
                    else:
                        pygame.draw.rect(self.screen, self.colorFill, rect)
                        self.matrix[idx_y][idx_x] = True
                    pygame.display.flip()

    def next_gen(self):

        for r in xrange(self.row):
            for c in xrange(self.col):
                neighbours = self.getNeighbours(r, c)
                # if this cell is alive
                if self.matrix[r][c] == True:
                    # die of under-popularion or overcrowding
                    if neighbours < 2 or neighbours > 3:
                        self.next_matrix[r][c] = False
                    else :
                        self.next_matrix[r][c] = True
                # cell is dead
                else :
                    if neighbours == 3:
                        self.next_matrix[r][c] = True
                    else :
                        self.next_matrix[r][c] = False
        # set the matrix to be the new state
        for r in xrange(self.row):
            for c in xrange(self.col):
                self.matrix[r][c] = self.next_matrix[r][c]

    def print_state(self):

        for r in xrange(self.row):
            for c in xrange(self.col):
                # replace the previous generation of the new generation
                #self.matrix[r][c] = new_matrix[r][c]

                rect = (c * (self.gridSize + 1)  + self.offset_x+ 1, 
                    r * (self.gridSize + 1) + self.offset_y + 1, 
                    self.gridSize, self.gridSize)
                if self.matrix[r][c] == True:
                    pygame.draw.rect(self.screen, self.colorFill, rect)
                elif self.matrix[r][c] == False:
                    pygame.draw.rect(self.screen, self.colorUnfill, rect)
        # refresh the painting
        pygame.display.flip()

    def conway(self):
        running = True
        pause = False

        while running:
            # make it 3fps
            self.clock.tick(3)
            x, y = pygame.mouse.get_pos()

            # collect and handle the event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                # keyboard stroke
                elif event.type == pygame.KEYDOWN:
                    # pause 
                    if event.key == pygame.K_SPACE:
                        pause = not pause
                    # reset the grid
                    elif event.key == pygame.K_r:
                        running = False
                        self.reset_grid()
                    # quit
                    elif event.key == pygame.K_q:
                        pygame.quit()

            if pause == True:
                continue

            self.next_gen()
            self.print_state()
                                    
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
