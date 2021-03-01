import random
from tkinter import *

import pygame
from PIL import Image
from pygame.examples.textinput import BGCOLOR
from pygame.locals import *

from Button import Button
from ImageView import resizeImage
from TextView import TextView

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (30, 30, 30)
background_color = WHITE
screen_width = 1024
screen_height = 512
WINDOWWIDTH = 1024  # size of window's width in pixels
WINDOWHEIGHT = int(2 * 1024 / 3)  # size of windows' height in pixels
screen_center = WINDOWWIDTH / 2, WINDOWHEIGHT / 3


def initGame():
    # pygame 초기화
    pygame.init()

    # 스크린 객체 저장
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Game")

    # 게임 시간을 위한 Clock 생성
    clock = pygame.time.Clock()

    imageString = "images/pygame.png"
    image = Image.open(imageString)
    image_width, image_height = image.size
    image_center = image_width / 2, image_height / 2
    initialImage = pygame.image.load(imageString)
    initialImagePos = screen_center[0] - image_center[0], screen_center[1] - image_center[1]

    playing = True
    while playing:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
                sys.exit()

        # 스크린 배경색 칠하기
        screen.fill(background_color)

        # 스크린 원하는 좌표에 이미지 찍기
        screen.blit(initialImage, initialImagePos)

        mouse = pygame.mouse.get_pos()

        # 버튼 만들기
        button1_size = 2 * image_width / 5, image_height / 2
        button1_center = WINDOWWIDTH / 2 - 3 * image_width / 10, 2 * WINDOWHEIGHT / 3
        button1_pos = WINDOWWIDTH / 2 - 3 * image_width / 10 - image_width / 5, 2 * WINDOWHEIGHT / 3 - image_height / 4
        button2_size = 2 * image_width / 5, image_height / 2
        button2_center = WINDOWWIDTH / 2 + 3 * image_width / 10, 2 * WINDOWHEIGHT / 3
        button2_pos = WINDOWWIDTH / 2 + 3 * image_width / 10 - image_width / 5, 2 * WINDOWHEIGHT / 3 - image_height / 4

        startButton = Button(screen, "시작하기", 40, BLACK, button1_pos, button1_size, (255, 100, 0), (255, 0, 0))
        startButton.onClickListener(selectGame)
        quitButton = Button(screen, "그만하기", 40, BLACK, button2_pos, button2_size, (0, 255, 100), (0, 255, 200))
        quitButton.onClickListener(sys.exit)

        # 작업한 내용 갱신하기
        pygame.display.flip()

        # 1초에 60번의 빈도로 순환하기
        clock.tick(60)


def selectGame():
    # 스크린 기본 설정
    background_color = WHITE
    screen_width = WINDOWWIDTH
    screen_height = WINDOWHEIGHT
    screen_center = WINDOWWIDTH / 2, screen_height / 3

    # pygame 초기화
    pygame.init()

    # 스크린 객체 저장
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Game")

    # 게임 시간을 위한 Clock 생성
    clock = pygame.time.Clock()

    playing = True
    while playing:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
                sys.exit()

        # 스크린 배경색 칠하기
        screen.fill(background_color)

        # 버튼 만들기
        button_size = (200, 80)
        backButton = Button(screen, "뒤로가기", 20, BLACK, (WINDOWWIDTH - 140, WINDOWHEIGHT - 60), (120, 50), (0, 255, 0),
                            (0, 255, 100))
        backButton.onClickListener(initGame)
        twoCardFlipGameButton = Button(screen, "두카드 뒤집기 게임", 20, BLACK,
                                       (WINDOWWIDTH / 2 - button_size[0] / 2, WINDOWHEIGHT / 4 - button_size[1] / 2),
                                       button_size, (255, 255, 0), (255, 255, 200))
        twoCardFlipGameButton.onClickListener(twoCardFlipGame)
        omokGameButton = Button(screen, "오목 게임", 20, BLACK,
                                (WINDOWWIDTH / 2 - button_size[0] / 2, 2 * WINDOWHEIGHT / 4 - button_size[1] / 2),
                                button_size, (255, 255, 0), (255, 255, 200))
        omokGameButton.onClickListener(omokGame)
        # 작업한 내용 갱신하기
        pygame.display.flip()

        # 1초에 60번의 빈도로 순환하기
        clock.tick(60)


