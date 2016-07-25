from Game import *

from ScoreBoard import *

window = tk.Tk()

row = 5
col = 10
rad = 10
lives = 3
padw = 70
padh = 10
windowWidth = 500
windowHeight = 650

window.geometry(str(windowWidth) + 'x' + str(windowHeight) + '+200+200')
window.resizable(width=False, height=False)
window.title('BrickBreak')

game = Game(window, windowWidth, 600)
game.populateBricks(col, row, [50, 40, 30, 20, 10])
game.initPaddle(padw, padh)
game.initBall(rad, 4, 4)
game.startGame()

window.mainloop()
