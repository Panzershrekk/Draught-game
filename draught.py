#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
import sys, random


class AiData():
    def __init__(self):
        self.oldX = 0
        self.oldY = 0
        self.curX = 0
        self.curY = 0
        self.opportunity = 0

class Ai():
    def __init__(self):
        self.depth = 1


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

    def evaluate(self, data):
        print(data.opportunity)
        return (data)

    def simulate(self, x, y, player, king, data):
        data.oldX = x
        data.oldY = y


        if y - 1 >= 0 and x + 1 <= 7:
            if self.board[x + 1][y - 1].belongToPlayer == 1:
                if x + 2 <= 7 and y - 2 >= 0 and self.board[x + 2][y - 2].belongToPlayer == 0:
                    #self.board[x + 2][y - 2].belongToPlayer = player
                    data.curX = x + 2
                    data.curY = y - 2
                    data.opportunity += 50
            elif self.board[x + 1][y - 1].belongToPlayer == 0:
                #self.board[x + 1][y - 1].belongToPlayer = player
                data.curX = x + 1
                data.curY = y - 1
                data.opportunity += 2
        if y - 1 >= 0 and x - 1 >= 0:
            if self.board[x - 1][y - 1].belongToPlayer == 1:
                if x - 2 >= 0 and y - 2 >= 0 and self.board[x - 2][y - 2].belongToPlayer == 0:
                    #self.board[x + 2][y - 2].belongToPlayer = player
                    data.curX = x - 2
                    data.curY = y - 2
                    data.opportunity += 50
            elif self.board[x - 1][y - 1].belongToPlayer == 0:
                data.curX = x - 1
                data.curY = y - 1
                data.opportunity += 2



        if y + 1 <= 7 and x + 1 <= 7 and king == True:
            if self.board[x + 1][y + 1].belongToPlayer == 1:
                if x + 2 <= 7 and y + 2 <= 7 and self.board[x + 2][y + 2].belongToPlayer == 0:
                    #self.board[x + 2][y - 2].belongToPlayer = player
                    data.curX = x + 2
                    data.curY = y - 2
                    data.opportunity += 50
            elif self.board[x + 1][y + 1].belongToPlayer == 0:
                #self.board[x + 1][y - 1].belongToPlayer = player
                data.curX = x + 1
                data.curY = y + 1
                data.opportunity += 2
        if y + 1 <= 7 and x - 1 >= 0 and king == True:
            if self.board[x - 1][y + 1].belongToPlayer == 1:
                if x - 2 >= 0 and y + 2 <= 7 and self.board[x - 2][y + 2].belongToPlayer == 0:
                    #self.board[x + 2][y - 2].belongToPlayer = player
                    data.curX = x - 2
                    data.curY = y + 2
                    data.opportunity += 50
            elif self.board[x - 1][y + 1].belongToPlayer == 0:
                data.curX = x - 1
                data.curY = y + 1
                data.opportunity += 2



    def removeLastMove(self, pawn, data):
        self.board[data.curX][data.curY].belongToPlayer = 0
        self.board[data.oldX][data.oldY].belongToPlayer = 2

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

    def defineBest(self):

        i = self.maxV(self.depth, None)
        #self.board[i.curX][i.curY].belongToPlayer = 2
        #self.board[i.oldX][i.oldY].belongToPlayer = 0
        print(i.oldX, i.oldY, i.curX, i.curY)
        return i

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
        self.boardData[newX][newY].x = newX
        self.boardData[newX][newY].y = newY
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
        self.timer = QBasicTimer()
        self.currentPlayer = 1
        self.aiActivated = True
        self.Ai = Ai()
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

    def shapeAt(self, x, y):
        return self.board[(y * Board.BoardWidth) + x]

    def setShapeAt(self, x, y, shape):
        self.board[(y * Board.BoardWidth) + x] = shape

    def squareWidth(self):
        return self.contentsRect().width() // Board.BoardWidth

    def squareHeight(self):
        return self.contentsRect().height() // Board.BoardHeight

    def paintEvent(self, event):
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
                self.players[self.boardData.boardData[cptX][cptY].belongToPlayer - 1].pawnLeft -= 1
                self.players[self.currentPlayer - 1].pawnKilled += 1
                self.boardData.boardData[cptX][cptY].belongToPlayer = 0
                killCheck = True

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
                        if self.aiActivated is True:
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
