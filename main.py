from cmu_graphics import *
import copy
import os
import random
#-------------------------------------------------------------------------------
#Code slightly modified from the Tetris Case Study Step 1
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col,None, 'black', app.cellBorderWidth)

def drawBoardBorder(app):
  # draw the board outline and 3x3 cells:
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)
    for i in range(9):
        x=app.boardLeft+((app.boardWidth/3)*(i%3))
        y=app.boardTop+((app.boardHeight/3)*(i//3))
        drawRect(x,y,app.boardWidth/3,app.boardHeight/3,fill=None, border='black',borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, color, border, borderWidth):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border=border,
             borderWidth=borderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)
#-------------------------------------------------------------------------------
def findSelectedCell(app,mx,my):
    for row in range(app.rows):
        for col in range(app.cols):
            x, y = getCellLeftTop(app, row, col)
            w, h = getCellSize(app)

            if x-w<=mx<=x+w and y-h<=my<=y+h:
                return (row,col)
    return (None,None)
#-------------------------------------------------------------------------------
def getSquareRegion(board,row,col):
    if row%3==0: rowsList=[row,row+1,row+2]
    elif row%3==1: rowsList=[row-1,row,row+1]
    elif row%3==2: rowsList=[row-2,row-1,row]

    if col%3==0: colsList=[col,col+1,col+2]
    elif col%3==1: colsList=[col-1,col,col+1]
    elif col%3==2: colsList=[col-2,col-1,col]

    vals=[]
    for num1 in rowsList:
        for num2 in colsList:
            if board[num1][num2]!=0:
                vals.append(board[num1][num2])
    return vals

def getLegals(board,row,col):
    rows,cols=len(board),len(board[0])
    legals=set()
    colList=[]
    for rowNum in range(rows):
        colList.append(board[rowNum][col])
    square=getSquareRegion(board,row,col)

    for num in range(1,10):
        #Check Row
        if num not in board[row]:
            if num not in colList:
                #Check Square
                if num not in square:
                    legals.add(num)
    return legals
#-------------------------------------------------------------------------------
#Backtracking code modified from the Mini-Sudoku solver
'''
#Backtraking
def sudokuSolver(app):
    board=copy.deepcopy(app.board)
    rows,cols=len(board),len(board[0])
    for i in range(rows):
        for j in range(cols):
            if board[i][j]==None:
                return f(board,i,j)

def f(board,x,y):
    if boardFinished(board) and isLegalSudoku(board):
        return board
    else:
        for val in range(9):
            oldVal=board[x][y]
            board[x][y]=val
            if isLegalSudoku(board):
                if boardFinished(board): return board
                #update new spot
                a,b=newIndex(board,x,y)
                newBoard=f(board,a,b)
                if newBoard!=None:
                    return newBoard
            board[x][y]=oldVal
        return None

def boardFinished(board):
    rows,cols=len(board),len(board[0])
    for i in range(rows):
        for j in range(cols):
            if board[i][j]==None:
                return False
    return True

def newIndex(board,x,y):
    rows,cols=len(board),len(board[0])
    for i in range(x,rows):
        for j in range(cols):
            if (i==x and j>y) or i>x:
                if board[i][j]==None:
                    return (i,j)

def isLegalSudoku(board):
    rows,cols=len(board),len(board[0])
    #Check each row 
    for rowList in board:
        if not isLegal(rowList): return False
    #Check Columns
    for colNum in range(cols):
        colList=[]
        #loop through rows to get column elements
        for row in board:
            colList.append(row[colNum])
        if not isLegal(colList): return False
    #Check 3x3 blocks
    
    return True
'''
#-------------------------------------------------------------------------------
#Board loading from Sudoku hints
def getBoard(difficulty):
    path = random.choice(loadBoardPaths(difficulty))
    file = readFile(f"C:\\Users\\1234l\\Documents\\Documents\\CMU\\15112\\term project\\tp-starter-files\\tp-starter-files\\{path}")
    file = file.splitlines()
    board=[]
    for line in file:
        rowList=[]
        for num in line.split(' '):
            rowList.append(int(num))
        board.append(rowList)
    return board


def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def loadBoardPaths(filters):
        boardPaths = [ ]
        for filename in os.listdir(f'C:\\Users\\1234l\\Documents\\Documents\\CMU\\15112\\term project\\tp-starter-files\\tp-starter-files\\boards'):
            if filename.endswith('.txt'):
                if hasFilters(filename, filters):
                    boardPaths.append(f'boards/{filename}')
        return boardPaths

def hasFilters(filename, filters=None):
    if filters == None: return True
    for filter in filters:
        if filter not in filename:
            return False
    return True

#-------------------------------------------------------------------------------
#Splash Screen
def splash_onKeyPress(app, key):
    if key == 'h': setActiveScreen('help')
    elif key=='enter': 
        setActiveScreen('game')

def splash_onMousePress(app,mouseX,mouseY):
    setActiveScreen('game')

def splash_redrawAll(app):
    drawLabel('insert splash screen, press h for instructions, and enter/click to play',app.width/2,app.height/2)
#-------------------------------------------------------------------------------
#Help Screen
def help_onKeyPress(app, key):
    if key == 'enter': setActiveScreen('splash')

def help_onMousePress(app,mouseX,mouseY):
    setActiveScreen('splash')

def help_redrawAll(app):
    drawLabel('instructions. press enter/click to return to splash screen',app.width/2,app.height/2)
#-------------------------------------------------------------------------------
#Game Screen
def game_onAppStart(app):
    #Initiailze board
    app.rows = 9
    app.cols = 9
    
    app.board=getBoard('easy')
    app.banned=[]
    app.legals=[]
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col]!=0: 
                app.banned.append((row,col))
            else:
                legalSet=getLegals(app.board,row,col)
                app.legals.append((row,col,legalSet))

    app.boardLeft = 75
    app.boardTop = 130
    app.boardWidth = 550
    app.boardHeight = 550
    app.cellBorderWidth = 2
    
    app.selectedCellX=None
    app.selectedCellY=None

    app.showLegals=False
    # app.solvedBoard=sudokuSolver(app)

def game_onMousePress(app,mouseX,mouseY):
    print(mouseX,mouseY)
    app.selectedCellX,app.selectedCellY=findSelectedCell(app,mouseX,mouseY) 

def game_onKeyPress(app,key):
    if app.selectedCellX!=None:
        if key.isdigit():
            if (app.selectedCellX,app.selectedCellY) not in app.banned:
                app.board[app.selectedCellX][app.selectedCellY]=int(key)

def game_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill='yellow',opacity=15)
    drawBoard(app)
    drawBoardBorder(app)
    if app.selectedCellX!=None:
        drawCell(app, app.selectedCellX, app.selectedCellY, None, 'red', app.cellBorderWidth*3)
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col]!=0:
                numX, numY = getCellLeftTop(app, row,col)
                w, h = getCellSize(app)
                drawLabel(app.board[row][col],numX+w/2,numY+h/2,size=25)
                if (row,col) in app.banned:
                    drawRect(numX,numY,w,h,fill=rgb(135,62,133),opacity=25)
                else:
                    for legalVal in getLegals(app.board,row,col):
                        drawLegal(legalVal,row,col)

def drawLegal(legalVal,row,col):
    numX, numY = getCellLeftTop(app, row,col)
    if int(legalVal)==1:
        x=numX+5
        y=numY+5
    drawLabel(legalVal,x,y,size=10)
#-------------------------------------------------------------------------------
runAppWithScreens(initialScreen='splash',width=1000,height=700)