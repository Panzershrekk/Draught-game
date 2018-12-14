#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QToolBar, QLabel, QAction, QSizePolicy, QWidget, QGridLayout, QDialog, QPushButton
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QSize
from PyQt5.QtGui import QPainter, QColor, QFont
import sys, random

### Class to get useful information about the current ai moving such as its previous position or its actual one and the opportunity for each movement
class AiData():
    def __init__(self):
        self.oldX = 0
        self.oldY = 0
        self.curX = 0
        self.curY = 0
        self.opportunity = 0

### Class tha will handle the simulation of a min max algorithm and retrieve the best possible move dor a piece
class Ai():
    def __init__(self):
        ### The depth of the min max algorithm, the deeper it goes the stronger that AI will be
        self.depth = 1


    ### Get all data of each pawn on the current board
    def updatePawn(self, boardData):
        self.board = boardData
        self.AiPawn = []
        self.PlayerPawn = []
        nbrOfPawn = 0
        for i in range(8):
            for j in range(8):
                if boardData[j][i].belongToPlayer == 2:
                    self.AiPawn.append(boardData[j][i])
                    nbrOfPawn += 1
        nbrOfPawn = 0
        for x in range(8):
            for y in range(8):
                if boardData[y][x].belongToPlayer == 1:
                    self.PlayerPawn.append(boardData[y][x])
                    nbrOfPawn += 1

    ### Calculate the best move at the end of the simulation (not fully done)
    def evaluate(self, data):
        return (data)

    ### Simulate a movement of a pawn for Player X and calculate its opportuinity
    def simulate(self, x, y, player, king, data):
        data.oldX = x
        data.oldY = y


        if (y - 1 >= 0 and x + 1 <= 7) and (king == True or player == 2):
            if self.board[x + 1][y - 1].belongToPlayer == (1 if player == 2 else 1):
                if x + 2 <= 7 and y - 2 >= 0 and self.board[x + 2][y - 2].belongToPlayer == 0:
                    data.curX = x + 2
                    data.curY = y - 2
                    data.opportunity += 50
            elif self.board[x + 1][y - 1].belongToPlayer == 0:
                if (data.opportunity < 50):
                    data.curX = x + 1
                    data.curY = y - 1
                    data.opportunity += 2
        if (y - 1 >= 0 and x - 1 >= 0) and (king == True or player == 2):
            if self.board[x - 1][y - 1].belongToPlayer == (1 if player == 2 else 1):
                if x - 2 >= 0 and y - 2 >= 0 and self.board[x - 2][y - 2].belongToPlayer == 0:
                    data.curX = x - 2
                    data.curY = y - 2
                    data.opportunity += 50
            elif self.board[x - 1][y - 1].belongToPlayer == 0:
                if (data.opportunity < 50):
                    data.curX = x - 1
                    data.curY = y - 1
                    data.opportunity += 2



        if (y + 1 <= 7 and x + 1 <= 7) and (king == True or player == 1):
            if self.board[x + 1][y + 1].belongToPlayer == (1 if player == 2 else 1):
                if x + 2 <= 7 and y + 2 <= 7 and self.board[x + 2][y + 2].belongToPlayer == 0:
                    data.curX = x + 2
                    data.curY = y + 2
                    data.opportunity += 50
            elif self.board[x + 1][y + 1].belongToPlayer == 0:
                if (data.opportunity < 50):
                    data.curX = x + 1
                    data.curY = y + 1
                    data.opportunity += 2
        if (y + 1 <= 7 and x - 1 >= 0) and (king == True or player == 1):
            if self.board[x - 1][y + 1].belongToPlayer == (1 if player == 2 else 1):
                if x - 2 >= 0 and y + 2 <= 7 and self.board[x - 2][y + 2].belongToPlayer == 0:
                    data.curX = x - 2
                    data.curY = y + 2
                    data.opportunity += 50
            elif self.board[x - 1][y + 1].belongToPlayer == 0:
                if (data.opportunity < 50):
                    data.curX = x - 1
                    data.curY = y + 1
                    data.opportunity += 2


    ### Remove the last simulated move (not used)
    def removeLastMove(self, pawn, data):
        self.board[data.curX][data.curY].belongToPlayer = 0
        self.board[data.oldX][data.oldY].belongToPlayer = 2

    ### Retrieve the best possible move for the ai's opponent taking the ai previous move into account
    def minV(self, depth, prevData):
        finalData = AiData()
        finalData.opportunity = 1000000000
        if (depth == 0):
            ev = self.evaluate(prevData)
            return ev
        for pawn in self.PlayerPawn:
            data = AiData()
            self.simulate(pawn.x, pawn.y, pawn.belongToPlayer, pawn.isKing, data)
            val = self.maxV(depth - 1, data)
            if val.opportunity < finalData.opportunity:
                finalData = val
            #self.removeLastMove(pawn, data)
        return finalData

    ### Retrieve the best possible move for the ai the oppenent previous move into account
    def maxV(self, depth, prevData):
        finalData = AiData()
        finalData.opportunity = -1000000000
        if (depth == 0):
            ev = self.evaluate(prevData)
            return ev
        for pawn in self.AiPawn:
            data = AiData()
            self.simulate(pawn.x, pawn.y, pawn.belongToPlayer, pawn.isKing, data)
            val = self.minV(depth - 1, data)
            if val.opportunity > finalData.opportunity:
                finalData = val
        return finalData

    ### Launch the simulation and return the best move for the ai
    def defineBest(self):

        i = self.maxV(self.depth, None)
        return i

