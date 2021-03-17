import sys
import pygame
import math
from pygame.locals import *
from Window import window_width, window_height, window_center_x, window_center_y
from ImageView import resizeImage
from Button import Button

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
displaywin = pygame.display.set_mode((window_width, window_height))
bag = pygame.image.load("images/randomNumberImages/bag_186x218.png")
bag_width, bag_height = bag.get_size()
bag_update_string = resizeImage("images/randomNumberImages", "bag", int(bag_width * 1.5), int(bag_height * 1.5), 1)
bag = pygame.image.load(bag_update_string)


def mixAnimation():
    for step in range(360):
        displaywin.fill(BGCOLOR)
        # 움직이는 공을 그립니다. math.sin()
        yPos = -1 * math.sin(7 * step * math.pi / 180) * AMPLITUDE
        # 푸른색 공을 그려줍니다.
        displaywin.blit(bag, (int(window_width / 3), int(yPos) + int(window_height / 8)))
        # 디스플레이 업데이트 해준다.
        pygame.display.update()
    for step in range(360):
        displaywin.fill(BGCOLOR)
        # 움직이는 공을 그립니다. math.sin()
        xPos = -1 * math.sin(7 * step * math.pi / 180) * AMPLITUDE
        # 푸른색 공을 그려줍니다.
        displaywin.blit(bag, (int(xPos) + int(window_width / 3), int(window_height / 8)))
        # 디스플레이 업데이트 해준다.
        pygame.display.update()


# 메인 루프
while True:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    # 배경을 칠합니다.
    displaywin.fill(BGCOLOR)
    mix_button = Button(displaywin, "숫자 구슬 섞기", 20, (0, 0, 0), (3, int(window_height / 7)), (200, 60), (0, 255, 0), (0, 255, 100), 4)
    mix_button.onClickListener(mixAnimation)
    displaywin.blit(bag, (int(window_width / 3), int(window_height / 8)))

    pygame.display.update()
    FPSCLOCK.tick(FPS)


