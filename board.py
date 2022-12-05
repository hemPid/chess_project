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


    def is_move_aviliable(self, move):
        pass

    def move(self, mv):
        pass

    def is_check(self, side):
        pass

    def is_castle_aviliable(self, side):
        pass

    def is_mate(self, side):
        pass

    def get_aviliable_cells(self, side, fig):
        if fig[0] == 'p':
            # pawn
            pass

    def get_aviliable_cells_pawn(self, side, fig):
        fig_pos = self.figs[side][fig]
        fig_coords = self.parse_cell_to_coords(fig_pos)
        res = []
        possible_fields = []
        oposite_side = 'black'
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
            oposite_side = 'white'
            start_position = 6
        possible_fields = list(map(self.parse_coords_to_cell, possible_coords))
        # case 1
        if possible_fields[0]:
            fig1 = self.get_fields_fig(possible_fields[0])
            if fig1 and fig1['side'] == oposite_side:
                res.append(possible_fields[0])
        # case 2
        if possible_fields[1]:
            fig2 = self.get_fields_fig(possible_fields[1])
            if fig2 and fig2['side'] == oposite_side:
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
        fig_coords = self.parse_cell_to_coords(fig_pos)
        res = []
        possible_fields = []
        oposite_side = 'black'
        if side == 'black':
            oposite_side = 'white'
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
                possible_coords.append((fig_coords[0] + add_x, fig_coords[1] + add_y))
        possible_fields = list(map(self.parse_coords_to_cell, possible_coords))
        for field in possible_fields:
            f = self.get_fields_fig(field)
            if not f or f['side'] == oposite_side:
                res.append(field)
        return res

    def get_aviliable_cells_bishop(self, side, fig):
        fig_pos = self.figs[side][fig]
        fig_coords = self.parse_cell_to_coords(fig_pos)
        res = []
        oposite_side = 'black'
        if side == 'black':
            oposite_side = 'white'
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
                            elif f['side'] == oposite_side:
                                res.append(field)
                                directions[i][j] = False
                            else:
                                directions[i][j] = False
            k += 1
        return res

    def get_aviliable_cells_rook(self, side, fig):
        fig_pos = self.figs[side][fig]
        fig_coords = self.parse_cell_to_coords(fig_pos)
        res = []
        oposite_side = 'black'
        if side == 'black':
            oposite_side = 'white'
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
                            elif f['side'] == oposite_side:
                                res.append(field)
                                directions[i][j] = False
                            else:
                                directions[i][j] = False
            k += 1
        return res
    def get_aviliable_cells_queen(self, side, fig):
        fig_pos = self.figs[side][fig]
        fig_coords = self.parse_cell_to_coords(fig_pos)
        res = []
        oposite_side = 'black'
        if side == 'black':
            oposite_side = 'white'
        directions = [[True, True, True],
                      [True, False, True],
                      [True, True, True]]
        signs = [-1, 0, 1]
        k = 1
        while True in directions[0] or True in directions[1] or True in directions[2]:
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
                            elif f['side'] == oposite_side:
                                res.append(field)
                                directions[i][j] = False
                            else:
                                directions[i][j] = False
            k += 1
        return res