WHITE = (255, 255, 255)

# 짝 맞추기 게임(두카드 뒤집기 게임)
# 기본 설정
FPS = 30  # frames per second, the general speed of the program

REVEALSPEED = 8  # speed boxes' sliding reveals and covers
backImg = Image.open('images/twoCardFlipImages/back.png')
card_width = int(backImg.width / 4)
card_height = int(backImg.height / 4)
card_horizontal_gap = 20
card_vertical_gap = 20
board_width = 4
board_height = 4

BOXSIZE = 60  # size of box height & width in pixels
GAPSIZE = 20  # size of gap between boxes in pixels
BOARDWIDTH = 4  # number of columns of icons
BOARDHEIGHT = 4  # number of rows of icons
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (card_width + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (card_height + GAPSIZE))) / 2)

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


def twoCardFlipGame():
    pygame.init()
    surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("두카드 뒤집기 게임")
    surface.fill(WHITE)

    menu = Menu(surface)
    board = Board(surface, (card_width, card_height), (card_horizontal_gap, card_vertical_gap), (BOARDWIDTH, BOARDHEIGHT))
    while True:
        runTwoCardFlipGame(surface, board)
        menu.is_continue(board)


def runTwoCardFlipGame(surface, board):
    global FPSCLOCK
    pygame.display.set_caption("두카드 뒤집기 게임")
    pygame.display.set_icon(pygame.image.load("images/twoCardFlipImages/back.png"))
    pygame.mixer.init()
    pygame.mixer.music.load("musics/twocardgamemusic.mp3")
    pygame.mixer.music.play(-5, 0.0)
    FPSCLOCK = pygame.time.Clock()

    mouseX = 0
    mouseY = 0  # 마우스 이벤트 발생 좌표

    board.setRandomBoard()
    revealed_boxes = board.generateRevealedBoxesData(False)
    print(revealed_boxes)
    first_selection = None  # 첫 클릭 좌표 저장
    surface.fill(WHITE)
    board.startGameAnimation()

    while True:  # game loop
        mouseClicked = False

        surface.fill(WHITE)  # draw window
        board.drawBoard(revealed_boxes)

        againButton = Button(surface, "다시시작", 20, BLACK, (board.surface_width - 140, board.surface_height - 200),
                             (120, 50),
                             (0, 255, 0), (0, 255, 100))
        againButton.onClickListener(twoCardFlipGame)
        backButton = Button(surface, "뒤로가기", 20, BLACK, (board.surface_width - 140, board.surface_height - 130),
                            (120, 50),
                            (0, 0, 255), (0, 100, 255))
        backButton.onClickListener(back)
        quitButton = Button(surface, "게임종료", 20, BLACK, (board.surface_width - 140, board.surface_height - 60),
                            (120, 50),
                            (255, 0, 0), (255, 100, 0))
        quitButton.onClickListener(sys.exit)

        for event in pygame.event.get():  # 이벤트 처리 루프
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                mouseClicked = True

        boxX, boxY = board.getMousePositionOnBoard(mouseX, mouseY)
        if boxX is not None and boxY is not None:
            # 마우스가 현재 박스 위에 있다.
            if not revealed_boxes[boxX][boxY]:  # 닫힌 상자라면 하이라이트만
                board.drawHighLightCard(boxX, boxY)
            if not revealed_boxes[boxX][boxY] and mouseClicked:
                board.revealBoxesAnimation([(boxX, boxY)])
                revealed_boxes[boxX][boxY] = True  # 닫힌 상자 + 클릭 -> 박스 열기
                if first_selection is None:  # 1번 박스 > 좌표 기록
                    first_selection = (boxX, boxY)
                else:  # 1번 박스 아님 > 2번 박스 > 짝 검사
                    icon1shape, icon1color = board.getPicAndNum(first_selection[0], first_selection[1])
                    icon2shape, icon2color = board.getPicAndNum(boxX, boxY)
                    if icon1shape is not icon2shape or icon1color is not icon2color:
                        # 서로 다름이면 둘 다 닫기
                        pygame.time.wait(1000)  # 1초
                        board.coverBoxesAnimation([(first_selection[0], first_selection[1]), (boxX, boxY)])
                        revealed_boxes[first_selection[0]][first_selection[1]] = False
                        revealed_boxes[boxX][boxY] = False

                    # 다 오픈되었으면
                    elif board.hasWon(revealed_boxes):
                        board.gameWonAnimation()
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


