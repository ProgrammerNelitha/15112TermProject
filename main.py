from cmu_graphics import *
import copy
import os
import random

#TO DO LIST
#ability to show legals for just one box 
#ui for hints
#Later: ability to manually enter legals, different difficulties allow different hints
#Faster backtracker

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
#Board loading slightly modified from Sudoku hints
def getBoard(difficulty):
    path = random.choice(loadBoardPaths(difficulty))
    print('path:',path)
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
def onAppStart(app):
    app.difficulty=None
    app.gameOver=False

def splash_onKeyPress(app, key):
    if key == 'h': setActiveScreen('help')
    if key=='1': app.difficulty='easy'
    if key=='2': app.difficulty='medium'
    if key=='3': app.difficulty='hard'
    if key=='4': app.difficulty='expert'
    if key=='5': app.difficulty='evil'
    elif key=='enter': 
        if app.difficulty!=None: setActiveScreen('game')

def splash_onMousePress(app,mouseX,mouseY):
    print(mouseX,mouseY)
    if app.difficulty!=None: setActiveScreen('game')

def splash_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill='yellow',opacity=15)
    drawLabel('SUDOKU',app.width/2,100,size=75,bold=True, fill='orange')
    drawLabel("Press 'h' for instructions and enter/click to play!",app.width/2,185,size=20)
    drawLabel('Press 1 for Easy Difficulty',app.width/2,250,size=20,fill='lightGreen')
    drawLabel('Press 2 for Medium Difficulty',app.width/2,300,size=20,fill='green')
    drawLabel('Press 3 for Hard Difficulty',app.width/2,350,size=20,fill='yellow')
    drawLabel('Press 4 for Expert Difficulty',app.width/2,400,size=20,fill='orange')
    drawLabel('Press 5 for Evil Difficulty',app.width/2,450,size=20,fill='red')
    drawLabel(f'Chosen difficulty is: {app.difficulty}',app.width/2,550,size=20)
    drawRect(app.width/2,550,300,100,fill=None,align='center',border='black')
#-------------------------------------------------------------------------------
#Help Screen
def help_onKeyPress(app, key):
    if key == 'enter': setActiveScreen('splash')

def help_onMousePress(app,mouseX,mouseY):
    print(mouseX,mouseY)
    setActiveScreen('splash')

def help_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill='yellow',opacity=15)

    drawLabel('INSTRUCTIONS',app.width/2,100,size=75,bold=True, fill='orange')
    drawLabel("Press enter or click the screen to return to the main menu",app.width/2,185,size=20)
    drawLabel("In Sudoku you are given a 9x9 grid, which is composed of 9 'squares' (3x3).",app.width/2,250,size=20)
    drawLabel("Each cell in the board must be filled with numbers 1-9, with each number",app.width/2,280,size=20)
    drawLabel("being used only once in each row, column, and square",app.width/2,310,size=20)
    
    drawLabel("Use the mouse to select a cell, the keyboard to enter numbers, and 'backspace' to delete said numbers",app.width/2,450,size=20)

    drawLabel("If you wish you may turn on Legals Mode, which displays all possible values that a cell can take on",app.width/2,550,size=20)
#-------------------------------------------------------------------------------
#Backtracking code modified from the Mini-Sudoku solver
def getFewestLegals(board,legals):
    rows,cols=len(board),len(board[0])

    minLegal=0
    minCoord=None
    for i in range(rows):
        for j in range(cols):
            if (i,j) in legals:
                l=len(legals[(i,j)])
                if l<minLegal or minCoord==None:
                    minLegal=l
                    minCoord=(i,j)
    return minCoord

def sudokuSolver(app,board1):
    board=copy.deepcopy(board1)
    legals=app.legals.copy()
    #Start at position with fewest legals    
    x,y=getFewestLegals(board,legals)
    return f(legals,board,x,y)

def f(legals,board,x,y):
    #m,n=getFewestLegals(board,legals)
    if finishedSudoku(board):#len(app.legals[(m,n)])==0:
        return board
    else:
        #Try entering values 1-9
        for val in range(1,10):
            oldVal=board[x][y]
            board[x][y]=val
            legals=resetLegals(board)
            #print(f'attempt {x,y,val}',board)
            if isLegalSudoku(board):
                #print('is legal')
                if finishedSudoku(board): 
                    return board
                #update new spot
                a,b=getFewestLegals(board,legals)
                #if len(legals[(a,b)])==0: return board

                newBoard=f(legals,board,a,b)
                if newBoard!=None:
                    return newBoard
            board[x][y]=oldVal
            legals=resetLegals(board)
        return None

def isLegalSudoku(board):
    rows,cols=len(board),len(board[0])
    for row in range(rows):
        #Check each row
        if not BTcheckSudoku(board[row]): return False

        for colNum in range(cols):
            #Check Columns
            colList=[]
            #loop through rows to get column elements
            for rowList in board:
                colList.append(rowList[colNum])
            if not BTcheckSudoku(colList): return False

            #Check 3x3 blocks
            square=getSquareRegion(board,row,colNum)
            if not BTcheckSudoku(square): return False
    return True

def BTcheckSudoku(list):
    #Makes sure that no duplicates exist in a region
    for num in range(1,10):
        if list.count(num)>1: return False
    return True
#-------------------------------------------------------------------------------
#Stuff needed for game
def finishedSudoku(board):
    rows,cols=len(board),len(board[0])
    for row in range(rows):
        #Check each row
        if not checkSudoku(board[row]): return False

        for colNum in range(cols):
            #Check Columns
            colList=[]
            #loop through rows to get column elements
            for rowList in board:
                colList.append(rowList[colNum])
            if not checkSudoku(colList): return False

            #Check 3x3 blocks
            square=getSquareRegion(board,row,colNum)
            if not checkSudoku(square): return False
    return True

