import pygame as pg
pg.font.init()
pg.init()

global width, height, widthInPixels, heightInPixels

width = 17
height = 5
widthInPixels = width * 32
heightInPixels = height * 32
win = pg.display.set_mode((200,200))
myFont = pg.font.SysFont("Times New Roman", 18)

tile_start = pg.image.load("Start.png")
tile_target = pg.image.load("Target.png")
tile_blank = pg.image.load("Blank.png")
tile_wall = pg.image.load("Wall.png")
tile_analyzing = pg.image.load("Analyzing.png")
tile_analyzed = pg.image.load("Analyzed.png")
tile_path = pg.image.load("Path.png")
tile_current = pg.image.load("Current.png")
tile_slow = pg.image.load("Slow.png")
d = pg.image.load("D.png")
aStar = pg.image.load("AStar.png")
delete = pg.image.load("Delete.png")
play = pg.image.load("Play.png")
menu = pg.image.load("Menu.png")
slider = pg.image.load("Slider.png")
exit = pg.image.load("Exit.png")


class Tile():
    def __init__(self, posX, posY):
        self.currentTile = tile_blank
        self.x = posX
        self.y = posY
        self.score = 1
        self.tileThatGotIt = None

    def turnToStart(self):
        self.currentTile = tile_start

    def turnToTarget(self):
        self.currentTile = tile_target

    def turnToWall(self):
        if self.currentTile != tile_start and self.currentTile != tile_target:
            self.currentTile = tile_wall

    def turnToBlank(self):
        if self.currentTile != tile_start and self.currentTile != tile_target:
            self.score = 1
            self.currentTile = tile_blank

    def turnToAnalyzing(self):
        if self.currentTile != tile_start and self.currentTile != tile_target:
            self.currentTile = tile_analyzing

    def turnToAnalyzed(self):
        if self.currentTile != tile_start and self.currentTile != tile_target:
            self.currentTile = tile_analyzed

    def turnToPath(self):
        if self.currentTile != tile_start and self.currentTile != tile_target:
            self.currentTile = tile_path

    def turnToCurrent(self):
        if self.currentTile != tile_start and self.currentTile != tile_target:
            self.currentTile = tile_current

    def turnToSlow(self):
        if self.currentTile != tile_start and self.currentTile != tile_target:
            self.score = 2
            self.currentTile = tile_slow

    def reset(self):
        self.currentTile = tile_blank
        self.score = 1

class Button():
    def __init__(self, posX, posY, buttonType):
        self.currentTile = buttonType
        self.x = posX
        self.y = posY

class ToggleButton():
    def __init__(self, posX, posY, t1, t2):
        self.possibleTiles = [t1, t2]
        self.currentTile = t1
        self.x = posX
        self.y = posY

    def toggle(self):
        if self.currentTile == self.possibleTiles[0]:
            self.currentTile = self.possibleTiles[1]
        elif self.currentTile == self.possibleTiles[1]:
            self.currentTile = self.possibleTiles[0]


class Slider():
    def __init__(self, x, y, type):
        self.x = x
        self.x2 = x + 13
        self.y = y
        self.y2 = y + 13
        self.type = type
        self.clicked = False
        if self.type == 0:
            self.value = int(17 + 0.32 * (self.x - 41))
        if self.type == 1:
            self.value = int(5 + 0.195 * (self.x - 41))


    def updateX(self, diff):
        if diff < 0 and self.x < 42:
            self.x = 42
            self.x2 = 55

        elif diff > 0 and self.x2 > 158:
            self.x = 145
            self.x2 = 158

        self.x += diff
        self.x2 += diff

        if self.type == 0:
            self.value = int(17 + 0.32 * (self.x - 41))
        if self.type == 1:
            self.value = int(5 + 0.195 * (self.x - 41))