### Class that contain data about pawn, what position they have, to who they belong, if they are king etc
class Pawn():
    def __init__(self, x, y, player):
        super().__init__()
        self.x = x
        self.y = y
        self.belongToPlayer = player
        self.selected = False
        self.moveAvailable = False
        self.isKing = False

    ### Retrieve who own the pawn
    def getPlayer(self):
        return self.belongToPlayer


### Information about the player
class Player():
    def __init__(self, player):
        super().__init__()
        ### Player 1 or 2
        self.player = player
        ### Number of pawn left
        self.pawnLeft = 12
        ### Number of pawn killed
        self.pawnKilled = 0

### Class that contains data about the board of the game
class BoardData():
    def __init__(self):
        super().__init__()
        self.initData()

    ### Create arrays that will contain the data of each square of the board
    def initData(self):
        self.boardData = [[0 for x in range(8)] for y in range(8)]

    ### Create pawn for player x at position x and y
    def createPawn(self, x, y, player):
        self.boardData[x][y] = player
        return (Pawn(x, y, player))

    ### Make the move for the pawn of player X
    def movePawn(self, x, y, player, newX, newY, newP):
        self.boardData[x][y].x = newX
        self.boardData[x][y].y = newY
        self.boardData[x][y].belongToPlayer = 0
        self.boardData[newX][newY].isKing = self.boardData[x][y].isKing
        self.boardData[x][y].isKing = False
        self.boardData[newX][newY].x = newX
        self.boardData[newX][newY].y = newY
        self.boardData[newX][newY].belongToPlayer = newP

    ### Delete all GUI information after a move
    def clearBoard(self):
        for i in range(8):
            for j in range(8):
                self.boardData[j][i].moveAvailable = False
                self.boardData[j][i].selected = False

    ### Generate every pawn for each player
    def setupBoardData(self, x, y):
        for i in range(y):
            for j in range(x):
                self.boardData[j][i] = self.createPawn(0, 0, 0)

        self.boardData[0][0] = self.createPawn(0, 0, 0)
        self.boardData[1][0] = self.createPawn(1, 0, 1)
        self.boardData[3][0] = self.createPawn(3, 0, 1)
        self.boardData[5][0] = self.createPawn(5, 0, 1)
        self.boardData[7][0] = self.createPawn(7, 0, 1)
        self.boardData[0][1] = self.createPawn(0, 1, 1)
        self.boardData[2][1] = self.createPawn(2, 1, 1)
        self.boardData[4][1] = self.createPawn(4, 1, 1)
        self.boardData[6][1] = self.createPawn(6, 1, 1)
        self.boardData[1][2] = self.createPawn(1, 2, 1)
        self.boardData[3][2] = self.createPawn(3, 2, 1)
        self.boardData[5][2] = self.createPawn(5, 2, 1)
        self.boardData[7][2] = self.createPawn(7, 2, 1)

        self.boardData[0][7] = self.createPawn(0, 7, 2)
        self.boardData[2][7] = self.createPawn(2, 7, 2)
        self.boardData[4][7] = self.createPawn(4, 7, 2)
        self.boardData[6][7] = self.createPawn(6, 7, 2)
        self.boardData[1][6] = self.createPawn(1, 6, 2)
        self.boardData[3][6] = self.createPawn(3, 6, 2)
        self.boardData[5][6] = self.createPawn(5, 6, 2)
        self.boardData[7][6] = self.createPawn(7, 6, 2)
        self.boardData[0][5] = self.createPawn(0, 5, 2)
        self.boardData[2][5] = self.createPawn(2, 5, 2)
        self.boardData[4][5] = self.createPawn(4, 5, 2)
        self.boardData[6][5] = self.createPawn(6, 5, 2)
        # print(self.boardData[0][0], self.boardData[0][1], self.boardData[0][2])

