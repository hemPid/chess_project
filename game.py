class Game:
    """docstring for Game"""
    def __init__(self, screen, w_name, b_name, tc_type, tc_add, tc_start):
        self.screen = screen
        self.white = w_name
        self.black = b_name
        self.tc_type = tc_type
        self.tc_add = tc_add
        self.w_time = tc_start
        self.b_time = tc_start
        self.board = Board()
    
    def draw_board(side):
        pass