def settings(win, ws, hs):
    global width, height, widthInPixels, heightInPixels, run
    settings = True
    win = pg.display.set_mode((200,200))
    posCompare = None
    while settings:
        if ws.value < 17:
            ws.value = 17
        elif ws.value > 50:
            ws.value = 50
        if hs.value < 5:
            hs.value = 5
        elif hs.value > 25:
            hs.value = 25
        widthValue = myFont.render(str(ws.value), 1, (0,0,0))
        heightValue = myFont.render(str(hs.value), 1, (0,0,0))
        win.blit(menu,(0,0))
        win.blit(slider, (ws.x, ws.y))
        win.blit(slider, (hs.x, hs.y))
        win.blit(widthValue, (135, 54))
        win.blit(heightValue, (135, 96))

        pg.display.update()
        for event in pg.event.get():
            pos = pg.mouse.get_pos()
            if event.type == pg.MOUSEBUTTONDOWN:
                if pos[0] > 55 and pos[0] < 145 and pos[1] > 155 and pos[1] < 186:
                    settings = False

                if pos[0] > ws.x and pos[0] < ws.x2 and pos[1] > ws.y and pos[1] < ws.y2:
                    posCompare = pos
                    ws.clicked = True

                if pos[0] > hs.x and pos[0] < hs.x2 and pos[1] > hs.y and pos[1] < hs.y2:
                    posCompare = pos
                    hs.clicked = True

            if event.type == pg.MOUSEMOTION:
                if ws.clicked:
                    ws.updateX(int(pos[0] - posCompare[0]))
                    posCompare = pos
                if hs.clicked:
                    hs.updateX(int(pos[0] - posCompare[0]))
                    posCompare = pos

            if event.type == pg.MOUSEBUTTONUP:
                ws.clicked = False
                hs.clicked = False

            if event.type == pg.QUIT:
                settings = False
                run = False
                pg.quit()

    width = ws.value
    height = hs.value
    widthInPixels = width * 32
    heightInPixels = height * 32
    win = pg.display.set_mode((widthInPixels, heightInPixels + 100))
    return False


def drawBoard(width, height, tiles, wallB, tileB, tileS, tileT, delB, playB, slowB, aB, exitB):
    for i in range(width):
        for j in range(height):
            win.blit(tiles[i][j].currentTile, (tiles[i][j].x * 32, tiles[i][j].y * 32))
    win.blit(wallB.currentTile, (wallB.x*32, wallB.y*32))
    win.blit(tileB.currentTile, (tileB.x*32, tileB.y*32))
    win.blit(tileS.currentTile, (tileS.x*32, tileS.y*32))
    win.blit(tileT.currentTile, (tileT.x*32, tileT.y*32))
    win.blit(delB.currentTile, (delB.x*32, delB.y*32))
    win.blit(playB.currentTile, (playB.x*32, playB.y*32))
    win.blit(slowB.currentTile, (slowB.x*32, slowB.y*32))
    win.blit(aB.currentTile, (aB.x*32, aB.y*32))
    win.blit(exitB.currentTile, (exitB.x*32, exitB.y*32))
def reset(tiles):
    for i in range(width):
        for j in range(height):
            tiles[i][j].reset();
    return None, None
def CalculateScore(start, target, tile):
    gCost = abs(start.x - tile.x) + abs(start.y - tile.y)
    hCost = abs(target.x - tile.x) + abs(target.y - tile.y)
    fCost = (gCost + hCost) * tile.score
    return fCost