### Class that will display who is the winner of the game
class WinnerWindow(QDialog):
    def __init__(self, winner):
        super().__init__()

        grid = QGridLayout()

        boldFont = QFont()
        boldFont.setBold(True)

        winnerLabel = QLabel(winner + " won the game ! Congratulations, woo woo wooo !!")
        grid.addWidget(winnerLabel, 0, 0)

        b1 = QPushButton("Restart the game", self)
        b1.clicked.connect(self.restart)
        grid.addWidget(b1, 1, 0)

        self.setLayout(grid)
        self.setWindowTitle("And we have a winner !")

    ### Set the draught class
    def setDraught(self, draught):
        self.draught = draught

    ### Restart the game
    def restart(self):
        self.draught.resetGame()
        self.close()

### Main class that will launch the game
class Draught(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        ### Instantitate the board class
        self.tboard = Board(self)
        self.tboard.setDraught(self)
        self.setCentralWidget(self.tboard)

        ### Create the menu and action
        mainMenu = self.menuBar()
        gameMenu = mainMenu.addMenu(" Game")

        resetAction = QAction("Reset", self)
        resetAction.setShortcut("Ctrl+R")

        pvp = QAction("Player vs Player", self)
        pvp.setShortcut("Ctrl+P")

        pve = QAction("Player vs Ai", self)
        pve.setShortcut("Ctrl+A")

        gameMenu.addAction(resetAction)
        gameMenu.addAction(pvp)
        gameMenu.addAction(pve)

        resetAction.triggered.connect(self.resetGame)
        pvp.triggered.connect(self.playerGame)
        pve.triggered.connect(self.aiGame)


        ### Toolbar that will contain information about the game,
        toolbar = QToolBar()
        toolbar.setAllowedAreas(Qt.RightToolBarArea)
        toolbar.setIconSize(QSize(40, 40))
        toolbar.setFloatable(False)
        toolbar.setMovable(False)

        magicWidget = QWidget()
        self.grid = QGridLayout()

        myFont = QFont()
        myFont.setBold(True)
        myFont.setPixelSize(15)

        ### Label of both player
        self.playerLabel = QLabel("Player 1")
        self.playerLabel.setFont(myFont)
        self.playerTurn = self.turnLabel()

        self.opponentLabel = QLabel("Player 2")
        self.opponentLabel.setFont(myFont)
        self.opponentLabel.setContentsMargins(0, 30, 0, 0)
        self.opponentTurn = self.turnLabel()
        self.opponentTurn.setContentsMargins(0, 30, 0, 0)

        self.playerPawnLeft = QLabel(str(self.tboard.players[0].pawnLeft))
        self.opponentPawnLeft = QLabel(str(self.tboard.players[1].pawnLeft))

        self.playerPawnKilled = QLabel(str(self.tboard.players[0].pawnKilled))
        self.opponentPawnKilled = QLabel(str(self.tboard.players[1].pawnKilled))

        ### Putting all widget in grid
        self.grid.addWidget(self.playerLabel, 0, 0)
        self.grid.addWidget(self.playerTurn, 0, 1)
        self.grid.addWidget(self.remainingLabel(), 1, 0)
        self.grid.addWidget(self.playerPawnLeft, 1, 1)
        self.grid.addWidget(self.killedLabel(), 2, 0)
        self.grid.addWidget(self.playerPawnKilled, 2, 1)

        self.grid.addWidget(self.opponentLabel, 3, 0)
        self.grid.addWidget(self.opponentTurn, 3, 1)
        self.grid.addWidget(self.remainingLabel(), 4, 0)
        self.grid.addWidget(self.opponentPawnLeft, 4, 1)
        self.grid.addWidget(self.killedLabel(), 5, 0)
        self.grid.addWidget(self.opponentPawnKilled, 5, 1)

        magicWidget.setLayout(self.grid)
        ###Putting the grid in a toolbar
        toolbar.addWidget(magicWidget)

        ### Update the label every turn
        self.updateTurnLabel()

        self.addToolBar(Qt.RightToolBarArea, toolbar)

        self.resize(550, 400)
        self.center()
        self.setWindowTitle('Draught')
        self.show()

    ### Reset the game
    def resetGame(self):
        self.tboard.initBoard()
        self.updatePawnLeft(0)
        self.updatePawnLeft(1)
        self.updatePawnKilled(0)
        self.updatePawnKilled(1)
        self.updateTurnLabel()
        self.update()

    ### Set up the player vs player mode
    def playerGame(self):
        self.resetGame()
        self.tboard.aiActivated = False

    ### Set up the player vs ai mode
    def aiGame(self):
        self.resetGame()
        self.tboard.aiActivated = True

    ### Display who won the game
    def displayWinner(self, nextTurnPlayer):
        self.update()
        if (nextTurnPlayer == 0):
            winner = "Player 2"
        elif (nextTurnPlayer == 1):
            winner = "Player 1"
        self.winnerWindow = WinnerWindow(winner)
        self.winnerWindow.setDraught(self)
        self.winnerWindow.exec()

    ### Displaye who is the current turn
    def turnLabel(self):
        label = QLabel("Your turn !")
        label.setStyleSheet('color: #c20d00')
        return label

    ### Display the number of remaining pawn
    def remainingLabel(self):
        return QLabel("Remaining : ")

    ### Display the number of killed pawn
    def killedLabel(self):
        return QLabel("Killed : ")

    ### Update the number of pawn left
    def updatePawnLeft(self, player):
        if (player == 0):
            self.playerPawnLeft.setText(str(self.tboard.players[0].pawnLeft))
        elif (player == 1):
            self.opponentPawnLeft.setText(str(self.tboard.players[1].pawnLeft))
        self.update()

    ### Update the number of pawn killed
    def updatePawnKilled(self, player):
        if (player == 0):
            self.playerPawnKilled.setText(str(self.tboard.players[0].pawnKilled))
        elif (player == 1):
            self.opponentPawnKilled.setText(str(self.tboard.players[1].pawnKilled))
        self.update()

    ### Update the turn of player
    def updateTurnLabel(self):
        if (self.tboard.currentPlayer == 1):
            self.playerTurn.setText("Your turn !")
            self.opponentTurn.setText("")
        elif (self.tboard.currentPlayer == 2):
            self.opponentTurn.setText("Your turn !")
            self.playerTurn.setText("")
        self.update()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

### Class that will manage the display of the board and the behaviour of the game
class Board(QFrame):
    ### Size of the board
    BoardWidth = 8
    BoardHeight = 8

    def __init__(self, parent):
        super().__init__(parent)
        self.aiActivated = False
        self.initBoard()

    ### Initiliaze all data for the board
    def initBoard(self):
        self.timer = QBasicTimer()
        ### Set the first player
        self.currentPlayer = 1
        ### Setup ai
        self.Ai = Ai()
        ### Check if the game is over
        self.gameFinished = False
        ### Check wich pawn is selected
        self.pawnSelected = False
        ### Check if the player can do other move
        self.forced = False
        ### Get the selected pawn pos
        self.selectedX = 0
        self.selectedY = 0
        ### Get the selected move
        self.curX = 0
        self.curY = 0
        ### Setup the board
        self.board = []
        self.boardData = BoardData()
        self.boardData.setupBoardData(Board.BoardWidth, Board.BoardHeight)
        ### Create players
        self.players = []
        self.players.append(Player(1))
        self.players.append(Player(2))
        self.setFocusPolicy(Qt.StrongFocus)

    def setDraught(self, parent):
        self.draught = parent

    ### Get the width of the square
    def squareWidth(self):
        return self.contentsRect().width() // Board.BoardWidth

    ### Get the height of the square
    def squareHeight(self):
        return self.contentsRect().height() // Board.BoardHeight

    ### Paint event that will draw the board
    def paintEvent(self, event):
        ### The painter
        painter = QPainter(self)
        ### The rectangle
        rect = self.contentsRect()
        boardTop = rect.bottom() - Board.BoardHeight * self.squareHeight()
        ### Draw every square of the board
        for i in range(Board.BoardHeight):
            for j in range(Board.BoardWidth):
                self.drawSquare(painter, rect.left() + j * self.squareWidth(), boardTop + i * self.squareHeight(),
                                (i + j) % 2)
                if (self.boardData.boardData[j][i].selected == True):
                    self.drawSquare(painter, rect.left() + j * self.squareWidth(), boardTop + i * self.squareHeight(),
                                    2)
                if (self.boardData.boardData[j][i].moveAvailable == True):
                    self.drawSquare(painter, rect.left() + j * self.squareWidth(),
                                    boardTop + i * self.squareHeight(),
                                    2)
                if (self.boardData.boardData[j][i].getPlayer() == 1):
                    self.drawPawn(painter, rect.left() + j * self.squareWidth(), boardTop + i * self.squareHeight(), 0,
                                  self.boardData.boardData[j][i].isKing)
                if (self.boardData.boardData[j][i].getPlayer() == 2):
                    self.drawPawn(painter, rect.left() + j * self.squareWidth(), boardTop + i * self.squareHeight(), 1,
                                  self.boardData.boardData[j][i].isKing)

    ### Method that will draw Square
    def drawSquare(self, painter, x, y, colorIndex):
        colorTable = [0x514D5B, 0xFFFFFF, 0x7F5579, 0xFF0000]

        color = QColor(colorTable[colorIndex])
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2,
                         self.squareHeight() - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
                         x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1,
                         y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)

    ### Function that will draw pawn
    def drawPawn(self, painter, x, y, colorIndex, isKing=False):
        colorTable = [0xC1442E, 0xF6CD37]

        color = QColor(colorTable[colorIndex])
        painter.setBrush(color)
        painter.drawEllipse(x, y, self.squareWidth(), self.squareHeight())
        painter.setBrush(Qt.green)
        if isKing == True:
            painter.setPen(color.lighter())
            painter.drawEllipse(x, y, self.squareWidth() / 2, self.squareHeight() / 2)


    ### Check if a move can kill a pawn
    def killAvailable(self, x , y):
        if self.boardData.boardData[x][y].isKing == True or self.currentPlayer == 1:
            if x + 1 <= 7 and y + 1 <= 7:
                if self.boardData.boardData[x + 1][y + 1].belongToPlayer == (2 if self.currentPlayer == 1 else 1):
                    if x + 2 <= 7 and y + 2 <= 7 and self.boardData.boardData[x + 2][y + 2].belongToPlayer == 0:
                        return True
            if x - 1 >= 0 and y + 1 <= 7:
                if self.boardData.boardData[x - 1][y + 1].belongToPlayer == (2 if self.currentPlayer == 1 else 1):
                    if x - 2 >= 0 and y + 2 <= 7 and self.boardData.boardData[x - 2][y + 2].belongToPlayer == 0:
                        return True

        if self.boardData.boardData[x][y].isKing == True or self.currentPlayer == 2:
            if x + 1 <= 7 and y - 1 >= 0:
                if self.boardData.boardData[x + 1][y - 1].belongToPlayer == (2 if self.currentPlayer == 1 else 1):
                    if x + 2 <= 7 and y - 2 >= 0 and self.boardData.boardData[x + 2][y - 2].belongToPlayer == 0:
                        return True
            if x - 1 >= 0 and y - 1 >= 0:
                if self.boardData.boardData[x - 1][y - 1].belongToPlayer == (2 if self.currentPlayer == 1 else 1):
                    if x - 2 >= 0 and y - 2 >= 0 and self.boardData.boardData[x - 2][y - 2].belongToPlayer == 0:
                        return True
        return False

    ### Define if the next ove can kill
    def defineKillingMove(self, x , y):
        if self.boardData.boardData[x][y].isKing == True or self.currentPlayer == 1:
            if x + 1 <= 7 and y + 1 <= 7:
                if self.boardData.boardData[x + 1][y + 1].belongToPlayer == (2 if self.currentPlayer == 1 else 1):
                    if x + 2 <= 7 and y + 2 <= 7 and self.boardData.boardData[x + 2][y + 2].belongToPlayer == 0:
                        self.boardData.boardData[x + 2][y + 2].moveAvailable = True
            if x - 1 >= 0 and y + 1 <= 7:
                if self.boardData.boardData[x - 1][y + 1].belongToPlayer == (2 if self.currentPlayer == 1 else 1):
                    if x - 2 >= 0 and y + 2 <= 7 and self.boardData.boardData[x - 2][y + 2].belongToPlayer == 0:
                        self.boardData.boardData[x - 2][y + 2].moveAvailable = True

        if self.boardData.boardData[x][y].isKing == True or self.currentPlayer == 2:
            if x + 1 <= 7 and y - 1 >= 0:
                if self.boardData.boardData[x + 1][y - 1].belongToPlayer == (2 if self.currentPlayer == 1 else 1):
                    if x + 2 <= 7 and y - 2 >= 0 and self.boardData.boardData[x + 2][y - 2].belongToPlayer == 0:
                        self.boardData.boardData[x + 2][y - 2].moveAvailable = True
            if x - 1 >= 0 and y - 1 >= 0:
                if self.boardData.boardData[x - 1][y - 1].belongToPlayer == (2 if self.currentPlayer == 1 else 1):
                    if x - 2 >= 0 and y - 2 >= 0 and self.boardData.boardData[x - 2][y - 2].belongToPlayer == 0:
                        self.boardData.boardData[x - 2][y - 2].moveAvailable = True

    ### Check if the the pawn can move in direction
    def defineAvailableMove(self, x, y):

        if self.boardData.boardData[x][y].isKing == True or self.currentPlayer == 1:
            if x + 1 <= 7 and y + 1 <= 7:
                if self.boardData.boardData[x + 1][y + 1].belongToPlayer == (2 if self.currentPlayer == 1 else 1):
                    if x + 2 <= 7 and y + 2 <= 7 and self.boardData.boardData[x + 2][y + 2].belongToPlayer == 0:
                        self.boardData.boardData[x + 2][y + 2].moveAvailable = True
                elif self.boardData.boardData[x + 1][y + 1].belongToPlayer == (1 if self.currentPlayer == 1 else 2):
                    self.boardData.boardData[x + 1][y + 1].moveAvailable = False
                else:
                    self.boardData.boardData[x + 1][y + 1].moveAvailable = True
            if x - 1 >= 0 and y + 1 <= 7:
                if self.boardData.boardData[x - 1][y + 1].belongToPlayer == (2 if self.currentPlayer == 1 else 1):
                    if x - 2 >= 0 and y + 2 <= 7 and self.boardData.boardData[x - 2][y + 2].belongToPlayer == 0:
                        self.boardData.boardData[x - 2][y + 2].moveAvailable = True
                elif self.boardData.boardData[x - 1][y + 1].belongToPlayer == (1 if self.currentPlayer == 1 else 2):
                    self.boardData.boardData[x - 1][y + 1].moveAvailable = False
                else:
                    self.boardData.boardData[x - 1][y + 1].moveAvailable = True

        if self.boardData.boardData[x][y].isKing == True or self.currentPlayer == 2:
            if x + 1 <= 7 and y - 1 >= 0:
                if self.boardData.boardData[x + 1][y - 1].belongToPlayer == (2 if self.currentPlayer == 1 else 1):
                    if x + 2 <= 7 and y - 2 >= 0 and self.boardData.boardData[x + 2][y - 2].belongToPlayer == 0:
                        self.boardData.boardData[x + 2][y - 2].moveAvailable = True
                elif self.boardData.boardData[x + 1][y - 1].belongToPlayer == (1 if self.currentPlayer == 1 else 2):
                    self.boardData.boardData[x + 1][y - 1].moveAvailable = False
                else:
                    self.boardData.boardData[x + 1][y - 1].moveAvailable = True
            if x - 1 >= 0 and y - 1 >= 0:
                if self.boardData.boardData[x - 1][y - 1].belongToPlayer == (2 if self.currentPlayer == 1 else 1):
                    if x - 2 >= 0 and y - 2 >= 0 and self.boardData.boardData[x - 2][y - 2].belongToPlayer == 0:
                        self.boardData.boardData[x - 2][y - 2].moveAvailable = True
                elif self.boardData.boardData[x - 1][y - 1].belongToPlayer == (1 if self.currentPlayer == 1 else 2):
                    self.boardData.boardData[x - 1][y - 1].moveAvailable = False
                else:
                    self.boardData.boardData[x - 1][y - 1].moveAvailable = True

    ### Kill the pawn after a killing move move, return true a a pawn was killed
    def removePawn(self, oldX, oldY, x, y):

        killCheck = False
        cptX = oldX
        cptY = oldY

        while cptX != x:
            if self.boardData.boardData[cptX][cptY].belongToPlayer == (2 if self.currentPlayer == 1 else 1):
                playerHurted = self.boardData.boardData[cptX][cptY].belongToPlayer - 1
                self.players[playerHurted].pawnLeft -= 1
                self.players[self.currentPlayer - 1].pawnKilled += 1
                self.boardData.boardData[cptX][cptY].belongToPlayer = 0
                self.update()
                self.draught.updatePawnLeft(playerHurted)
                self.draught.updatePawnKilled(self.currentPlayer - 1)
                killCheck = True
                if (self.players[playerHurted].pawnLeft == 0):
                    self.gameFinished = True
            if cptX < x:
                cptX += 1
            else:
                cptX -= 1
            if cptY < y:
                cptY += 1
            else:
                cptY -= 1
        return killCheck

    ### The mouse pressed event
    def mousePressEvent(self, event):
        ### Check if the game is finished
        if self.gameFinished == True:
            return
        ### Get the position where the click was and check if pawn was previously selected, allowing the pawn to move
        if event.button() == Qt.LeftButton & self.pawnSelected == True:
            x = int(event.pos().x() / self.squareWidth())
            y = int(event.pos().y() / self.squareHeight())

            ### End the turn if player is not forced to play
            if x == self.selectedX and y == self.selectedY and self.forced == False:
                self.boardData.clearBoard()
                self.pawnSelected = False
            ###check if a move is available
            if self.boardData.boardData[x][y].moveAvailable == True:
                self.boardData.movePawn(self.selectedX, self.selectedY, 1, x, y, self.currentPlayer)
                self.boardData.boardData[self.selectedX][self.selectedY].selected = False
                killCheck = self.removePawn(self.selectedX, self.selectedY, x, y)

                self.boardData.clearBoard()
                ### Check if multikill is available
                if (self.killAvailable(x, y) == True and killCheck == True):
                    self.forced = True
                    self.selectedX = x
                    self.selectedY = y
                    self.defineKillingMove(self.selectedX, self.selectedY)
                    self.boardData.boardData[x][y].selected = True
                else:
                    ### Setup the next player turn
                    self.pawnSelected = False
                    if (self.currentPlayer == 1):
                        if y == 7:
                            self.boardData.boardData[x][y].isKing = True
                        self.currentPlayer = 2
                        ### Play the ai turn if ai is activated
                        if self.aiActivated is True and self.gameFinished == False:
                            self.Ai.updatePawn(self.boardData.boardData)
                            ai = self.Ai.defineBest()
                            self.currentPlayer = 2
                            self.boardData.movePawn(ai.oldX, ai.oldY, 1, ai.curX, ai.curY, 2)
                            self.removePawn(ai.oldX, ai.oldY, ai.curX, ai.curY)
                            if ai.curY == 0:
                                self.boardData.boardData[ai.curX][ai.curY].isKing = True
                            self.currentPlayer = 1
                    else:
                        if y == 0:
                            self.boardData.boardData[x][y].isKing = True
                        self.currentPlayer = 1
                    self.forced = False
                    self.draught.updateTurnLabel()
                ### Check if the game is finished
                if self.gameFinished == True:
                    self.draught.displayWinner(self.currentPlayer - 1)
                    return
        ### Click but no pawn selected
        elif event.button() == Qt.LeftButton:
            x = int(event.pos().x() / self.squareWidth())
            y = int(event.pos().y() / self.squareHeight())
            if (self.boardData.boardData[x][y].belongToPlayer == self.currentPlayer):
                self.pawnSelected = True
                self.selectedX = x
                self.selectedY = y
                self.boardData.boardData[x][y].selected = True
                self.defineAvailableMove(x, y)

            ##self.boardData.movePawn(1, 0, 1, x, y, 1)

        self.update()


### Launch the game
if __name__ == '__main__':
    app = QApplication([])
    draught = Draught()
    sys.exit(app.exec_())
