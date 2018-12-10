#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QToolBar, QLabel, QAction, QSizePolicy, QWidget, QGridLayout, QDialog, QPushButton
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QSize
from PyQt5.QtGui import QPainter, QColor, QFont
import sys, random


class Pawn():
    def __init__(self, x, y, player):
        super().__init__()
        self.x = x
        self.y = y
        self.belongToPlayer = player
        self.selected = False
        self.moveAvailable = False
        self.isKing = False

    def getPlayer(self):
        return self.belongToPlayer


class Player():
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.pawnLeft = 12
        self.pawnKilled = 0



class BoardData():
    def __init__(self):
        super().__init__()
        self.initData()

    def initData(self):
        self.boardData = [[0 for x in range(8)] for y in range(8)]
        self.playerPawn = []

    def createPawn(self, x, y, player):
        self.boardData[x][y] = player
        self.playerPawn.append(Pawn(0, 0, 1))
        return (Pawn(x, y, player))

    def movePawn(self, x, y, player, newX, newY, newP):
        self.boardData[x][y].x = newX
        self.boardData[x][y].y = newY
        self.boardData[x][y].belongToPlayer = 0
        self.boardData[newX][newY].isKing = self.boardData[x][y].isKing
        self.boardData[x][y].isKing = False
        self.boardData[newX][newY].belongToPlayer = newP

    def clearBoard(self):
        for i in range(8):
            for j in range(8):
                self.boardData[j][i].moveAvailable = False
                self.boardData[j][i].selected = False

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

    def setDraught(self, draught):
        self.draught = draught

    def restart(self):
        self.draught.resetGame()
        self.close()