def findPathA(start, target, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton):
    delay = 1
    tilesToAnalyze = []
    tileScores = []
    analyzedTiles = []
    path = []
    currentTile = start
    while target not in tilesToAnalyze:
        if currentTile.x == 0:
            if tiles[currentTile.x + 1][currentTile.y] not in tilesToAnalyze and tiles[currentTile.x + 1][currentTile.y] not in analyzedTiles:
                if tiles[currentTile.x + 1][currentTile.y].currentTile != tile_wall:
                    tilesToAnalyze.append(tiles[currentTile.x + 1][currentTile.y])
                    tiles[currentTile.x + 1][currentTile.y].tileThatGotIt = currentTile
                    tiles[currentTile.x + 1][currentTile.y].turnToAnalyzing()
                    drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
                    pg.display.update()
                    pg.time.wait(delay)
                    tileScores.append(CalculateScore(start, target, currentTile))
        elif currentTile.x == width-1:
            if tiles[currentTile.x - 1][currentTile.y] not in tilesToAnalyze and tiles[currentTile.x - 1][currentTile.y] not in analyzedTiles:
                if tiles[currentTile.x - 1][currentTile.y].currentTile != tile_wall:
                    tilesToAnalyze.append(tiles[currentTile.x - 1][currentTile.y])
                    tiles[currentTile.x - 1][currentTile.y].tileThatGotIt = currentTile
                    tiles[currentTile.x - 1][currentTile.y].turnToAnalyzing()
                    drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
                    pg.display.update()
                    pg.time.wait(delay)
                    tileScores.append(CalculateScore(start, target, currentTile))
        else:
            if tiles[currentTile.x + 1][currentTile.y] not in tilesToAnalyze and tiles[currentTile.x + 1][currentTile.y] not in analyzedTiles:
                if tiles[currentTile.x + 1][currentTile.y].currentTile != tile_wall:
                    tilesToAnalyze.append(tiles[currentTile.x + 1][currentTile.y])
                    tiles[currentTile.x + 1][currentTile.y].tileThatGotIt = currentTile
                    tiles[currentTile.x + 1][currentTile.y].turnToAnalyzing()
                    drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
                    pg.display.update()
                    pg.time.wait(delay)
                    tileScores.append(CalculateScore(start, target, currentTile))
            if tiles[currentTile.x - 1][currentTile.y] not in tilesToAnalyze and tiles[currentTile.x - 1][currentTile.y] not in analyzedTiles:
                if tiles[currentTile.x - 1][currentTile.y].currentTile != tile_wall:
                    tilesToAnalyze.append(tiles[currentTile.x - 1][currentTile.y])
                    tiles[currentTile.x - 1][currentTile.y].tileThatGotIt = currentTile
                    tiles[currentTile.x - 1][currentTile.y].turnToAnalyzing()
                    drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
                    pg.display.update()
                    pg.time.wait(delay)
                    tileScores.append(CalculateScore(start, target, currentTile))

        if currentTile.y == 0:
            if tiles[currentTile.x][currentTile.y + 1] not in tilesToAnalyze and tiles[currentTile.x][currentTile.y + 1] not in analyzedTiles:
                if tiles[currentTile.x][currentTile.y + 1].currentTile != tile_wall:
                    tilesToAnalyze.append(tiles[currentTile.x][currentTile.y + 1])
                    tiles[currentTile.x][currentTile.y + 1].tileThatGotIt = currentTile
                    tiles[currentTile.x][currentTile.y + 1].turnToAnalyzing()
                    drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
                    pg.display.update()
                    pg.time.wait(delay)
                    tileScores.append(CalculateScore(start, target, currentTile))
        elif currentTile.y == height-1:
            if tiles[currentTile.x][currentTile.y - 1] not in tilesToAnalyze and tiles[currentTile.x][currentTile.y - 1] not in analyzedTiles:
                if tiles[currentTile.x][currentTile.y - 1].currentTile != tile_wall:
                    tilesToAnalyze.append(tiles[currentTile.x][currentTile.y - 1])
                    tiles[currentTile.x][currentTile.y - 1].tileThatGotIt = currentTile
                    tiles[currentTile.x][currentTile.y - 1].turnToAnalyzing()
                    drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
                    pg.display.update()
                    pg.time.wait(delay)
                    tileScores.append(CalculateScore(start, target, currentTile))
        else:
            if tiles[currentTile.x][currentTile.y + 1] not in tilesToAnalyze and tiles[currentTile.x][currentTile.y + 1] not in analyzedTiles:
                if tiles[currentTile.x][currentTile.y + 1].currentTile != tile_wall:
                    tilesToAnalyze.append(tiles[currentTile.x][currentTile.y + 1])
                    tiles[currentTile.x][currentTile.y + 1].tileThatGotIt = currentTile
                    tiles[currentTile.x][currentTile.y + 1].turnToAnalyzing()
                    drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
                    pg.display.update()
                    pg.time.wait(delay)
                    tileScores.append(CalculateScore(start, target, currentTile))
            if tiles[currentTile.x][currentTile.y - 1] not in tilesToAnalyze and tiles[currentTile.x][currentTile.y - 1] not in analyzedTiles:
                if tiles[currentTile.x][currentTile.y - 1].currentTile != tile_wall:
                    tilesToAnalyze.append(tiles[currentTile.x][currentTile.y - 1])
                    tiles[currentTile.x][currentTile.y - 1].tileThatGotIt = currentTile
                    tiles[currentTile.x][currentTile.y - 1].turnToAnalyzing()
                    drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
                    pg.display.update()
                    pg.time.wait(delay)
                    tileScores.append(CalculateScore(start, target, currentTile))

        if target in tilesToAnalyze:
            break
        if len(tilesToAnalyze) == 0:
            currentTile.turnToAnalyzed()
            break
        analyzedTiles.append(currentTile)
        currentTile.turnToAnalyzed()
        drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
        pg.display.update()
        pg.time.wait(delay)
        currentTile = tilesToAnalyze[tileScores.index(min(tileScores))]
        currentTile.turnToCurrent()
        drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
        pg.display.update()
        pg.time.wait(delay * 10)
        tilesToAnalyze.pop(tileScores.index(min(tileScores)))
        tileScores.pop(tileScores.index(min(tileScores)))

    if target in tilesToAnalyze:
        currentTile = target
        while start not in path:
            path.append(currentTile.tileThatGotIt)
            currentTile.turnToPath()
            currentTile = currentTile.tileThatGotIt
            drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
            pg.display.update()
            pg.time.wait(delay)
