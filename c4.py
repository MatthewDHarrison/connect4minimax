# Connect 4 in Python

# | | | | | | | |
# | | | | | | | |
# | | | | |x| | |
# | | |o|x|o| | |
# | | |x|o|x| | |
# | |x|x|o|o| | |
# ^^^^^^^^^^^^^^^
import random
import copy
CPU = 'o'
P1 = 'x'

rows, cols = (6, 7)
evaluationTable = [[3, 4, 5, 7, 5, 4, 3],
                  [4, 6, 8, 10, 8, 6, 4],
                  [5, 8, 11, 13, 11, 8, 5],
                  [5, 8, 11, 13, 11, 8, 5],
                  [4, 6, 8, 10, 8, 6, 4],
                  [3, 4, 5, 7, 5, 4, 3]]

def evaluateContent(b):
    utility = 138
    sum = 0
    for i in range(0,rows):
        for j in range(0,cols):
            if (b[i][j] == 'o'):
                sum += evaluationTable[i][j];
            elif (b[i][j] == 'x'):
                sum -= evaluationTable[i][j];
    return utility + sum;

#initialize empty board
def init():
    board = [[' ' for i in range(cols)] for j in range(rows)]
    return board

board = init()


def printBoard(b):
    for i in range(0, rows):
        str = '|'
        for j in range(0, cols):
            str += b[i][j] + '|'
        print(str)
    print('^^^^^^^^^^^^^^^')
    print(' 0 1 2 3 4 5 6')

def validMove(move):
    return (move in range(0, cols) and board[0][move] == ' ')

def getMove():
    badInput = True
    while(badInput):
        playerMove = input()
        try:
            playerMove = int(playerMove)
            if (validMove(playerMove)):
                if (board[0][playerMove] == ' '):
                    return playerMove
                else:
                    print('Invalid move -- space occupied')
            else:
                print('Bad Input!')
        except:
            print('Bad Input!')

def playMove(b, move, player):
    # check if valid move
    for i in range(0, rows):
        if (i == (rows - 1) or b[i + 1][move] != ' ') and b[i][move] == ' ':
            b[i][move] = player
            if (checkForWinner(b, player)):
                return True
    return False

def checkForWinner(b, player):
    for i in range(0, rows):
        for j in range(0, cols-3):
            if b[i][j] == player and b[i][j+1] == player and b[i][j+2] == player and b[i][j+3] == player:
                return True
    for i in range(0, rows-3):
        for j in range(0, cols):
            if b[i][j] == player and b[i+1][j] == player and b[i+2][j] == player and b[i+3][j] == player:
                return True
    for i in range(0, rows-3):
        for j in range(0, cols-3):
            if b[i][j] == player and b[i+1][j+1] == player and b[i+2][j+2] == player and b[i+3][j+3] == player:
                return True
    for i in range(3, rows):
        for j in range(0, cols-3):
            if b[i][j] == player and b[i-1][j+1] == player and b[i-2][j+2] == player and b[i-3][j+3] == player:
                return True

def getRandomMove():
    move = -1
    while (not validMove(move)):
        move = random.randint(0, cols)
    return move

def getMinimaxMove(b):
    move = -1
    preval = -999
    for i in range(0, cols):
        if validMove(i):
            boardCopy = [x[:] for x in b]
            playMove(boardCopy, i, CPU)
            eval = minimax(4, boardCopy, -999, 999, False)
            if eval > preval:
                preval = eval
                move = i
    return move

def minimax(depth, b, alpha, beta, isMaximising):
    if checkForWinner(b, CPU):
        return 999
    elif checkForWinner(b, P1):
        return -999

    if depth == 0:
        return evaluateContent(b)

    if isMaximising:
        maxEval = -999

        for i in range(0, cols):
            if validMove(i):
                boardCopy = [x[:] for x in b]
                playMove(boardCopy, i, CPU)
                eval = minimax(depth - 1, boardCopy, alpha, beta, False)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return maxEval


    else:
        minEval = 999

        for i in range(0, cols):
            if validMove(i):
                boardCopy = [x[:] for x in b]
                playMove(boardCopy, i, P1)
                eval = minimax(depth - 1, boardCopy, alpha, beta, True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return minEval


gameOverPlayer = False
gameOverCPU = False

print('You go first. Enter 0 - 6 to select column')
printBoard(board)
turn = 1
while (not gameOverPlayer and not gameOverCPU) and turn < 42:
    playerMove = getMove()
    gameOverPlayer = playMove(board, playerMove, 'x')
    turn += 1
    printBoard(board)
    if not gameOverPlayer:
        cpuMove = getMinimaxMove(board)
        gameOverCPU = playMove(board, cpuMove, 'o')
        turn += 1
    printBoard(board)


print('Game over!')
if gameOverPlayer:
    print('You won!')
elif gameOverCPU:
    print('Computer won!')
else:
    print('Miraculously, a tie!')


# made working c4 game with random moves
# first attempt at minimax:
    # tried to implement without depth value, exceeded maximum recursion depth
    # made depth smaller, CPU was bad at determining best move
# found algorithm https://softwareengineering.stackexchange.com/questions/263514/why-does-this-evaluation-function-work-in-a-connect-four-game-in-java
    # seems to work at first, but after 'blocking' stops working
    # check for winner function was buggy, rewrote to be more streamlined
    # seems to be working pretty well with depth=3, can avoid traps 2 moves in advance
