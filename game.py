import board
import pygame


class Game:
    """docstring for Game"""
    def __init__(self, screen, tc_start, w_name='undefined',
                 b_name='undefined', tc_type='n', tc_add=0):
        self.screen = screen
        self.white = w_name
        self.black = b_name
        self.tc_type = tc_type
        self.white_color = 0xf0d9b5
        self.black_color = 0xb58863
        self.tc_add = tc_add
        self.w_time = tc_start
        self.b_time = tc_start
        self.board = board.Board()

    def draw_board(self, pos, cell_size, side='w'):
        for i in range(8):
            for j in range(8):
                color = None
                if i % 2 == j % 2:
                    color = self.white_color
                else:
                    color = self.black_color
                pygame.draw.rect(self.screen, color,
                                 (pos[0] + cell_size*j,
                                  pos[1] + cell_size*i,
                                  cell_size, cell_size))
