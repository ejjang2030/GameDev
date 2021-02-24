import pygame
import random
import sys
from tkinter import *
from tkinter import messagebox
from PIL import Image

from pygame.examples.textinput import BGCOLOR
from pygame.locals import *

from ImageView import resizeImage
from Button import Button


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (30, 30, 30)
background_color = WHITE
screen_width = 1024
screen_height = 512
screen_center = screen_width / 2, screen_height / 3

# 짝 맞추기 게임(두카드 뒤집기 게임)
# 기본 설정
FPS = 30  # frames per second, the general speed of the program
WINDOWWIDTH = 1024  # size of window's width in pixels
WINDOWHEIGHT = int(2 * 1024 / 3)  # size of windows' height in pixels
REVEALSPEED = 8  # speed boxes' sliding reveals and covers
backImg = Image.open('images/twoCardFlipImages/back.png')
box_width = int(backImg.width / 4)
box_height = int(backImg.height / 4)

BOXSIZE = 60  # size of box height & width in pixels
GAPSIZE = 20  # size of gap between boxes in pixels
BOARDWIDTH = 4  # number of columns of icons
BOARDHEIGHT = 4  # number of rows of icons
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (box_width + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (box_height + GAPSIZE))) / 2)

pics = []
for i in range(1, 11):
    pics.append('clover' + str(i))
for i in range(1, 11):
    pics.append('dia' + str(i))
for i in range(1, 11):
    pics.append('heart' + str(i))
for i in range(1, 11):
    pics.append('spaid' + str(i))

BOXCOLOR = 255, 255, 255  # 파란색
HIGHLIGHTCOLOR = 255, 0, 0  # 빨간색


def twoCardFlipStartGame():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()

    pygame.mixer.init()
    pygame.mixer.music.load("musics/twocardgamemusic.mp3")
    pygame.mixer.music.play(-5, 0.0)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mouseX = 0
    mouseY = 0  # 마우스 이벤트 발생 좌표
    pygame.display.set_caption("두카드 뒤집기 게임")
    pygame.display.set_icon(pygame.image.load("images/twoCardFlipImages/back.png"))
    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None  # 첫 클릭 좌표 저장
    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    while True:  # game loop
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR)  # draw window
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get():  # 이벤트 처리 루프
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                mouseClicked = True

        boxX, boxY = getBoxAtPixel(mouseX, mouseY)
        if boxX is not None and boxY is not None:
            # 마우스가 현재 박스 위에 있다.
            if not revealedBoxes[boxX][boxY]:  # 닫힌 상자라면 하이라이트만
                drawHighLightBox(boxX, boxY)
            if not revealedBoxes[boxX][boxY] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxX, boxY)])
                revealedBoxes[boxX][boxY] = True  # 닫힌 상자 + 클릭 -> 박스 열기
                if firstSelection is None:  # 1번 박스 > 좌표 기록
                    firstSelection = (boxX, boxY)
                else:  # 1번 박스 아님 > 2번 박스 > 짝 검사
                    icon1shape, icon1color = getPicAndNum(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getPicAndNum(mainBoard, boxX, boxY)
                    if icon1shape is not icon2shape or icon1color is not icon2color:
                        # 서로 다름이면 둘 다 닫기
                        pygame.time.wait(1000)  # 1초
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxX, boxY)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxX][boxY] = False

                    # 다 오픈되었으면
                    elif hasWon(revealedBoxes):
                        gameWonAnimation()
                        pygame.time.wait(1000)
                        '''
                        # 게임판 재설정
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        # 잠깐 공개
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        # 게임 시작
                        startGameAnimation(mainBoard)
                        # pygame.mixer.music.play(-5, 0.0)
                        '''
                    firstSelection = None

                # 화면을 다시 그린 다음 시간 지연을 기다린다...
            pygame.display.update()
            FPSCLOCK.tick(FPS)