def back():
    pygame.mixer.music.fadeout(10)
    selectGame()


class Board:
    def __init__(self, surface: pygame.Surface, card_size: tuple, card_gap: tuple, board_size_2: tuple):
        self.surface = surface
        self.surface_width, self.surface_height = self.surface.get_size()
        self.card_width, self.card_height = card_size
        self.card_horizontal_gap, self.card_vertical_gap = card_gap
        self.board_width, self.board_height = board_size_2
        self.pics = []
        for n in range(1, 11):
            self.pics.append('clover' + str(n))
        for n in range(1, 11):
            self.pics.append('dia' + str(n))
        for n in range(1, 11):
            self.pics.append('heart' + str(n))
        for n in range(1, 11):
            self.pics.append('spaid' + str(n))
        self.board = self.getRandomBoard()
        self.x_margin = int((self.surface_width - (self.board_width * (self.card_width + self.card_horizontal_gap))) / 2)
        self.y_margin = int((self.surface_height - (self.board_height * (self.card_height + self.card_vertical_gap))) / 2)

        self.revealed_boxes = []

    def drawCard(self, card, boxX, boxY):
        left, top = self.getCardPosition(boxX, boxY)  # 보드 좌표에서 픽셀 좌표 구하기

        # resizeImageAll('clover', box_width, box_height)
        # resizeImageAll('dia', box_width, box_height)
        # resizeImageAll('heart', box_width, box_height)
        # resizeImageAll('spaid', box_width, box_height)

        cloverImg = self.makeCards('clover', self.card_width, self.card_height)
        diaImg = self.makeCards('dia', self.card_width, self.card_height)
        heartImg = self.makeCards('heart', self.card_width, self.card_height)
        spaidImg = self.makeCards('spaid', self.card_width, self.card_height)

        self.showCards(cloverImg, card, 'clover', left, top)
        self.showCards(diaImg, card, 'dia', left, top)
        self.showCards(heartImg, card, 'heart', left, top)
        self.showCards(spaidImg, card, 'spaid', left, top)

    def showCards(self, image_list, pic, name, left, top):
        for n in range(1, 11):
            if pic == name + str(n):
                self.surface.blit(image_list[n], (left, top))

    def getCardPosition(self, boxX, boxY):
        # 좌표를 픽셀 좌표로 변환
        left = boxX * (self.card_width + self.card_horizontal_gap) + self.x_margin
        top = boxY * (self.card_height + self.card_vertical_gap) + self.y_margin
        return left, top

    def drawBoard(self, revealed):
        for boxX in range(self.board_width):
            for boxY in range(self.board_height):
                left, top = self.getCardPosition(boxX, boxY)
                print(boxX, boxY)
                if not revealed[boxX][boxY]:
                    # 닫힌 상자를 만든다.
                    resizeImage('images/twoCardFlipImages', 'back', self.card_width, self.card_height)
                    back_of_card = pygame.image.load(
                        f'images/twoCardFlipImages/back_{self.card_width}x{self.card_height}.png')
                    back_of_card_rect = back_of_card.get_rect()
                    back_of_card_rect.center = left + self.card_width // 2, top + self.card_height // 2
                    self.surface.blit(back_of_card, back_of_card_rect)
                    pygame.draw.rect(self.surface, (255, 255, 255), back_of_card_rect, 1)
                else:
                    # 열린 상자
                    card, num = self.getPicAndNum(boxX, boxY)
                    self.drawCard(card, boxX, boxY)

    def drawBoxCovers(self, board, boxes, coverage):
        global FPSCLOCK
        # 닫히겨나 열린 상태의 상자를 그린다.
        # 상자는 요소 2개를 가진 리스트이며 xy 위치를 가진다.
        for box in boxes:
            left, top = self.getCardPosition(box[0], box[1])
            pygame.draw.rect(self.surface, BGCOLOR, (left, top, self.card_width, self.card_height))
            card, num = self.getPicAndNum(box[0], box[1])
            self.drawCard(card, box[0], box[1])
            if coverage > 0:  # 닫힌 상태이면, 덮개만:
                resizeImage('images/twoCardFlipImages', 'back', self.card_width, self.card_height)
                back = pygame.image.load(f'images/twoCardFlipImages/back_{self.card_width}x{self.card_height}.png')
                backRect = back.get_rect()
                backRect.center = left + self.card_width // 2, top + self.card_height // 2
                self.surface.blit(back, backRect)
                pygame.draw.rect(self.surface, BOXCOLOR, backRect, 1)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

    def getPicAndNum(self, boxX, boxY):
        # 아이콘 값은 board[x][y][0] 에 있다.
        # 색깔 값은 board[x][y][1]에 있다.
        return self.board[boxX][boxY][0], self.board[boxX][boxY][1]

    def setRandomBoard(self):
        self.board = self.getRandomBoard()

    def getRandomBoard(self):  # 카드 섞기
        cards = []
        pictures = random.sample(self.pics, int(self.board_width * self.board_height / 2))
        for pic in pictures:
            cards.append((pic, 1))
            # print(cards)
        random.shuffle(cards)
        # print(cards)
        num_cards_used = int(self.board_width * self.board_height / 2)
        cards = cards[:num_cards_used] * 2
        # print(cards)
        random.shuffle(cards)
        # 게임판 만들기
        board = []
        for x in range(self.board_width):
            column = []
            for y in range(self.board_height):
                column.append(cards[0])
                del cards[0]  # 추가한 아이콘을 지운다
            board.append(column)
        # print(board)
        return board

    # getBoxAtPixel을 다음 메서드로 구현
    def getMousePositionOnBoard(self, x, y):
        for boxX in range(self.board_width):
            for boxY in range(self.board_height):
                left, top = self.getCardPosition(boxX, boxY)
                box_rect = pygame.Rect(left, top, self.card_width, self.card_height)
                if box_rect.collidepoint(x, y):
                    return boxX, boxY
        return None, None

    def drawHighLightCard(self, boxX, boxY,  highlight_color=(255, 0, 0)):
        left, top = self.getCardPosition(boxX, boxY)
        pygame.draw.rect(self.surface, highlight_color, (left - 5, top - 5, self.card_width + 10, self.card_height + 10), 4)

    # 카드를 다시 엎어놓은 상태를 저장하는 메소드
    def generateRevealedBoxesData(self, val):
        boxes = []  # 열린 상자 만들기
        for n in range(self.board_width):
            boxes.append([val] * self.board_height)
        return boxes

    def startGameAnimation(self):
        # 무작위로 상자를 열어서 보여준다.
        covered_boxes = self.generateRevealedBoxesData(False)
        boxes = []
        for x in range(self.board_width):
            for y in range(self.board_height):
                boxes.append((x, y))
        random.shuffle(boxes)
        box_list = random.sample(boxes, 4)
        box_groups = self.splitIntoGroupsOf(1, box_list)
        self.drawBoard(covered_boxes)

        for boxGroup in box_groups:
            self.revealBoxesAnimation(boxGroup)
            self.coverBoxesAnimation(boxGroup)

    def revealBoxesAnimation(self, boxesToReveal):
        # 상자가 열려요
        for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
            self.drawBoxCovers(self.board, boxesToReveal, coverage)

    def coverBoxesAnimation(self, boxesTocover):
        # 상자가 닫혀요
        for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
            self.drawBoxCovers(self.board, boxesTocover, coverage)

    def gameWonAnimation(self):
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
            self.surface.fill(WHITE)

            # 버튼 만들기
            # showButtonText(DISPLAYSURF, "성공!", 50, (WINDOWWIDTH // 2, int(WINDOWHEIGHT / 2)), BLACK)
            winText = TextView(self.surface, "성공!", "fonts/ELAND_Choice_M.ttf", 50, BLACK,
                               (self.surface_width // 2, int(self.surface_height / 2)))
            winText.showText()
            againButton = Button(self.surface, "다시시작", 20, BLACK, (self.surface_width - 140, self.surface_height - 200), (120, 50),
                                 (0, 255, 0), (0, 255, 100))
            againButton.onClickListener(twoCardFlipGame)
            backButton = Button(self.surface, "뒤로가기", 20, BLACK, (self.surface_width - 140, self.surface_height - 130), (120, 50),
                                (0, 0, 255), (0, 100, 255))
            backButton.onClickListener(selectGame)
            quitButton = Button(self.surface, "게임종료", 20, BLACK, (self.surface_width - 140, self.surface_height - 60), (120, 50),
                                (255, 0, 0), (255, 100, 0))
            quitButton.onClickListener(sys.exit)
            # 작업한 내용 갱신하기
            pygame.display.flip()

            # 1초에 60번의 빈도로 순환하기
            clock.tick(60)


    # 카드가 다 뒤집어 졌는지 여부를 판별하는 메소드
    def hasWon(self, revealedBoxes):
        # 모든 상자가 열렸으면 True, 아니면 False
        for n in revealedBoxes:
            if False in n:
                return False  # 닫힌게 있으면 False
        return True

    def splitIntoGroupsOf(self, groupSize, theList):
        # 2차원 리스트 생성, 최대로 groupSize만큼의 요소포함
        result = []
        for i in range(0, len(theList), groupSize):
            result.append(theList[i:i + groupSize])
        return result

    def resizeImageAll(self, name, width, height):
        for i in range(1, 11):
            resizeImage('images/twoCardFlipImages', f'{name}_{i}', width, height)

    # 그림 카드 만들기
    def makeCards(self, name, width, height):
        img = [None]
        for n in range(1, 11):
            img.append(pygame.image.load(f'images/twoCardFlipImages/{name}_{n}_{width}x{height}.png'))
        return img


bg_color = (128, 128, 128)
black = (0, 0, 0)
blue = (0, 50, 255)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 200, 0)

window_width = 800
window_height = 500
board_width = 500
grid_size = 30

fps = 60
fps_clock = pygame.time.Clock()
is_show = True

def omokGame():
    pygame.init()
    surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Omok game")
    surface.fill(bg_color)

    omok = Omok(surface)
    menu = Menu(surface)
    while True:
        run_game(surface, omok, menu)
        menu.is_continue(omok)


def run_game(surface, omok, menu):
    omok.init_game()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                menu.terminate()
            elif event.type == MOUSEBUTTONUP:
                if not omok.check_board(event.pos):
                    if menu.check_rect(event.pos, omok):
                        omok.init_game()

        back_button = Button(surface, "Back", 20, (255, 255, 255), (WINDOWWIDTH - 220, WINDOWHEIGHT - 7 * 60), (180, 50), (0, 0, 255),
                             (0, 200, 255), 3)
        back_button.onClickListener(menu.back)
        undo_button = Button(surface, "Undo", 20, (255, 255, 255), (WINDOWWIDTH - 220, WINDOWHEIGHT - 6 * 60), (180, 50), (0, 0, 255),
                             (0, 200, 255), 3)
        undo_button.onClickListener(omok.undo)
        undoall_button = Button(surface, "Undo All", 20, (255, 255, 255), (WINDOWWIDTH - 220, WINDOWHEIGHT - 5 * 60), (180, 50), (0, 0, 255),
                             (0, 200, 255), 3)
        undoall_button.onClickListener(omok.undo_all)
        redo_button = Button(surface, "Redo", 20, (255, 255, 255), (WINDOWWIDTH - 220, WINDOWHEIGHT - 4 * 60), (180, 50), (0, 0, 255),
                             (0, 200, 255), 3)
        redo_button.onClickListener(omok.redo)
        new_button = Button(surface, "New Game", 20, (255, 255, 255), (WINDOWWIDTH - 220, WINDOWHEIGHT - 3 * 60), (180, 50), (0, 0, 255),
                             (0, 200, 255), 3)
        new_button.onClickListener(omokGame)
        menu.set_omok(omok)
        hide_button = Button(surface, None, 20, (255, 255, 255), (WINDOWWIDTH - 220, WINDOWHEIGHT - 2 * 60), (180, 50),
                             (0, 0, 255),
                             (0, 200, 255), 3)
        # print(is_show)
        if is_show:
            hide_button.setText("Show Number")
        else:
            hide_button.setText("Hide Number")
        menu.set_button(hide_button)
        hide_button.onClickListener(menu.show_hide)
        quit_button = Button(surface, "Quit", 20, (255, 255, 255), (WINDOWWIDTH - 220, WINDOWHEIGHT - 60), (180, 50), (0, 0, 255),
                             (0, 200, 255), 3)
        quit_button.onClickListener(menu.terminate)

        if omok.is_gameover:
            return

        pygame.display.update()
        fps_clock.tick(fps)


class Omok:
    def __init__(self, surface):
        self.board = [[0 for i in range(board_size)] for j in range(board_size)]
        self.menu = Menu(surface)
        self.rule = Rule(self.board)
        self.surface = surface
        self.pixel_coords = []
        self.set_coords()
        self.set_image_font()
        self.is_show = None
        self.textview = TextView(self.surface, None, "fonts/ELAND_Choice_M.ttf", 20, None, None)

    def init_game(self):
        self.turn = black_stone
        self.draw_board()
        self.menu.show_msg(empty)
        self.init_board()
        self.coords = []
        self.redos = []
        self.backs = []
        self.id = 1
        self.is_gameover = False

    def set_image_font(self):
        black_img = pygame.image.load('images/omokImages/black.png')
        white_img = pygame.image.load('images/omokImages/white.png')
        self.last_w_img = pygame.image.load('images/omokImages/white_a.png')
        self.last_b_img = pygame.image.load('images/omokImages/black_a.png')
        self.board_img = pygame.image.load('images/omokImages/board.png')
        self.font = pygame.font.Font("fonts/ELAND_Choice_M.ttf", 14)
        self.black_img = pygame.transform.scale(black_img, (grid_size, grid_size))
        self.white_img = pygame.transform.scale(white_img, (grid_size, grid_size))

    def init_board(self):
        for y in range(board_size):
            for x in range(board_size):
                self.board[y][x] = 0

    def draw_board(self):
        self.surface.blit(self.board_img, (0, 0))

    def draw_image(self, img_index, x, y):
        img = [self.black_img, self.white_img, self.last_b_img, self.last_w_img]
        self.surface.blit(img[img_index], (x, y))

    def show_number(self, x, y, stone, number):
        colors = [white, black, red, red]
        color = colors[stone]
        # print("self.text : ", self.textview.__dict__)
        self.menu.make_text(self.font, str(number), color, None, y + 15, x + 15, 1, textview=self.textview)

    def hide_numbers(self):
        for i in range(len(self.coords)):
            x, y = self.coords[i]
            self.draw_image(i % 2, x, y)
        if self.coords:
            x, y = self.coords[-1]
            self.draw_image(i % 2 + 2, x, y)

    def show_numbers(self):
        for i in range(len(self.coords)):
            x, y = self.coords[i]
            self.show_number(x, y, i % 2, i + 1)
        if self.coords:
            x, y = self.coords[-1]
            self.draw_image(i % 2, x, y)
            self.show_number(x, y, i % 2 + 2, i + 1)

    def draw_stone(self, coord, stone, increase):
        x, y = self.get_point(coord)
        self.board[y][x] = stone
        self.hide_numbers()
        if self.is_show:
            self.show_numbers()
        self.id += increase
        self.turn = 3 - self.turn

    # todo : undo 메서드 제대로 작동 안됨
    def undo(self):
        if not self.coords:
            return
        self.draw_board()
        coord = self.coords.pop()
        self.redos.append(coord)
        self.draw_stone(coord, empty, -1)

    def undo_all(self):
        if not self.coords:
            return
        self.id = 1
        self.turn = black_stone
        while self.coords:
            coord = self.coords.pop()
            self.redos.append(coord)
        self.init_board()
        self.draw_board()

    def redo(self):
        if not self.redos:
            return
        coord = self.redos.pop()
        self.coords.append(coord)
        self.draw_stone(coord, self.turn, 1)

    def set_coords(self):
        for y in range(board_size):
            for x in range(board_size):
                self.pixel_coords.append((x * grid_size + 25, y * grid_size + 25))

    def get_coord(self, pos):
        for coord in self.pixel_coords:
            x, y = coord
            rect = pygame.Rect(x, y, grid_size, grid_size)
            if rect.collidepoint(pos):
                return coord
        return None

    def get_point(self, coord):
        x, y = coord
        x = (x - 25) // grid_size
        y = (y - 25) // grid_size
        return x, y

    def check_board(self, pos):
        coord = self.get_coord(pos)
        if not coord:
            return False
        x, y = self.get_point(coord)
        if self.board[y][x] != empty:
            return True

        self.coords.append(coord)
        self.draw_stone(coord, self.turn, 1)
        if self.check_gameover(coord, 3 - self.turn):
            self.is_gameover = True
        if len(self.redos):
            self.redos = []
        return True

    def check_gameover(self, coord, stone):
        x, y = self.get_point(coord)
        if self.id > board_size * board_size:
            self.show_winner_msg(stone)
            return
        elif 5 <= self.rule.is_gameover(x, y, stone):
            self.show_winner_msg(stone)
            return True
        return False

    def show_winner_msg(self, stone):
        for i in range(3):
            self.menu.show_msg(stone)
            pygame.display.update()
            pygame.time.delay(200)
            self.menu.show_msg(empty)
            pygame.display.update()
            pygame.time.delay(200)
        self.menu.show_msg(stone)

class Menu(object):
    def __init__(self, surface):
        self.font = pygame.font.Font('fonts/ELAND_Choice_M.ttf', 20)
        self.surface = surface
        self.draw_menu()
        self.omok = None
        self.button = None

    def draw_menu(self):
        top, left = window_height - 30, window_width - 200
        self.back_rect = self.make_text(self.font, 'Back', blue, None, top - 180, left)
        self.new_rect = self.make_text(self.font, 'New Game', blue, None, top - 30, left)
        self.quit_rect = self.make_text(self.font, 'Quit Game', blue, None, top, left)
        self.show_rect = self.make_text(self.font, 'Hide Number  ', blue, None, top - 60, left)
        self.undo_rect = self.make_text(self.font, 'Undo', blue, None, top - 150, left)
        self.uall_rect = self.make_text(self.font, 'Undo All', blue, None, top - 120, left)
        self.redo_rect = self.make_text(self.font, 'Redo', blue, None, top - 90, left)

    def show_msg(self, msg_id):
        msg = {
            empty: '                                    ',
            black_stone: 'Black win!!!',
            white_stone: 'White win!!!',
            tie: 'Tie',
        }
        center_x = window_width - (window_width - board_width) // 2
        self.make_text(self.font, msg[msg_id], black, bg_color, 30, center_x, 1)

    def make_text(self, font, text, color, bgcolor, top, left, position=0, textview=None):
        if textview is None:
            surf = font.render(text, False, color, bgcolor)
            rect = surf.get_rect()
            # print("rect : ", rect.__class__)
            if position:
                rect.center = (left, top)
            else:
                rect.topleft = (left, top)
            self.surface.blit(surf, rect)
            return rect
        else:
            textview.setText(text)
            textview.setTextColor(color)
            textview.setTextPosition((left, top))
            textview.showText()

    def set_omok(self, omok):
        self.omok = omok

    def set_button(self, button):
        self.button = button

    def show_hide(self, omok=None):
        global is_show
        top, left = window_height - 90, window_width - 200
        # todo : flicking(show/hide 번갈아 표시되는 것) 현상 제거하기
        if omok is None:
            if self.omok.is_show:
                self.omok.is_show = False
                is_show = False
                self.omok.hide_numbers()
            elif not self.omok.is_show:
                self.omok.is_show = True
                is_show = True
                self.omok.show_numbers()
        else:
            if omok.is_show:
                self.make_text(self.font, 'Show Number', blue, bg_color, top, left)
                omok.hide_numbers()
                omok.is_show = False
            else:
                self.make_text(self.font, 'Hide Number  ', blue, bg_color, top, left)
                omok.show_numbers()
                omok.is_show = True

    def check_rect(self, pos, omok):
        if self.new_rect.collidepoint(pos):
            return True
        elif self.show_rect.collidepoint(pos):
            self.show_hide(omok)
        elif self.undo_rect.collidepoint(pos):
            omok.undo()
        elif self.uall_rect.collidepoint(pos):
            omok.undo_all()
        elif self.redo_rect.collidepoint(pos):
            omok.redo()
        elif self.quit_rect.collidepoint(pos):
            self.terminate()
        elif self.back_rect.collidepoint(pos):
            self.back()
        return False

    def back(self):
        selectGame()

    def terminate(self):
        pygame.quit()
        sys.exit()

    def is_continue(self, omok):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == MOUSEBUTTONUP:
                    if self.check_rect(event.pos, omok):
                        return
            pygame.display.update()
            fps_clock.tick(fps)


board_size = 15
empty = 0
black_stone = 1
white_stone = 2
last_b_stone = 3
last_a_stont = 4
tie = 100


class Rule(object):
    def __init__(self, board):
        self.board = board

    def is_invalid(self, x, y):
        return x < 0 or x >= board_size or y < 0 or y >= board_size

    def is_gameover(self, x, y, stone):
        x1, y1 = x, y
        list_dx = [-1, 1, -1, 1, 0, 0, 1, -1]
        list_dy = [0, 0, -1, 1, -1, 1, -1, 1]
        for i in range(0, len(list_dx), 2):
            cnt = 1
            for j in range(i, i + 2):
                dx, dy = list_dx[j], list_dy[j]
                x, y = x1, y1
                while True:
                    x, y = x + dx, y + dy
                    if self.is_invalid(x, y) or self.board[y][x] != stone:
                        break
                    else:
                        cnt += 1
            if cnt >= 5:
                return cnt
        return cnt


if __name__ == "__main__":
    initGame()