def checkSudoku(list):
    for num in range(1,10):
        if list.count(num)!=1: return False
    return True

def resetLegals(board):
    legals=dict()
    rows,cols=len(board),len(board[0])
    for row in range(rows):
        for col in range(cols):
            if board[row][col]==0: 
                legalSet=getLegals(board,row,col)
                legals[(row,col)]=legalSet
    return legals
#-------------------------------------------------------------------------------
#Game Screen
def game_onScreenActivate(app):
    #Initiailze board
    app.rows = 9
    app.cols = 9
    
    app.board=getBoard(app.difficulty)
    print('starting board:',app.board)
    app.banned=[]
    app.legals=dict()
    #Create ban list and legal list simultaneously
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col]!=0: 
                app.banned.append((row,col))
            else:
                legalSet=getLegals(app.board,row,col)
                app.legals[(row,col)]=legalSet
    app.solution = sudokuSolver(app,app.board)
    app.wrongCells = []

    app.boardLeft = 75
    app.boardTop = 130
    app.boardWidth = 550
    app.boardHeight = 550
    app.cellBorderWidth = 2
    
    app.selectedCellX=None
    app.selectedCellY=None

    app.showLegals=False

    app.hint1X=None
    app.hint1Y=None
    app.hint1Val=None
    app.hint1Solved=False
    app.hint2=False
    app.hint2Solved=False

    app.gameOver=False

def game_onMousePress(app,mouseX,mouseY):
    print(mouseX,mouseY)
    app.selectedCellX,app.selectedCellY=findSelectedCell(app,mouseX,mouseY)

    if 725<=mouseX<=915 and 180<=mouseY<=220:
        app.showLegals=not app.showLegals

    if app.gameOver:
         setActiveScreen('splash')

def game_onKeyPress(app,key):
    if app.selectedCellX!=None:
        if key.isdigit():
            if (app.selectedCellX,app.selectedCellY) not in app.banned and app.board[app.selectedCellX][app.selectedCellY]==0:
                app.board[app.selectedCellX][app.selectedCellY]=int(key)
                if app.board[app.selectedCellX][app.selectedCellY]!=app.solution[app.selectedCellX][app.selectedCellY]:
                    app.wrongCells.append((app.selectedCellX,app.selectedCellY))
                
        if key=='backspace':
            app.board[app.selectedCellX][app.selectedCellY]=0
            if (app.selectedCellX,app.selectedCellY) in app.wrongCells:
                app.wrongCells.remove((app.selectedCellX,app.selectedCellY))
        app.legals=resetLegals(app.board)
    if key=='h':
        hintX,hintY=getFewestLegals(app.board,app.legals)
        l=getLegals(hintX,hintY)
        if len(l)==1:
            app.hint1X,app.hint1Y=hintX,hintY
            for val in l: app.hint1Val=val
    if key == 'enter' and app.gameOver: 
        setActiveScreen('splash')
        
def game_onStep(app):
    if finishedSudoku(app.board):
        app.gameOver=True
        print('yay')

def game_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill='yellow',opacity=15)
    drawBoard(app)
    drawBoardBorder(app)
    drawRect(820,200,190,40,fill=None,border='black',align='center')
    if app.showLegals:
        drawLabel("Display Legals",820,200,size=25,bold=True, fill='green')
    else:
        drawLabel("Display Legals",820,200,size=25,bold=True, fill='red')

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
            elif app.showLegals==True and (row,col) not in app.banned:
                for legalVal in app.legals[(row,col)]:
                    drawLegal(app,legalVal,row,col)
            if (row,col) in app.wrongCells:
                drawRect(numX,numY,w,h,fill='red',opacity=25)

    if app.hint1X!=None:
        if len(getLegals(app.board,app.hint1X,app.hint1Y))!=1:
            app.hint1X,app.hint1Y=None,None
        else:
            w, h = getCellSize(app)
            hintX,hintY = numX, numY = getCellLeftTop(app,app.hint1X,app.hint1Y)
            drawRect(hintX,hintY,w,h,fill='blue',opacity=25)
            drawLabel(f'Place a {app.hint1Val} at row {app.hint1X} column {app.hint1Y}', 650, 130)

    if app.gameOver:
        drawLabel("Congratulations You Win!",820,535,size=25,bold=True, fill='orange')
        drawLabel("Press enter or click the screen",820,600,size=20)
        drawLabel(" to return to the main menu",820,630,size=20)              

def drawLegal(app,legalVal,row,col):
    numX, numY = getCellLeftTop(app, row,col)
    #75,130 is top left corner
    if int(legalVal)==1:
        x=numX+10
        y=numY+10
    elif int(legalVal)==2:
        x=numX+30
        y=numY+10
    elif int(legalVal)==3:
        x=numX+50
        y=numY+10
    elif int(legalVal)==4:
        x=numX+10
        y=numY+30
    elif int(legalVal)==5:
        x=numX+30
        y=numY+30
    elif int(legalVal)==6:
        x=numX+50
        y=numY+30
    elif int(legalVal)==7:
        x=numX+10
        y=numY+50
    elif int(legalVal)==8:
        x=numX+30
        y=numY+50
    elif int(legalVal)==9:
        x=numX+50
        y=numY+50
    drawLabel(legalVal,x,y,size=15)
#-------------------------------------------------------------------------------
runAppWithScreens(initialScreen='splash',width=1000,height=700)