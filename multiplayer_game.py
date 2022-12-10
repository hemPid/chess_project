import single_game
import pygame
import connection
import game_type_choice


class multiplayer_game_window(single_game.single_game_window):
    """docstring for multiplayer_game_window"""
    def __init__(self, screen, data):
        super(multiplayer_game_window, self).__init__(screen, data)
        print('!!!')
        print(data)
        self.con = connection.Connection(self.data['chname'],
                                         self.data['name'],
                                         self.message_event,
                                         self.subscribe_event)
        self.con.connect()
        self.side = self.data['side']
        if self.side == 'white':
            self.op_side = 'black'
        else:
            self.op_side = 'white'

    def send_move(self, fig, field, time):
        self.con.write({
            'type': 'move',
            'fig': fig,
            'field': field,
            'time': time,
            'side': self.side
            })

    def send_result(self, res):
        self.con.write({
            'type': 'result',
            'res': res
            })

    def loop(self, dt):
        self.screen.fill((255, 255, 255))
        self.draw_board((self.board_pos_x, self.board_pos_y),
                        self.cell_size, self.side)
        self.draw_timer(self.side)
        if not self.game_over:
            for f in self.select_fields:
                self.select_field(f)
            self.draw_buttons()
            if self.current_move == 'white':
                self.white_time -= dt
                if self.white_time <= 0:
                    self.white_time = 0
                    if self.side == 'white':
                        self.endgame('0-1')
                        self.send_result('0-1')
            else:
                self.black_time -= dt
                if self.black_time <= 0:
                    self.black_time = 0
                    if self.side == 'black':
                        self.endgame('1-0')
                        self.send_result('1-0')
        else:
            if self.game_over:
                self.draw_quit_button()
                self.draw_result_text()

    def ev(self, events, dt):
        for event in events:
            if event.type == pygame.QUIT:
                self.con.write({'msg_type': 'disconnect'})
                self.con.disconnect()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_mouse_on_board(event) and\
                   not self.game_over and\
                   self.current_move == self.side:
                    field = self.get_mouse_cell(event)
                    if not len(self.select_fields):
                        fig = self.bd.get_fields_fig(field)
                        if fig and fig['side'] == self.current_move:
                            self.select_fields = self.bd.\
                                get_moves(self.current_move, fig['fig'])
                            self.selected_fig = fig['fig']
                    else:
                        if field in self.select_fields:
                            self.bd.move(self.current_move,
                                         self.selected_fig, field)
                            self.history['moves'].\
                                append((self.selected_fig,
                                       field))
                            if self.side == 'white':
                                self.send_move(self.selected_fig,
                                               field,
                                               self.white_time)
                                self.white_time += self.add*1000
                                if self.bd.is_mate('black'):
                                    self.endgame('1-0')
                                elif self.bd.is_draw('black'):
                                    self.endgame('0,5-0,5')
                                else:
                                    self.current_move = 'black'
                            else:
                                self.black_time += self.add*1000
                                self.send_move(self.selected_fig,
                                               field,
                                               self.black_time)
                                if self.bd.is_mate('white'):
                                    self.endgame('0-1')
                                elif self.bd.is_draw('white'):
                                    self.endgame('0,5-0,5')
                                else:
                                    self.current_move = 'white'
                        self.select_fields = []
                        self.selected_fig = None
                if self.game_over and self.quit_button.collidepoint(event.pos):
                    self.data = {'name': self.data['name']}
                    self.finished = True
                    self.con.disconnect()
                    self.next_stage = game_type_choice.game_type_choice_window
                for but in self.buttons:
                    if self.buttons[but].collidepoint(event.pos):
                        if but == 'resign':
                            if self.side == 'white':
                                self.send_result('0-1')
                                self.endgame('0-1')
                                break
                            else:
                                self.send_result('1-0')
                                self.endgame('1-0')
                                break
                        else:
                            self.send_result('0,5-0,5')
                            self.endgame('0,5-0,5')
                            break

    def subscribe_event(self):
        print('connected')

    def message_event(self, message):
        print(message.message)
        if message.message['type'] == 'move' and\
           message.message['side'] != self.side:
            self.bd.move(message.message['side'],
                         message.message['fig'],
                         message.message['field'])
            self.history['moves'].\
                append((message.message['fig'],
                       message.message['field']))
            if self.side == 'black':
                self.white_time = message.message['time']
                if self.bd.is_mate('black'):
                    self.endgame('1-0')
                elif self.bd.is_draw('black'):
                    self.endgame('0,5-0,5')
                else:
                    self.current_move = 'black'
            else:
                self.black_time = message.message['time']
                if self.bd.is_mate('white'):
                    self.endgame('0-1')
                elif self.bd.is_draw('white'):
                    self.endgame('0,5-0,5')
                else:
                    self.current_move = 'white'
        if message.message['type'] == 'result':
            print('resigned')
            print(message.message)
            self.endgame(message.message['res'])
        if message.message['type']:
            pass