def findPath(start, target, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton):
    delay = 1
    tilesToAnalyze = []
    tileScores = []
    analyzedTiles = []
    path = []
    currentTile = start
    while target not in tilesToAnalyze:
        if currentTile.x == 0:
            if tiles[currentTile.x + 1][currentTile.y] not in tilesToAnalyze and tiles[currentTile.x + 1][currentTile.y] not in analyzedTiles:
                if tiles[currentTile.x + 1][currentTile.y].currentTile != tile_wall:
                    tilesToAnalyze.append(tiles[currentTile.x + 1][currentTile.y])
                    tiles[currentTile.x + 1][currentTile.y].tileThatGotIt = currentTile
                    tiles[currentTile.x + 1][currentTile.y].turnToAnalyzing()
                    tiles[currentTile.x + 1][currentTile.y].score += currentTile.score + 1
                    drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
                    pg.display.update()
                    pg.time.wait(delay)
                    tileScores.append(tiles[currentTile.x + 1][currentTile.y].score)
        elif currentTile.x == width-1:
            if tiles[currentTile.x - 1][currentTile.y] not in tilesToAnalyze and tiles[currentTile.x - 1][currentTile.y] not in analyzedTiles:
                if tiles[currentTile.x - 1][currentTile.y].currentTile != tile_wall:
                    tilesToAnalyze.append(tiles[currentTile.x - 1][currentTile.y])
                    tiles[currentTile.x - 1][currentTile.y].tileThatGotIt = currentTile
                    tiles[currentTile.x - 1][currentTile.y].turnToAnalyzing()
                    tiles[currentTile.x - 1][currentTile.y].score += currentTile.score + 1
                    drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
                    pg.display.update()
                    pg.time.wait(delay)
                    tileScores.append(tiles[currentTile.x - 1][currentTile.y].score)
        else:
            if tiles[currentTile.x + 1][currentTile.y] not in tilesToAnalyze and tiles[currentTile.x + 1][currentTile.y] not in analyzedTiles:
                if tiles[currentTile.x + 1][currentTile.y].currentTile != tile_wall:
                    tilesToAnalyze.append(tiles[currentTile.x + 1][currentTile.y])
                    tiles[currentTile.x + 1][currentTile.y].tileThatGotIt = currentTile
                    tiles[currentTile.x + 1][currentTile.y].turnToAnalyzing()
                    tiles[currentTile.x + 1][currentTile.y].score += currentTile.score + 1
                    drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
                    pg.display.update()
                    pg.time.wait(delay)
                    tileScores.append(tiles[currentTile.x + 1][currentTile.y].score)
            if tiles[currentTile.x - 1][currentTile.y] not in tilesToAnalyze and tiles[currentTile.x - 1][currentTile.y] not in analyzedTiles:
                if tiles[currentTile.x - 1][currentTile.y].currentTile != tile_wall:
                    tilesToAnalyze.append(tiles[currentTile.x - 1][currentTile.y])
                    tiles[currentTile.x - 1][currentTile.y].tileThatGotIt = currentTile
                    tiles[currentTile.x - 1][currentTile.y].turnToAnalyzing()
                    tiles[currentTile.x - 1][currentTile.y].score += currentTile.score + 1
                    drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
                    pg.display.update()
                    pg.time.wait(delay)
                    tileScores.append(tiles[currentTile.x - 1][currentTile.y].score)

        if currentTile.y == 0:
            if tiles[currentTile.x][currentTile.y + 1] not in tilesToAnalyze and tiles[currentTile.x][currentTile.y + 1] not in analyzedTiles:
                if tiles[currentTile.x][currentTile.y + 1].currentTile != tile_wall:
                    tilesToAnalyze.append(tiles[currentTile.x][currentTile.y + 1])
                    tiles[currentTile.x][currentTile.y + 1].tileThatGotIt = currentTile
                    tiles[currentTile.x][currentTile.y + 1].turnToAnalyzing()
                    tiles[currentTile.x][currentTile.y + 1].score += currentTile.score + 1
                    drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
                    pg.display.update()
                    pg.time.wait(delay)
                    tileScores.append(tiles[currentTile.x][currentTile.y + 1].score)
        elif currentTile.y == height-1:
            if tiles[currentTile.x][currentTile.y - 1] not in tilesToAnalyze and tiles[currentTile.x][currentTile.y - 1] not in analyzedTiles:
                if tiles[currentTile.x][currentTile.y - 1].currentTile != tile_wall:
                    tilesToAnalyze.append(tiles[currentTile.x][currentTile.y - 1])
                    tiles[currentTile.x][currentTile.y - 1].tileThatGotIt = currentTile
                    tiles[currentTile.x][currentTile.y - 1].turnToAnalyzing()
                    tiles[currentTile.x][currentTile.y - 1].score += currentTile.score + 1
                    drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
                    pg.display.update()
                    pg.time.wait(delay)
                    tileScores.append(tiles[currentTile.x][currentTile.y - 1].score)
        else:
            if tiles[currentTile.x][currentTile.y + 1] not in tilesToAnalyze and tiles[currentTile.x][currentTile.y + 1] not in analyzedTiles:
                if tiles[currentTile.x][currentTile.y + 1].currentTile != tile_wall:
                    tilesToAnalyze.append(tiles[currentTile.x][currentTile.y + 1])
                    tiles[currentTile.x][currentTile.y + 1].tileThatGotIt = currentTile
                    tiles[currentTile.x][currentTile.y + 1].turnToAnalyzing()
                    tiles[currentTile.x][currentTile.y + 1].score += currentTile.score + 1
                    drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
                    pg.display.update()
                    pg.time.wait(delay)
                    tileScores.append(tiles[currentTile.x][currentTile.y + 1].score)
            if tiles[currentTile.x][currentTile.y - 1] not in tilesToAnalyze and tiles[currentTile.x][currentTile.y - 1] not in analyzedTiles:
                if tiles[currentTile.x][currentTile.y - 1].currentTile != tile_wall:
                    tilesToAnalyze.append(tiles[currentTile.x][currentTile.y - 1])
                    tiles[currentTile.x][currentTile.y - 1].tileThatGotIt = currentTile
                    tiles[currentTile.x][currentTile.y - 1].turnToAnalyzing()
                    tiles[currentTile.x][currentTile.y - 1].score += currentTile.score + 1
                    drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
                    pg.display.update()
                    pg.time.wait(delay)
                    tileScores.append(tiles[currentTile.x][currentTile.y - 1].score)

        if target in tilesToAnalyze:
            break
        if len(tilesToAnalyze) == 0:
            currentTile.turnToAnalyzed()
            break
        analyzedTiles.append(currentTile)
        currentTile.turnToAnalyzed()
        drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
        pg.display.update()
        pg.time.wait(delay)
        currentTile = tilesToAnalyze[tileScores.index(min(tileScores))]
        currentTile.turnToCurrent()
        drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
        pg.display.update()
        pg.time.wait(delay * 10)
        tilesToAnalyze.pop(tileScores.index(min(tileScores)))
        tileScores.pop(tileScores.index(min(tileScores)))

    if target in tilesToAnalyze:
        currentTile = target
        while start not in path:
            path.append(currentTile.tileThatGotIt)
            currentTile.turnToPath()
            currentTile = currentTile.tileThatGotIt
            drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
            pg.display.update()
            pg.time.wait(delay)


