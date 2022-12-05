import pygame
import board


class single_game_window:
    """docstring for single_game_window"""
    def __init__(self, screen, data):
        self.screen = screen
        self.data = data
        self.finished = False
        self.next_stage = None
        self.white_color = 0xf0d9b5
        self.black_color = 0xb58863
        self.board_pos_x = 50
        self.board_pos_y = 50
        self.cell_size = 80
        self.bd = board.Board()
        self.current_move = 'w'
        self.select_fields = []
        time = int(data['tc'].split(' + ')[0])
        print(time)
        self.white_time = time*60*1000
        self.black_time = time*60*1000
        self.add = int(data['tc'].split(' + ')[1])
        self.timer_font = pygame.font.SysFont('arial', 40, True)

    def loop(self, dt):
        self.screen.fill((255, 255, 255))
        self.draw_board((self.board_pos_x, self.board_pos_y), self.cell_size, self.current_move)
        for f in self.select_fields:
            self.select_field(f)
        if self.current_move == 'w':
            self.white_time -= dt
        else:
            self.black_time -= dt
        self.draw_timer()

    def ev(self, events, dt):
        pass

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

    def get_field_coords(self, field):
        pos = field
        coord_x = 0
        coord_y = 0
        if self.current_move == 'w':
            coord_x = self.board_pos_x + self.cell_size*(ord(pos[0]) - ord('a'))
            coord_y = self.board_pos_y + self.cell_size*(8 - int(pos[1]))
        else:
            coord_x = self.board_pos_x + self.cell_size*(ord('h') - ord(pos[0]))
            coord_y = self.board_pos_y + self.cell_size*(int(pos[1]) - 1)
        return (coord_x, coord_y)

    def select_field(self, field):
        cell_pos = self.get_field_coords(field)
        surf = pygame.Surface((self.cell_size, self.cell_size))
        surf.set_alpha(90)
        pygame.draw.circle(surf, (0, 255, 0), (self.cell_size // 2, self.cell_size // 2), self.cell_size*0.2)
        self.screen.blit(surf, cell_pos)

    def parse_time(self, time):
        time_minutes = time // (60*1000)
        time_seconds = (time % (60*1000)) // 1000
        res = ''
        if time_minutes < 10:
            res += '0'
        res += str(time_minutes) + ':'
        if time_seconds < 10:
            res += '0'
        res += str(time_seconds)
        return res

    def draw_timer(self):
        white_time_str = self.parse_time(self.white_time)
        black_time_str = self.parse_time(self.black_time)
        black_time_rendered_text = self.timer_font.render(black_time_str, True, (0,0,0))
        white_time_rendered_text = self.timer_font.render(white_time_str, True, (0,0,0))
        white_timer_coords = (0, 0)
        black_timer_coords = (0, 0)
        if self.current_move == 'w':
            white_timer_coords = (self.board_pos_x + self.cell_size*8 + 10, self.board_pos_y + self.cell_size*7)
            black_timer_coords = (self.board_pos_x + self.cell_size*8 + 10, self.board_pos_y)
        else:
            black_timer_coords = (self.board_pos_x + self.cell_size*8 + 10, self.board_pos_y + self.cell_size*7)
            white_timer_coords = (self.board_pos_x + self.cell_size*8 + 10, self.board_pos_y)
        self.screen.blit(white_time_rendered_text, white_timer_coords)
        self.screen.blit(black_time_rendered_text, black_timer_coords)

