__author__ = 'chmikkel'

import random

height = 3
width = 3

#define the game board
#list of 9 elements with values
# . - not used
# X - team x
# O - team o


board = []
freeSpace = []

def initBoard():
    for i in range(9):
        board.append('.')

def printBoard():
    for y in range (height):
        for x in range (width):
            print board[y*height+x],
        print

def findFree():
    for y in range (height):
        for x in range (width):
            if board[y*height+x] == '.':
                freeSpace.append(y*height+x)
    print freeSpace
    print len(freeSpace)
    return len(freeSpace)


def makeMove(team):
    #pick one empty spot at random
    print 'freespace ', freeSpace
    if len(freeSpace):
        i = random.choice(freeSpace)
        freeSpace.remove(i)
        board[i] = team
        print 'chose ', i

def checkWin():
    #check vertical
    for x in range (width):
        marker = board [x]
        if marker != ".":
            if (marker == board[x+width]):
                if (marker == board[x+width*2]):
                    print "WINNER vert ",
                    print x, board [x], board [x+width], board[x+2*width]
    #check horizontal
    for y in range (height):
        marker = board[y*height]
        if marker != ".":
            if (marker == board[y*height+1]):
                if (marker == board[y*height+2]):
                    print "WINNER hor ",
                    print y, board [y*height], board [y*height+1], board[y*height+2]
    #check diagnal

initBoard()
printBoard()
findFree()
turn = 'X'
while len(freeSpace):
    makeMove(turn)
    printBoard()
    checkWin()
    if turn=='X':
        turn = 'Y'
    else:
        turn = 'X'