def main():
    global width, height, widthInPixels, heightInPixels, run
    sets = False
    gamePlayed = False
    start = None
    target = None
    draw = 0
    run = True
    widthSlider = Slider(41, 79, 0)
    heightSlider = Slider(41, 121, 1)
    settings(win, widthSlider, heightSlider)
    wallButton = Button(1, height + 1, tile_wall)
    tileButton = Button(3, height + 1, tile_blank)
    startButton = Button(5, height + 1, tile_start)
    targetButton = Button(7, height + 1, tile_target)
    slowButton = Button(9, height + 1, tile_slow)
    algoButton = ToggleButton(11, height + 1, d, aStar)
    playButton = Button(13, height + 1, play)
    deleteButton = Button(15, height + 1, delete)
    exitButton = Button(0, height + 2, exit)
    tiles = [[0 for i in range(height)] for j in range(width)]
    for i in range(width):
        for j in range(height):
            tiles[i][j] = Tile(i, j)
    while run:
        drawBoard(width, height, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
        pg.display.update()
        for event in pg.event.get():
            pos = pg.mouse.get_pos()
            x = pos[0]//32
            y = pos[1]//32

            if event.type == pg.MOUSEBUTTONDOWN:

                if x == 1 and y == height + 1:
                    draw = 1
                elif x == 3 and y == height + 1:
                    draw = 2
                elif x == 5 and y == height + 1:
                    if start is not None:
                        start.reset()
                        start = None
                    draw = 3
                elif x == 7 and y == height + 1:
                    if target is not None:
                        target.reset()
                        target = None
                    draw = 4
                elif x == 9 and y == height + 1:
                    draw = 5
                elif x == 11 and y == height + 1:
                    algoButton.toggle()
                elif x == 13 and y == height + 1:
                    if start is None or target is None:
                        print("Start or Target not placed!")
                    elif not gamePlayed:
                        if algoButton.currentTile == algoButton.possibleTiles[0]:
                            findPath(start, target, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
                        elif algoButton.currentTile == algoButton.possibleTiles[1]:
                            findPathA(start, target, tiles, wallButton, tileButton, startButton, targetButton, deleteButton, playButton, slowButton, algoButton, exitButton)
                        gamePlayed = True
                elif x == 15 and y == height + 1:
                    start, target = reset(tiles)
                    gamePlayed = False

                elif x == 0 and y == height + 2:
                    gamePlayed = False
                    sets = True

            if pg.mouse.get_pressed()[0]:
                if draw == 1:
                    if x < width and y < height:
                        tiles[x][y].turnToWall()
                if draw == 2:
                    if x < width and y < height:
                        tiles[x][y].turnToBlank()
                if draw == 3 and start is None:
                    if x < width and y < height:
                        tiles[x][y].turnToStart()
                        start = tiles[x][y]
                if draw == 4 and target is None:
                    if x < width and y < height:
                        tiles[x][y].turnToTarget()
                        target = tiles[x][y]
                if draw == 5:
                    if x < width and y < height:
                        tiles[x][y].turnToSlow()

            if event.type == pg.QUIT:
                run = False
                pg.quit()

        if sets:
            sets = settings(win, widthSlider, heightSlider)
            wallButton = Button(1, height + 1, tile_wall)
            tileButton = Button(3, height + 1, tile_blank)
            startButton = Button(5, height + 1, tile_start)
            targetButton = Button(7, height + 1, tile_target)
            slowButton = Button(9, height + 1, tile_slow)
            algoButton = ToggleButton(11, height + 1, d, aStar)
            playButton = Button(13, height + 1, play)
            deleteButton = Button(15, height + 1, delete)
            exitButton = Button(0, height + 2, exit)
            tiles = [[0 for i in range(height)] for j in range(width)]
            for i in range(width):
                for j in range(height):
                    tiles[i][j] = Tile(i, j)


main()