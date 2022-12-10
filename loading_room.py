import pygame
import game_type_choice
import connection

class waiting_room_window:
    """docstring for witing_room_window"""
    def __init__(self, screen, data):
        self.screen = screen
        self.data = data
        self.finished = False
        self.next_stage = None
        self.screen.fill((255, 255, 255))
        # drawing text and quit button
        self.button_font = pygame.font.SysFont('arial', 40, True)
        self.text_font = pygame.font.SysFont('arial', 50, True)
        self.text_rend = self.text_font.\
            render('waiting for someone to connect', True, (0, 0, 0))
        self.screen.blit(self.text_rend, (100, 100))
        self.but_text_rend = self.button_font.\
            render('quit', True, (0, 0, 0))
        self.buttons_color = (243, 194, 105)
        self.quit_but = pygame.draw.\
            rect(self.screen, self.buttons_color,
                 (100, 200,
                  self.but_text_rend.get_width() + 10,
                  self.but_text_rend.get_height() + 10))
        self.screen.blit(self.but_text_rend, (105, 205))
        # forming connection
        self.con = connection.Connection('waiting_room', self.data['name'], self.msg_listener, self.introduce)
        self.con.connect()
        self.data_to_send = self.data.copy()
        self.data_to_send['msg_type'] = 'introduction'

    def loop(self, dt):
        pass

    def ev(self, events, dt):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.quit_but.collidepoint(event.pos):
                    self.remove()
                    self.con.disconnect()
                    self.finished = True
                    self.data = {'name': self.data['name']}
                    self.next_stage = game_type_choice.game_type_choice_window

    def introduce(self):
        self.con.write(self.data_to_send)

    def remove(self):
        self.con.write({'msg_type': 'remove', 'name': self.data['name']})

    def msg_listener(self, message):
        print(message.message)
        if message.message['msg_type'] == 'request':
            self.introduce()