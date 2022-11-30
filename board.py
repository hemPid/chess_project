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

    def is_move_aviliable(move):
        pass

    def move(mv):
        pass

    def is_check(side):
        pass

    def is_castle_aviliable(side):
        pass

    def is_mate(side):
        pass
