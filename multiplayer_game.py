import single_game
import pygame
import connection

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

    def ev(self, events, dt):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_mouse_on_board(event) and not self.game_over:
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
                            if self.current_move == 'white':
                                if self.bd.is_mate('black'):
                                    self.endgame('1-0')
                                elif self.bd.is_draw('black'):
                                    self.endgame('0,5-0,5')
                                else:
                                    self.white_time += self.add*1000
                                    self.current_move = 'black'
                            else:
                                if self.bd.is_mate('white'):
                                    self.endgame('0-1')
                                elif self.bd.is_draw('white'):
                                    self.endgame('0,5-0,5')
                                else:
                                    self.black_time += self.add*1000
                                    self.current_move = 'white'
                        self.select_fields = []
                        self.selected_fig = None
                if self.game_over and self.quit_button.collidepoint(event.pos):
                    self.data = {'name': self.data['name']}
                    self.finished = True
                    self.next_stage = game_type_choice.game_type_choice_window
                for but in self.buttons:
                    if self.buttons[but].collidepoint(event.pos):
                        if but == 'resign':
                            if self.current_move == 'white':
                                self.endgame('0-1')
                                break
                            else:
                                self.endgame('1-0')
                                break
                        else:
                            self.endgame('0,5-0,5')
                            break

    def subscribe_event(self):
        print('connected')
        self.con.write(self.data['name'])

    def message_event(self, message):
        print(message.message)