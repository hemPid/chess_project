class Board:
    """docstring for Board"""
    def __init__(self):
        self.figs = {"white": {
                     "p1": "a2",
                     "p2": "b2",
                     "p3": "c2",
                     "p4": "d2",
                     "p5": "e2",
                     "p6": "f2",
                     "p7": "g2",
                     "p8": "h2",
                     "r1": "a1",
                     "r2": "h1",
                     "n1": "b1",
                     "n2": "g1",
                     "b1": "c1",
                     "b2": "f1",
                     "q": "d1",
                     "k": "e1"
                     },
                     "black": {
                     "p1": "a7",
                     "p2": "b7",
                     "p3": "c7",
                     "p4": "d7",
                     "p5": "e7",
                     "p6": "f7",
                     "p7": "g7",
                     "p8": "h7",
                     "r1": "a8",
                     "r2": "h8",
                     "n1": "b8",
                     "n2": "g8",
                     "b1": "c8",
                     "b2": "f8",
                     "q": "d8",
                     "k": "e8"
                     }}
        self.short_castle_aviliable = {'white': True, 'black': True}
        self.long_castle_aviliable = {'white': True, 'black': True}

    def parse_cell_to_coords(self, pos):
        return (ord(pos[0]) - ord('a'), int(pos[1]) - 1)

    def parse_coords_to_cell(self, coords):
        if coords[0] < 0 or coords[0] > 7 or coords[1] < 0 or coords[1] > 7:
            return False
        return chr(coords[0] + ord('a')) + str(coords[1] + 1)

    def get_fields_fig(self, field):
        res = False
        for side in self.figs:
            for fig in self.figs[side]:
                if self.figs[side][fig] == field:
                    res = {'side': side, 'fig': fig}
        return res

    def move(self, side, fig, field):
        f = self.get_fields_fig(field)
        if f:
            self.figs[f['side']][f['fig']] = '0'
        if fig == 'k':
            self.short_castle_aviliable[side] = False
            self.long_castle_aviliable[side] = False
            if side == 'white':
                if field == 'g1':
                    self.figs[side]['r2'] = 'f1'
                if field == 'c1':
                    self.figs[side]['r1'] = 'd1'
            else:
                if field == 'g8':
                    self.figs[side]['r2'] = 'f8'
                if field == 'c8':
                    self.figs[side]['r1'] = 'd8'
        if fig[0] == 'r':
            if fig[1] == '1':
                self.long_castle_aviliable[side] = False
            else:
                self.short_castle_aviliable[side] = False
        self.figs[side][fig] = field

    def get_moves(self, side, fig):
        field = self.figs[side][fig]
        av_cells = self.get_aviliable_cells(side, fig)
        res = []
        for move in av_cells:
            f = self.get_fields_fig(move)
            self.figs[side][fig] = move
            if f:
                self.figs[f['side']][f['fig']] = '0'
            if not self.is_check(side):
                if not f or f['fig'] != 'k':
                    res.append(move)
            self.figs[side][fig] = field
            if f:
                self.figs[f['side']][f['fig']] = move
        if fig[0] == 'k':
            if side == 'white' and\
               'g1' in res and\
               ('f1' not in res or self.is_check(side) or\
               not self.short_castle_aviliable[side]):
                res.remove('g1')
            if side == 'white' and\
               'c1' in res and\
               ('d1' not in res or self.is_check(side) or\
               not self.long_castle_aviliable[side]):
                res.remove('c1')
            if side == 'black' and\
               'g8' in res and\
               ('f8' not in res or self.is_check(side) or\
               not self.short_castle_aviliable[side]):
                res.remove('g8')
            if side == 'black' and\
               'c8' in res and\
               ('d8' not in res or self.is_check(side) or\
               not self.long_castle_aviliable[side]):
                res.remove('c8')
        return res

    def is_check(self, side):
        king_field = self.figs[side]['k']
        opposite_side = 'black'
        if side == 'black':
            opposite_side = 'white'
        for fig in self.figs[opposite_side]:
            if king_field in self.get_aviliable_cells(opposite_side, fig):
                return True
        return False

    def is_mate(self, side):
        if not self.is_check(side):
            return False
        for fig in self.figs[side]:
            if len(self.get_moves(side, fig)):
                return False
        return True

    def is_draw(self, side):
        if not self.is_check(side):
            flag = True
            for fig in self.figs[side]:
                if len(self.get_moves(side, fig)):
                    flag = False
            if flag:
                return True
            for sd in self.figs:
                aviliable_figs = []
                for fig in self.figs[sd]:
                    if self.figs[sd][fig] != '0':
                        aviliable_figs.append(fig[0])
                if len(aviliable_figs) > 2:
                    return False
                if 'q' in aviliable_figs or 'r' in aviliable_figs or 'p' in aviliable_figs:
                    return False
            return True
        return False

    def get_aviliable_cells(self, side, fig):
        if fig[0] == 'p':
            # pawn
            return self.get_aviliable_cells_pawn(side, fig)
        elif fig[0] == 'n':
            return self.get_aviliable_cells_knight(side, fig)
        elif fig[0] == 'b':
            return self.get_aviliable_cells_bishop(side, fig)
        elif fig[0] == 'r':
            return self.get_aviliable_cells_rook(side, fig)
        elif fig[0] == 'q':
            return self.get_aviliable_cells_queen(side)
        elif fig[0] == 'k':
            return self.get_aviliable_cells_king(side)
        else:
            return None

    def get_aviliable_cells_pawn(self, side, fig):
        fig_pos = self.figs[side][fig]
        if fig_pos == '0':
            return []
        fig_coords = self.parse_cell_to_coords(fig_pos)
        res = []
        possible_fields = []
        opposite_side = 'black'
        start_position = 1
        if side == 'white':
            possible_coords = [(fig_coords[0] + 1, fig_coords[1] + 1),
                               (fig_coords[0] - 1, fig_coords[1] + 1),
                               (fig_coords[0], fig_coords[1] + 1),
                               (fig_coords[0], fig_coords[1] + 2)]
        else:
            possible_coords = [(fig_coords[0] + 1, fig_coords[1] - 1),
                               (fig_coords[0] - 1, fig_coords[1] - 1),
                               (fig_coords[0], fig_coords[1] - 1),
                               (fig_coords[0], fig_coords[1] - 2)]
            opposite_side = 'white'
            start_position = 6
        possible_fields = list(map(self.parse_coords_to_cell, possible_coords))
        # case 1
        if possible_fields[0]:
            fig1 = self.get_fields_fig(possible_fields[0])
            if fig1 and fig1['side'] == opposite_side:
                res.append(possible_fields[0])
        # case 2
        if possible_fields[1]:
            fig2 = self.get_fields_fig(possible_fields[1])
            if fig2 and fig2['side'] == opposite_side:
                res.append(possible_fields[1])
        # case 3
        if possible_fields[2]:
            fig3 = self.get_fields_fig(possible_fields[2])
            if not fig3:
                res.append(possible_fields[2])
        # case 4
        if possible_fields[3]:
            fig4 = self.get_fields_fig(possible_fields[3])
            if not fig4 and not fig3 and fig_coords[1] == start_position:
                res.append(possible_fields[3])
        return res

    def get_aviliable_cells_knight(self, side, fig):
        fig_pos = self.figs[side][fig]
        if fig_pos == '0':
            return []
        fig_coords = self.parse_cell_to_coords(fig_pos)
        res = []
        possible_fields = []
        opposite_side = 'black'
        if side == 'black':
            opposite_side = 'white'
        possible_coords = []
        possible_adds = (-2, -1, 1, 2)
        for add_x in possible_adds:
            for add_y in possible_adds:
                if abs(add_x) == abs(add_y) or\
                   fig_coords[0] + add_x < 0 or\
                   fig_coords[0] + add_x > 7 or\
                   fig_coords[1] + add_y < 0 or\
                   fig_coords[1] + add_y > 7:
                    continue
                possible_coords.append((fig_coords[0] + add_x,
                                        fig_coords[1] + add_y))
        possible_fields = list(map(self.parse_coords_to_cell, possible_coords))
        for field in possible_fields:
            f = self.get_fields_fig(field)
            if not f or f['side'] == opposite_side:
                res.append(field)
        return res

    def get_aviliable_cells_bishop(self, side, fig):
        fig_pos = self.figs[side][fig]
        if fig_pos == '0':
            return []
        fig_coords = self.parse_cell_to_coords(fig_pos)
        res = []
        opposite_side = 'black'
        if side == 'black':
            opposite_side = 'white'
        directions = [[True, True], [True, True]]
        k = 1
        while True in directions[0] or True in directions[1]:
            for i in range(2):
                sign1 = (-1) ** i
                for j in range(2):
                    sign2 = (-1) ** j
                    if directions[i][j]:
                        coords = (fig_coords[0] + sign1 * k,
                                  fig_coords[1] + sign2 * k)
                        if coords[0] < 0 or\
                           coords[0] > 7 or\
                           coords[1] < 0 or\
                           coords[1] > 7:
                            directions[i][j] = False
                        else:
                            field = self.parse_coords_to_cell(coords)
                            f = self.get_fields_fig(field)
                            if not f:
                                res.append(field)
                            elif f['side'] == opposite_side:
                                res.append(field)
                                directions[i][j] = False
                            else:
                                directions[i][j] = False
            k += 1
        return res

    def get_aviliable_cells_rook(self, side, fig):
        fig_pos = self.figs[side][fig]
        if fig_pos == '0':
            return []
        fig_coords = self.parse_cell_to_coords(fig_pos)
        res = []
        opposite_side = 'black'
        if side == 'black':
            opposite_side = 'white'
        directions = [[True, True], [True, True]]
        k = 1
        while True in directions[0] or True in directions[1]:
            for i in range(2):
                for j in range(2):
                    sign = (-1) ** j
                    if directions[i][j]:
                        if not i:
                            coords = (fig_coords[0] + sign*k,
                                      fig_coords[1])
                        else:
                            coords = (fig_coords[0],
                                      fig_coords[1] + sign*k)
                        if coords[0] < 0 or\
                           coords[0] > 7 or\
                           coords[1] < 0 or\
                           coords[1] > 7:
                            directions[i][j] = False
                        else:
                            field = self.parse_coords_to_cell(coords)
                            f = self.get_fields_fig(field)
                            if not f:
                                res.append(field)
                            elif f['side'] == opposite_side:
                                res.append(field)
                                directions[i][j] = False
                            else:
                                directions[i][j] = False
            k += 1
        return res

    def get_aviliable_cells_queen(self, side):
        fig_pos = self.figs[side]['q']
        if fig_pos == '0':
            return []
        fig_coords = self.parse_cell_to_coords(fig_pos)
        res = []
        opposite_side = 'black'
        if side == 'black':
            opposite_side = 'white'
        directions = [[True, True, True],
                      [True, False, True],
                      [True, True, True]]
        signs = [-1, 0, 1]
        k = 1
        while True in directions[0] or\
                True in directions[1] or\
                True in directions[2]:
            for i in range(3):
                for j in range(3):
                    if i == 1 and j == 1:
                        continue
                    if directions[i][j]:
                        coords = (fig_coords[0] + signs[i]*k,
                                  fig_coords[1] + signs[j]*k)
                        if coords[0] < 0 or\
                           coords[0] > 7 or\
                           coords[1] < 0 or\
                           coords[1] > 7:
                            directions[i][j] = False
                        else:
                            field = self.parse_coords_to_cell(coords)
                            f = self.get_fields_fig(field)
                            if not f:
                                res.append(field)
                            elif f['side'] == opposite_side:
                                res.append(field)
                                directions[i][j] = False
                            else:
                                directions[i][j] = False
            k += 1
        return res

    def get_aviliable_cells_king(self, side):
        fig_pos = self.figs[side]['k']
        fig_coords = self.parse_cell_to_coords(fig_pos)
        res = []
        opposite_side = 'black'
        if side == 'black':
            opposite_side = 'white'
        adds = [-1, 0, 1]
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    continue
                coords = (fig_coords[0] + adds[i],
                          fig_coords[1] + adds[j])
                if coords[0] < 0 or\
                   coords[0] > 7 or\
                   coords[1] < 0 or\
                   coords[1] > 7:
                    continue
                else:
                    field = self.parse_coords_to_cell(coords)
                    f = self.get_fields_fig(field)
                    if not f or f['side'] == opposite_side:
                        res.append(field)
        if self.short_castle_aviliable:
            if side == 'white' and\
               not self.get_fields_fig('f1') and\
               not self.get_fields_fig('g1'):
                res.append('g1')
            if side == 'black' and\
               not self.get_fields_fig('f8') and\
               not self.get_fields_fig('g8'):
                res.append('g8')
        if self.long_castle_aviliable:
            if side == 'white' and\
               not self.get_fields_fig('b1') and\
               not self.get_fields_fig('c1') and\
               not self.get_fields_fig('d1'):
                res.append('c1')
            if side == 'black' and\
               not self.get_fields_fig('b8') and\
               not self.get_fields_fig('c8') and\
               not self.get_fields_fig('d8'):
                res.append('c8')
        return res