# 카드가 다 뒤집어 졌는지 여부를 판별하는 메소드
def hasWon(revealedBoxes):
    # 모든 상자가 열렸으면 True, 아니면 False
    for n in revealedBoxes:
        if False in n:
            return False  # 닫힌게 있으면 False
    return True


# 카드를 다시 엎어놓은 상태를 저장하는 메소드
def generateRevealedBoxesData(val):  # 열린 상자 만들기
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


def getRandomizedBoard():  # 카드 섞기
    global pics
    cards = []
    pictures = random.sample(pics, int(BOARDWIDTH * BOARDHEIGHT / 2))
    for pic in pictures:
        for num in range(1, 2):
            cards.append((pic, num))
            print(cards)
    random.shuffle(cards)
    print(cards)
    numCardsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2)
    cards = cards[:numCardsUsed] * 2
    print(cards)
    random.shuffle(cards)
    # 게임판 만들기
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(cards[0])
            del cards[0]  # 추가한 아이콘을 지운다
        board.append(column)
    print(board)
    return board


def splitIntoGroupsOf(groupSize, theList):
    # 2차원 리스트 생성, 최대로 groupSize만큼의 요소포함
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxX, boxY):
    # 좌표를 픽셀 좌표로 변환
    left = boxX * (box_width + GAPSIZE) + XMARGIN
    top = boxY * (box_height + GAPSIZE) + YMARGIN
    return left, top


def getBoxAtPixel(x, y):
    for boxX in range(BOARDWIDTH):
        for boxY in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxX, boxY)
            boxRect = pygame.Rect(left, top, box_width, box_height)
            if boxRect.collidepoint(x, y):
                return boxX, boxY
    return None, None


def resizeImageAll(name, width, height):
    for i in range(1, 11):
        resizeImage('images/twoCardFlipImages', f'{name}_{i}', width, height)


# 그림 카드 만들기
def makeCards(name, width, height):
    img = [None]
    for n in range(1, 11):
        img.append(pygame.image.load(f'images/twoCardFlipImages/{name}_{n}_{width}x{height}.png'))
    return img


def showCards(imgList, pic, name, left, top):
    for i in range(1, 11):
        if pic == name + str(i):
            DISPLAYSURF.blit(imgList[i], (left, top))


def drawCard(pic, num, boxX, boxY):
    quarter = int(BOXSIZE * 0.25)
    half = int(BOXSIZE * 0.5)
    eight = int(BOXSIZE * 0.125)

    left, top = leftTopCoordsOfBox(boxX, boxY)  # 보드 좌표에서 픽셀 좌표 구하기

    # resizeImageAll('clover', box_width, box_height)
    # resizeImageAll('dia', box_width, box_height)
    # resizeImageAll('heart', box_width, box_height)
    # resizeImageAll('spaid', box_width, box_height)

    cloverImg = makeCards('clover', box_width, box_height)
    diaImg = makeCards('dia', box_width, box_height)
    heartImg = makeCards('heart', box_width, box_height)
    spaidImg = makeCards('spaid', box_width, box_height)

    showCards(cloverImg, pic, 'clover', left, top)
    showCards(diaImg, pic, 'dia', left, top)
    showCards(heartImg, pic, 'heart', left, top)
    showCards(spaidImg, pic, 'spaid', left, top)


def getPicAndNum(board, boxX, boxY):
    # 아이콘 값은 board[x][y][0] 에 있다.
    # 색깔 값은 board[x][y][1]에 있다.
    return board[boxX][boxY][0], board[boxX][boxY][1]


