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
        self.bd = board.Board()

    def draw_board(self, pos, cell_size, side='w'):
        # drawing cells
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
        # drawing figures
        for sd in self.bd.figs:
            for fig in self.bd.figs[sd]:
                fig_surf = pygame.\
                           image.\
                           load('models\\' + sd + '_' + fig[0] + '.png').\
                           convert_alpha()
                fig_im = pygame.transform.scale(fig_surf,
                                                (cell_size, cell_size))
                fig_pos_x = 0
                fig_pos_y = 0
                fig_crd_x = self.bd.figs[sd][fig][0]
                fig_crd_y = int(self.bd.figs[sd][fig][1])
                if side == 'w':
                    fig_pos_x = (ord(fig_crd_x) - ord('a'))\
                                * cell_size + pos[0]
                    fig_pos_y = (8 - fig_crd_y) * cell_size + pos[1]
                else:
                    fig_pos_x = (ord('h') - ord(fig_crd_x))\
                                * cell_size + pos[0]
                    fig_pos_y = (fig_crd_y - 1) * cell_size + pos[1]
                self.screen.blit(fig_im, (fig_pos_x, fig_pos_y))
