import board
import pygame
import game

def main():
    FPS = 30
    screen_width = 1200
    screen_height = 800
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    finished = False
    screen.fill(0xffffff)
    gm = game.Game(screen, 10)
    while not finished:
        gm.draw_board((20, 20), 90)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

if __name__ == '__main__':
    main()