#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
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


class Draught(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)

        mainMenu = self.menuBar()
        gameMenu = mainMenu.addMenu(" Game")




        self.statusbar = self.statusBar()
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)


        self.resize(400, 400)
        self.center()
        self.setWindowTitle('Draught')
        self.show()

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
        self.pawnSelected = False
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
                                    3)
                if (self.boardData.boardData[j][i].getPlayer() == 1):
                    self.drawPawn(painter, rect.left() + j * self.squareWidth(), boardTop + i * self.squareHeight(), 0,
                                  self.boardData.boardData[j][i].isKing)
                if (self.boardData.boardData[j][i].getPlayer() == 2):
                    self.drawPawn(painter, rect.left() + j * self.squareWidth(), boardTop + i * self.squareHeight(), 1,
                                  self.boardData.boardData[j][i].isKing)

    def drawSquare(self, painter, x, y, colorIndex):
        '''draws a square of a shape'''

        colorTable = [0x0000FF, 0xFFFFFF, 0xFF00FF, 0xFF0000]

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
        colorTable = [0xFF0000, 0xFFFF00]

        color = QColor(colorTable[colorIndex])
        painter.setBrush(color)
        painter.drawEllipse(x, y, self.squareWidth(), self.squareHeight())
        painter.setBrush(Qt.green)
        if isKing == True:
            painter.setPen(color.lighter())
            painter.drawEllipse(x, y, self.squareWidth() / 2, self.squareHeight() / 2)

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

        cptX = oldX
        cptY = oldY

        while cptX != x:
            if self.boardData.boardData[cptX][cptY].belongToPlayer == (2 if self.currentPlayer == 1 else 1):
                self.players[self.boardData.boardData[cptX][cptY].belongToPlayer - 1].pawnLeft -= 1
                self.players[self.currentPlayer - 1].pawnKilled += 1
                self.boardData.boardData[cptX][cptY].belongToPlayer = 0

            if cptX < x:
                cptX += 1
            else:
                cptX -= 1
            if cptY < y:
                cptY += 1
            else:
                cptY -= 1

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton & self.pawnSelected == True:
            x = int(event.pos().x() / self.squareWidth())
            y = int(event.pos().y() / self.squareHeight())

            if x == self.selectedX and y == self.selectedY:
                self.boardData.clearBoard()
                self.pawnSelected = False
            if self.boardData.boardData[x][y].moveAvailable == True:
                self.boardData.movePawn(self.selectedX, self.selectedY, 1, x, y, self.currentPlayer)
                self.boardData.boardData[self.selectedX][self.selectedY].selected = False
                self.removePawn(self.selectedX, self.selectedY, x, y)
                self.boardData.clearBoard()
                self.pawnSelected = False
                if (self.currentPlayer == 1):
                    if y == 7:
                        self.boardData.boardData[x][y].isKing = True
                    self.currentPlayer = 2
                else:
                    if y == 0:
                        self.boardData.boardData[x][y].isKing = True
                    self.currentPlayer = 1
                print(self.players[0].pawnKilled, self.players[0].pawnLeft)
                print(self.players[1].pawnKilled, self.players[1].pawnLeft)

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
