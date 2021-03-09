import pygame
import sys
from TextView import TextView
from Button import Button


def test():
    # pygame 초기화
    pygame.init()

    # 스크린 객체 저장
    screen = pygame.display.set_mode((512, 512))
    pygame.display.set_caption("Game")

    # 게임 시간을 위한 Clock 생성
    clock = pygame.time.Clock()

    while True:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 스크린 배경색 칠하기
        screen.fill((255, 255, 255))

        text = TextView(screen, "테스트", "fonts/ELAND_Choice_M.ttf", 100, (0, 0, 0), (512//2, 512//2), (255, 0, 255))
        text.showText()
        button = Button(screen, '테슬라', 50, (0, 0, 0), (512//2, 512//10), (200, 100), (255, 0, 0), (0, 255, 0), 10)
        button.onClickListener()
        # 작업한 내용 갱신하기
        pygame.display.flip()

        # 1초에 60번의 빈도로 순환하기
        clock.tick(60)


test()