class Draught(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.tboard = Board(self)
        self.tboard.setDraught(self)
        self.setCentralWidget(self.tboard)

        mainMenu = self.menuBar()
        gameMenu = mainMenu.addMenu(" Game")

        resetAction = QAction("Reset", self)
        resetAction.setShortcut("Ctrl+R")
        gameMenu.addAction(resetAction)
        gameMenu.triggered.connect(self.resetGame)

        self.statusbar = self.statusBar()
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

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

        self.playerLabel = QLabel("Player")
        self.playerLabel.setFont(myFont)
        self.playerTurn = self.turnLabel()

        self.opponentLabel = QLabel("Opponent")
        self.opponentLabel.setFont(myFont)
        self.opponentLabel.setContentsMargins(0, 30, 0, 0)
        self.opponentTurn = self.turnLabel()
        self.opponentTurn.setContentsMargins(0, 30, 0, 0)

        self.playerPawnLeft = QLabel(str(self.tboard.players[0].pawnLeft))
        self.opponentPawnLeft = QLabel(str(self.tboard.players[1].pawnLeft))

        self.playerPawnKilled = QLabel(str(self.tboard.players[0].pawnKilled))
        self.opponentPawnKilled = QLabel(str(self.tboard.players[1].pawnKilled))

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

        toolbar.addWidget(magicWidget)

        self.updateTurnLabel()

        self.addToolBar(Qt.RightToolBarArea, toolbar)

        self.resize(550, 400)
        self.center()
        self.setWindowTitle('Draught')
        self.show()

    def resetGame(self):
        self.tboard.initBoard()
        self.updatePawnLeft(0)
        self.updatePawnLeft(1)
        self.updatePawnKilled(0)
        self.updatePawnKilled(1)
        self.updateTurnLabel()
        self.update()

    def displayWinner(self, nextTurnPlayer):
        self.update()
        if (nextTurnPlayer == 0):
            winner = "Opponent"
        elif (nextTurnPlayer == 1):
            winner = "Player"
        self.winnerWindow = WinnerWindow(winner)
        self.winnerWindow.setDraught(self)
        self.winnerWindow.exec()

    def turnLabel(self):
        label = QLabel("Your turn !")
        label.setStyleSheet('color: #c20d00')
        return label

    def remainingLabel(self):
        return QLabel("Remaining : ")

    def killedLabel(self):
        return QLabel("Killed : ")

    def updatePawnLeft(self, player):
        if (player == 0):
            self.playerPawnLeft.setText(str(self.tboard.players[0].pawnLeft))
        elif (player == 1):
            self.opponentPawnLeft.setText(str(self.tboard.players[1].pawnLeft))
        self.update()

    def updatePawnKilled(self, player):
        if (player == 0):
            self.playerPawnKilled.setText(str(self.tboard.players[0].pawnKilled))
        elif (player == 1):
            self.opponentPawnKilled.setText(str(self.tboard.players[1].pawnKilled))
        self.update()

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


class Board(QFrame):
    msg2Statusbar = pyqtSignal(str)

    BoardWidth = 8
    BoardHeight = 8

    def __init__(self, parent):
        super().__init__(parent)

        self.initBoard()

    def initBoard(self):
        '''initiates board'''

        self.timer = QBasicTimer()
        self.currentPlayer = 1
        self.gameFinished = False
        self.pawnSelected = False
        self.forced = False
        self.selectedX = 0
        self.selectedY = 0
        self.curX = 0
        self.curY = 0
        self.board = []
        self.boardData = BoardData()
        self.boardData.setupBoardData(Board.BoardWidth, Board.BoardHeight)
        self.players = []
        self.players.append(Player(1))
        self.players.append(Player(2))
        self.setFocusPolicy(Qt.StrongFocus)

    def setDraught(self, parent):
        self.draught = parent

    def shapeAt(self, x, y):
        '''determines shape at the board position'''

        return self.board[(y * Board.BoardWidth) + x]

    def setShapeAt(self, x, y, shape):
        '''sets a shape at the board'''

        self.board[(y * Board.BoardWidth) + x] = shape

    def squareWidth(self):
        '''returns the width of one square'''

        return self.contentsRect().width() // Board.BoardWidth

    def squareHeight(self):
        '''returns the height of one square'''

        return self.contentsRect().height() // Board.BoardHeight

    def paintEvent(self, event):
        '''paints all shapes of the game'''
        painter = QPainter(self)
        rect = self.contentsRect()

        boardTop = rect.bottom() - Board.BoardHeight * self.squareHeight()
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

    def drawSquare(self, painter, x, y, colorIndex):
        '''draws a square of a shape'''

        colorTable = [0x514D5B, 0xFFFFFF, 0x7F5579]

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

    def drawPawn(self, painter, x, y, colorIndex, isKing=False):
        colorTable = [0xC1442E, 0xF6CD37]

        color = QColor(colorTable[colorIndex])
        painter.setBrush(color)
        painter.drawEllipse(x, y, self.squareWidth(), self.squareHeight())
        painter.setBrush(Qt.green)
        if isKing == True:
            painter.setPen(color.lighter())
            painter.drawEllipse(x, y, self.squareWidth() / 2, self.squareHeight() / 2)


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
                ## TODO : mettre pawnLeft à 0
                if (self.players[playerHurted].pawnLeft == 10):
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

    def mousePressEvent(self, event):
        if self.gameFinished == True:
            return
        if event.button() == Qt.LeftButton & self.pawnSelected == True:
            x = int(event.pos().x() / self.squareWidth())
            y = int(event.pos().y() / self.squareHeight())

            if x == self.selectedX and y == self.selectedY and self.forced == False:
                self.boardData.clearBoard()
                self.pawnSelected = False
            if self.boardData.boardData[x][y].moveAvailable == True:
                self.boardData.movePawn(self.selectedX, self.selectedY, 1, x, y, self.currentPlayer)
                self.boardData.boardData[self.selectedX][self.selectedY].selected = False
                killCheck = self.removePawn(self.selectedX, self.selectedY, x, y)
                self.boardData.clearBoard()

                if (self.killAvailable(x, y) == True and killCheck == True):
                    self.forced = True
                    self.selectedX = x
                    self.selectedY = y
                    self.defineKillingMove(self.selectedX, self.selectedY)
                    self.boardData.boardData[x][y].selected = True
                else:
                    self.pawnSelected = False
                    if (self.currentPlayer == 1):
                        if y == 7:
                            self.boardData.boardData[x][y].isKing = True
                        self.currentPlayer = 2
                    else:
                        if y == 0:
                            self.boardData.boardData[x][y].isKing = True
                        self.currentPlayer = 1
                    self.forced = False
                    self.draught.updateTurnLabel()

                if self.gameFinished == True:
                    self.draught.displayWinner(self.currentPlayer - 1)
                    return
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

    def mouseMoveEvent(self, event):
        x = int(event.pos().x() / self.squareWidth())
        y = int(event.pos().y() / self.squareHeight())


if __name__ == '__main__':
    app = QApplication([])
    draught = Draught()
    sys.exit(app.exec_())
