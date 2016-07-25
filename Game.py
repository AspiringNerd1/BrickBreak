import Tkinter as tk
from random import randint

from ScoreBoard import ScoreBoard


class Game:
    colors = ["magenta", "blue", "green", "yellow", "red"]

    def __init__(self, window, width, height):
        self.mainWindow = window
        self.canvasWidth = width
        self.canvasHeight = height

        self.points = 0
        self.lives = 3

        self.scoreBoard = ScoreBoard(window, width, 50)
        self.scoreBoard.initLives(3)

        self.canvas = tk.Canvas(self.mainWindow, width=self.canvasWidth, height=self.canvasHeight)
        self.canvas.pack(side=tk.TOP, expand=False, fill='both')

        self.mainWindow.bind("<Left>", self.onLeftPress)
        self.mainWindow.bind("<Right>", self.onRightPress)
        self.mainWindow.bind("<Return>", self.onEnterPress)

        self.paddle = self.ball = self.velocityX = self.bricks = \
            self.velocityY = self.radius = self.pressAnyKey = -1
        self.pauseBall = True

    def populateBricks(self, cols, rows, rowPoints):
        self.bricks = rows * cols
        for i in range(0, rows):
            for j in range(0, cols):
                width = (self.canvasWidth / cols)
                height = 25
                brickId = self.canvas.create_rectangle(j * width, i * height, (j + 1) * width,
                                                       (i + 1) * height, fill=self.colors[i],
                                                       width=2)
                self.canvas.itemconfig(brickId, tags=str(rowPoints[i]))

    def initPaddle(self, paddleWidth, paddleHeight):
        paddleX = (self.canvasWidth - paddleWidth) / 2
        paddleY = self.canvasHeight - 30
        self.paddle = self.canvas.create_rectangle(paddleX, paddleY, paddleX + paddleWidth,
                                                   paddleY + paddleHeight, fill="black")

    def initBall(self, radius, velocityX, velocityY):
        self.radius = radius
        self.velocityX = velocityX
        self.velocityY = velocityY
        ballX = (self.canvasWidth - radius) / 2
        ballY = (self.canvasHeight - radius) / 2
        self.ball = self.canvas.create_oval(ballX, ballY, ballX + radius, ballY + radius,
                                            fill="black")

    def onLeftPress(self, event):
        if self.canvas.coords(self.paddle)[0] >= 15:
            self.canvas.move(self.paddle, -10, 0)

    def onRightPress(self, event):
        if self.canvas.coords(self.paddle)[2] <= self.canvasWidth - 15:
            self.canvas.move(self.paddle, 10, 0)

    def onEnterPress(self, event):
        if self.startBall():
            return

    def startBall(self):
        if self.pauseBall:
            self.pauseBall = False
            self.moveBall()
            return True
        return False

    def moveBall(self):
        if self.pauseBall:
            return

        self.canvas.delete(self.pressAnyKey)
        ballCoordinates = self.canvas.coords(self.ball)
        if ballCoordinates[0] <= 15 or ballCoordinates[2] >= (self.canvasWidth - 15):
            self.velocityX = -self.velocityX
        if ballCoordinates[3] >= self.canvasHeight - 5:
            self.lives -= 1
            self.scoreBoard.decrementLives()
            self.stopBall()

        self.canvas.move(self.ball, self.velocityX, self.velocityY)
        self.checkCollision()
        self.canvas.after(10, self.moveBall)

    def checkCollision(self):
        ballCoordinates = self.canvas.coords(self.ball)

        if ballCoordinates.__len__() != 4:
            return

        overlap = self.canvas.find_overlapping(ballCoordinates[0], ballCoordinates[1],
                                               ballCoordinates[2], ballCoordinates[3])

        if len(overlap) > 1:
            self.velocityY = -self.velocityY
            self.velocityX += 0.5 * randint(-1, 1)
        if len(overlap) > 1:
            for i in overlap:
                if i != self.ball and i != self.paddle:
                    self.points += int(self.canvas.gettags(i)[0])
                    self.scoreBoard.setPoints(self.points)
                    self.canvas.delete(i)
                    self.bricks -= 1
                    self.checkGameOver()

    def displayPressAnyKey(self):
        x = self.canvasWidth / 2
        y = self.canvasHeight / 2 + 30
        self.pressAnyKey = self.canvas.create_text(x, y, font=("Roboto", 12),
                                                   text='Press Enter to start', fill="brown")

    def stopBall(self):
        self.pauseBall = True
        ballX = (self.canvasWidth - self.radius) / 2
        ballY = (self.canvasHeight - self.radius) / 2
        self.canvas.coords(self.ball, ballX, ballY, ballX + self.radius, ballY + self.radius)
        self.velocityY = abs(self.velocityY)
        self.displayPressAnyKey()
        self.checkGameOver()

    def checkGameOver(self):
        if self.lives == 0 or self.bricks == 0:
            self.endGame()

    def endGame(self):
        self.canvas.delete(self.ball)
        self.canvas.itemconfig(self.pressAnyKey, text="Game Over!")
        self.mainWindow.unbind("<Return>")
        self.mainWindow.unbind("<Left>")
        self.mainWindow.unbind("<Right>")

    def startGame(self):
        self.displayPressAnyKey()