def drawBoxCovers(board, boxes, coverage):
    # 닫히겨나 열린 상태의 상자를 그린다.
    # 상자는 요소 2개를 가진 리스트이며 xy 위치를 가진다.
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, box_width, box_height))
        pic, num = getPicAndNum(board, box[0], box[1])
        drawCard(pic, num, box[0], box[1])
        if coverage > 0:  # 닫힌 상태이면, 덮개만:
            resizeImage('images/twoCardFlipImages', 'back', box_width, box_height)
            back = pygame.image.load(f'images/twoCardFlipImages/back_{box_width}x{box_height}.png')
            backRect = back.get_rect()
            backRect.center = left + box_width // 2, top + box_height // 2
            DISPLAYSURF.blit(back, backRect)
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, backRect, 1)
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    # 상자가 열려요
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesTocover):
    # 상자가 닫혀요
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesTocover, coverage)


def drawBoard(board, revealed):
    # 모든 상자를 상태에 맞추어 그리기
    for boxX in range(BOARDWIDTH):
        for boxY in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxX, boxY)
            if not revealed[boxX][boxY]:
                # 닫힌 상자를 만든다.
                resizeImage('images/twoCardFlipImages', 'back', box_width, box_height)
                back = pygame.image.load(f'images/twoCardFlipImages/back_{box_width}x{box_height}.png')
                backRect = back.get_rect()
                backRect.center = left + box_width // 2, top + box_height // 2
                DISPLAYSURF.blit(back, backRect)
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, backRect, 1)
            else:
                # 열린 상자
                pic, num = getPicAndNum(board, boxX, boxY)
                drawCard(pic, num, boxX, boxY)


def drawHighLightBox(boxX, boxY):
    left, top = leftTopCoordsOfBox(boxX, boxY)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, box_width + 10, box_height + 10), 4)


def startGameAnimation(board):
    # 무작위로 상자를 열어서 보여준다.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x, y))
    random.shuffle(boxes)
    boxlist = random.sample(boxes, 4)
    boxGroups = splitIntoGroupsOf(1, boxlist)
    drawBoard(board, coveredBoxes)

    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def gameWonAnimation():
    pygame.mixer.music.fadeout(10)
    clock = pygame.time.Clock()
    # color1, color2 = color2, color1  # 색깔 깜빡이기
    # screen.blit(cardbackimg, (0, 0))
    # pygame.display.flip()
    # pygame.time.wait(200)

    # drawBoard(board, coveredBoxes)
    # pygame.time.wait(300)

    playing = True
    while playing:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
                sys.exit()

        # 스크린 배경색 칠하기
        DISPLAYSURF.fill(WHITE)

        # 버튼 만들기
        # showButtonText(DISPLAYSURF, "성공!", 50, (WINDOWWIDTH // 2, int(WINDOWHEIGHT / 2)), BLACK)
        againButton = Button(DISPLAYSURF, "다시시작", (WINDOWWIDTH - 140, WINDOWHEIGHT - 200), (120, 50))
        againButton.setInactivatedColor((0, 255, 0))
        againButton.setActivatedColor((0, 255, 100))
        againButton.mouseOnButtonHoverAndClickListener(twoCardFlipStartGame)
        againButton.showButtonText(20, BLACK)
        from initalGame import selectGame
        backButton = Button(DISPLAYSURF, "뒤로가기", (WINDOWWIDTH - 140, WINDOWHEIGHT - 130), (120, 50))
        backButton.setInactivatedColor((0, 0, 255))
        backButton.setActivatedColor((0, 100, 255))
        backButton.mouseOnButtonHoverAndClickListener(selectGame)
        backButton.showButtonText(20, BLACK)
        quitButton = Button(DISPLAYSURF, "게임종료", (WINDOWWIDTH - 140, WINDOWHEIGHT - 60), (120, 50))
        quitButton.setInactivatedColor((255, 0, 0))
        quitButton.setActivatedColor((255, 100, 0))
        quitButton.mouseOnButtonHoverAndClickListener("quit")
        quitButton.showButtonText(20, BLACK)
        # 작업한 내용 갱신하기
        pygame.display.flip()

        # 1초에 60번의 빈도로 순환하기
        clock.tick(60)

