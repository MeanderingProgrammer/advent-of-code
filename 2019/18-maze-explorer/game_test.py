import sys
import pygame
from pygame.locals import KEYDOWN, K_q

SCREENSIZE = WIDTH, HEIGHT = 600, 400
BLACK = (0, 0, 0)
GREY = (160, 160, 160)


def main():
    pygame.init()
    surface = pygame.display.set_mode(SCREENSIZE)

    while True:
        check_events()
        surface.fill(GREY)
        draw_line(surface)
        pygame.display.update()


def draw_line(surface):
    pygame.draw.line(surface, BLACK, (0, 0), (WIDTH, HEIGHT), 2)


def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    main()
