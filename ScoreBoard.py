import Tkinter as tk


class ScoreBoard:
    def __init__(self, window, width, height):
        self.mainWindow = window
        self.canvasWidth = width
        self.canvasHeight = height
        self.canvas = tk.Canvas(self.mainWindow, width=self.canvasWidth, height=self.canvasHeight)
        self.canvas.pack(side=tk.TOP, expand=False, fill='both')
        self.livesTextString = 'Lives: '
        self.pointsTextString = 'Points: '
        self.pointsText = -1
        self.images = []
        self.hearts = []
        self.lives = 1

        self.initPoints()

    def initLives(self, lives):
        self.lives = lives
        self.canvas.create_text(10, self.canvasHeight / 2,
                                anchor="w", font=('Purisa', 12),
                                text=self.livesTextString, fill='black')
        self.drawHearts()

    def drawHearts(self):
        x = 60
        for i in range(0, self.lives):
            heart = tk.PhotoImage(file="Resources/Images/heart.gif")
            self.images += [heart]
            heartID = self.canvas.create_image(x + 10, self.canvasHeight / 2,
                                               anchor="w", image=heart)
            self.hearts.append(heartID)
            x += 22

    def initPoints(self):
        x = self.canvasWidth - 120
        self.canvas.create_text(x, self.canvasHeight / 2,
                                anchor="w", font=('Purisa', 12),
                                text=self.pointsTextString, fill='black')
        x1 = self.canvasWidth - 50
        self.pointsText = self.canvas.create_text(x1, self.canvasHeight / 2, anchor="w",
                                                  font=('Purisa', 13), fill='red')
        self.setPoints(0)

    def setPoints(self, points):
        self.canvas.itemconfig(self.pointsText, text=str(points))

    def decrementLives(self):
        self.canvas.delete(self.hearts.pop())
