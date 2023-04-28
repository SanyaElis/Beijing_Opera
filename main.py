import random
import sys

from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication


class Tetris(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)

        self.statusbar = self.statusBar()
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        self.tboard.start()

        self.resize(300, 400)
        self.center()
        self.setWindowTitle('Tetris')
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2,
                  (screen.height() - size.height()) // 2)


class Board(QFrame):
    msg2Statusbar = pyqtSignal(str)

    BoardWidth = 15
    BoardHeight = 22
    Speed = 300

    def __init__(self, parent):
        super().__init__(parent)

        self.initBoard()

    def initBoard(self):

        self.curX = 0
        self.curY = 4
        self.curPiece = Shape()
        self.score = 0
        self.board = []

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.randomBoard()

    def shapeAt(self, x, y):
        return self.board[(y * Board.BoardWidth) + x]

    def setShapeAt(self, x, y, shape):
        self.board[(y * Board.BoardWidth) + x] = shape

    def squareWidth(self):
        return self.contentsRect().width() // Board.BoardWidth

    def squareHeight(self):
        return self.contentsRect().height() // Board.BoardHeight

    def start(self):

        self.isStarted = True
        self.score = 0
        self.randomBoard()

        self.msg2Statusbar.emit(str(self.score))

    def paintEvent(self, event):

        painter = QPainter(self)
        rect = self.contentsRect()

        boardTop = rect.bottom() - Board.BoardHeight * self.squareHeight()

        for i in range(Board.BoardHeight):
            for j in range(Board.BoardWidth):
                shape = self.shapeAt(j, Board.BoardHeight - i - 1)

                if shape != Tetrominoe.NoShape:
                    self.drawSquare(painter,
                                    rect.left() + j * self.squareWidth(),
                                    boardTop + i * self.squareHeight(), shape)

    def clearBoard(self):

        for i in range(Board.BoardHeight * Board.BoardWidth):
            self.board.append(Tetrominoe.NoShape)

    def randomBoard(self):
        for i in range(Board.BoardHeight * Board.BoardWidth):
            figure = random.randint(1, 7)
            self.board.append(figure)

    def check_vertical(self, row):
        for i in range(Board.BoardHeight - 2):
            j = i + 1
            number_of_same = 1
            print(self.shapeAt(row, i))
            print(self.shapeAt(row, j))
            while j != Board.BoardHeight - 1 and self.shapeAt(row, i) == self.shapeAt(row, j):
                j += 1
                number_of_same += 1
            if number_of_same >= 3 and self.shapeAt(row, i) != Tetrominoe.NoShape:
                self.score += number_of_same
                while number_of_same > 0:
                    self.setShapeAt(row, i + number_of_same - 1, Tetrominoe.NoShape)
                    number_of_same -= 1

    def check_horizontal(self, col):
        for i in range(Board.BoardWidth - 2):
            j = i + 1
            number_of_same = 1
            print(self.shapeAt(i, col))
            print(self.shapeAt(j, col))
            while j != Board.BoardHeight - 1 and self.shapeAt(i, col) == self.shapeAt(j, col):
                j += 1
                number_of_same += 1
            if number_of_same >= 3 and self.shapeAt(i, col) != Tetrominoe.NoShape:
                self.score += number_of_same
                while number_of_same > 0:
                    self.setShapeAt(i + number_of_same - 1, col, Tetrominoe.NoShape)
                    number_of_same -= 1

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if event.pos().x() < self.BoardWidth * self.squareWidth():
                self.mouse_place_click(event.pos().x(), event.pos().y())
                Board.setShapeAt(self, self.curX, self.curY, random.randint(1, 7))
                self.update()
        elif event.button() == Qt.RightButton:
            self.mouse_place_click(event.pos().x(), event.pos().y())
            print(self.curX, self.curY)
            print(self.shapeAt(self.curX, self.curY))
            self.check_vertical(self.curX)
            self.check_horizontal(self.curY)
            self.update()

    def mouse_place_click(self, x, y):
        c_x = x // self.squareWidth()
        c_y = (self.contentsRect().bottom() - y) // self.squareHeight()
        self.curX = c_x
        self.curY = c_y

    def drawSquare(self, painter, x, y, shape):

        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QColor(colorTable[shape])
        red_color = 0xFF0000

        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2,
                         self.squareHeight() - 2, color)

        if self.curX == x // self.squareWidth() and self.curY + 1 == (
                self.contentsRect().bottom() - y) // self.squareHeight():
            color = QColor(red_color)
            # color.setAlpha(200)
        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
                         x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1,
                         y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)
        painter.drawText(x + 10, y + 20, str(shape))


class Tetrominoe(object):
    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7


class Shape(object):
    coordsTable = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, 0), (0, 0), (0, 0), (0, 0))
    )

    def __init__(self):

        self.coords = [[0, 0] for i in range(4)]
        self.pieceShape = Tetrominoe.NoShape

        self.setShape(Tetrominoe.NoShape)

    def shape(self):
        return self.pieceShape

    def setShape(self, shape):

        table = Shape.coordsTable[shape]

        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]

        self.pieceShape = shape

    def setRandomShape(self):
        self.setShape(random.randint(1, 7))

    def x(self, index):
        return self.coords[index][0]

    def y(self, index):
        return self.coords[index][1]

    def setX(self, index, x):
        self.coords[index][0] = x

    def setY(self, index, y):
        self.coords[index][1] = y


if __name__ == '__main__':
    app = QApplication([])
    tetris = Tetris()
    sys.exit(app.exec_())
