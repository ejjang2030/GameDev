import sys
import pygame
import math
from pygame.locals import *
from Window import window_width, window_height, window_center_x, window_center_y
from ImageView import resizeImage
from Button import Button
from EditText import EditText

BRIGHTBLUE = (0, 50, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BGCOLOR = WHITE

# 초당 프레임 수 : 많을 수록 빠르다
# FRAME PER SECOND
FPS = 120
AMPLITUDE = 30
# 기본 시작 셋업
pygame.init()
FPSCLOCK = pygame.time.Clock()
surface = pygame.display.set_mode((window_width, window_height))

bag = pygame.image.load("images/randomNumberImages/bag_186x218.png")
bag_width, bag_height = bag.get_size()
bag_update_string = resizeImage("images/randomNumberImages", "bag", int(bag_width * 1.5), int(bag_height * 1.5), 1)
bag = pygame.image.load(bag_update_string)
bag_width, bag_height = bag.get_size()
bag_pos_x = int(window_width / 3)
bag_pos_y = int(window_height / 8)

marvel = pygame.image.load("images/randomNumberImages/marvel.png")
marvel_width, marvel_height = marvel.get_size()
marvel_update_string = resizeImage("images/randomNumberImages", "marvel", int(marvel_width / 3), int(marvel_height / 3), 1)
marvel = pygame.image.load(marvel_update_string)
marvel_width, marvel_height = marvel.get_size()

marvel_start_point = (int(bag_pos_x + bag_width / 2), int(bag_pos_y))
marvel_end_point = (int(window_width / 5), 2000)
show_marvel = False


# edittext

color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('orange')

def marvelAnimation():
    global latest_marvel_pos_x, latest_marvel_pos_y
    surface.fill(BGCOLOR)
    surface.blit(bag, (int(window_width / 3), int(window_height / 8)))
    for x in range(marvel_start_point[0], marvel_end_point[0], -1):
        surface.blit(bag, (int(window_width / 3), int(window_height / 8)))
        a = 4
        a1 = int((marvel_end_point[1] - marvel_start_point[1]) / (marvel_end_point[0] ** 2 - marvel_start_point[0] ** 2))
        b = 440
        c = marvel_start_point[1] - (marvel_start_point[0] ** 2) * a1
        y = int(a * ((x - b) ** 2) + c)
        y /= window_height
        surface.fill(BGCOLOR)
        showBag()
        surface.blit(marvel, (x, y))
        latest_marvel_pos_x, latest_marvel_pos_y = x, y
        pygame.display.update()


def showMarvel():
    global latest_marvel_pos_x, latest_marvel_pos_y
    surface.blit(marvel, (latest_marvel_pos_x, latest_marvel_pos_y))


def showBag():
    surface.blit(bag, (int(window_width / 3), int(window_height / 8)))


def mixAnimation():
    for step in range(360):
        surface.fill(BGCOLOR)
        # 움직이는 공을 그립니다. math.sin()
        yPos = -1 * math.sin(7 * step * math.pi / 180) * AMPLITUDE
        # 푸른색 공을 그려줍니다.
        surface.blit(bag, (bag_pos_x, int(yPos) + bag_pos_y))
        # 디스플레이 업데이트 해준다.
        pygame.display.update()
    for step in range(360):
        surface.fill(BGCOLOR)
        # 움직이는 공을 그립니다. math.sin()
        xPos = -1 * math.sin(7 * step * math.pi / 180) * AMPLITUDE
        # 푸른색 공을 그려줍니다.
        surface.blit(bag, (int(xPos) + bag_pos_x, bag_pos_y))
        # 디스플레이 업데이트 해준다.
        pygame.display.update()


def check():
    edittext.resetInputText()


edittext = EditText(surface, 32, (0, 0, 0), color_passive, color_active, (300, 50), (int((bag_pos_x + bag_width) / 2) - 20, bag_pos_y + bag_height + 50))
# 메인 루프
while True:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        edittext.initEditText(event)

    # 배경을 칠합니다.
    surface.fill(BGCOLOR)

    surface.blit(bag, (int(window_width / 3), int(window_height / 8)))
    mix_button = Button(surface, "숫자 구슬 섞기", 20, (0, 0, 0), (50, int(window_height / 7)), (200, 60), (0, 255, 0), (0, 255, 100), 4)
    mix_button.onClickListener(mixAnimation)
    if mix_button.isButtonClicked():
        show_marvel = False
    show_marvel_button = Button(surface, "구슬 꺼내기", 20, (0, 0, 0), (50, 2 * int(window_height / 7) + 20), (200, 60), (0, 255, 0), (0, 255, 100), 4)
    show_marvel_button.onClickListener(marvelAnimation)
    show_marvel_button.onClickListener(check)
    if show_marvel_button.isButtonClicked():
        show_marvel = True
    if show_marvel:
        showMarvel()
    surface.blit(bag, (int(window_width / 3), int(window_height / 8)))

    edittext.updateTextBoxColor()
    edittext.showEditTextBox()
    edittext.text_box_rect.w = max(100, edittext.text_render.get_width() + 10)

    check_button = Button(surface, "확인", 20, (0, 0, 0), (edittext.text_box_rect.x + edittext.text_box_rect.size[0], edittext.text_box_rect.y), (100, edittext.text_box_rect.size[1] + 1), color_passive, color_active)
    check_button.onClickListener(check)

    pygame.display.update()
    FPSCLOCK.tick(FPS)


