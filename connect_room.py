import pygame
import connection
import game_type_choice
import multiplayer_game


class connect_window:
    def __init__(self, screen, data):
        self.screen = screen
        self.data = data
        self.finished = False
        self.waiting_for_response = False
        self.next_stage = None
        self.screen.fill((255, 255, 255))
        self.aviliable_rooms = {}
        self.buttons_color = (243, 194, 105)
        self.con = connection.Connection('waiting_room', self.data['name'], self.msg_listener, self.request)
        self.con.connect()
        self.font = pygame.font.SysFont('arial', 30, True)
        self.list_item_height = 50
        self.list_pos = (100, 50)
        self.button_text = self.font.render('play', True, (0, 0, 0))
        self.empty_text = self.font.render('No games found', True, (0, 0, 0))
        self.quit_text = self.font.render('quit', True, (0,0,0))
        self.quit_but = pygame.draw.\
            rect(self.screen, self.buttons_color,
                 (1000, 50,
                  self.quit_text.get_width() + 4,
                  self.quit_text.get_height() + 2))

    def loop(self, dt):
        self.screen.fill((255, 255, 255))
        self.draw_list()
        pygame.draw.rect(self.screen, self.buttons_color, self.quit_but)
        self.screen.blit(self. quit_text, (1002, 51))

    def ev(self, events, dt):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.waiting_for_response:
                if self.quit_but.collidepoint(event.pos):
                    self.con.disconnect()
                    self.finished = True
                    self.next_stage = game_type_choice.game_type_choice_window
                for name in self.aviliable_rooms:
                    if self.aviliable_rooms[name]['button'].collidepoint(event.pos):
                        self.ask_permisson(name)

    def draw_list(self):
        i = 0
        for name in self.aviliable_rooms:
            data = self.aviliable_rooms[name]
            self.screen.\
                blit(data['rendered_name'],
                     (self.list_pos[0],
                      self.list_pos[1] +\
                      i*self.list_item_height +\
                      (self.list_item_height - data['rendered_name'].get_height()) / 2))
            self.screen.\
                blit(data['rendered_tc'],
                     (self.list_pos[0] + 450,
                      self.list_pos[1] +\
                      i*self.list_item_height +\
                      (self.list_item_height - data['rendered_name'].get_height()) / 2))
            pygame.draw.rect(self.screen, self.buttons_color, data['button'])
            self.screen.\
                blit(self.button_text,
                     (self.list_pos[0] + 702,
                      self.list_pos[1] +\
                      i*self.list_item_height +\
                      (self.list_item_height - self.button_text.get_height()) / 2))
            i += 1
        if not len(self.aviliable_rooms):
            self.screen.blit(self.empty_text, self.list_pos)



    def get_button_coords(self):
        return (self.list_pos[0] + 700,
                self.list_pos[1] + len(self.aviliable_rooms)*self.list_item_height + 2,
                self.button_text.get_width() + 4, self.list_item_height - 4)

    def request(self):
        self.con.write({'msg_type': 'request'})

    def ask_permisson(self, name):
        self.con.write({'msg_type': 'connect', 
                        'name': self.data['name'],
                        'to': name})
        self.waiting_for_response = True

    def msg_listener(self, message):
        if message.message['msg_type'] == 'introduction':
            tc = message.message['tc']
            button = pygame.draw.rect(self.screen, self.buttons_color,
                                      self.get_button_coords())
            rendered_name = self.font.\
                render(message.message['name'], True, (0,0,0))
            rendered_tc = self.font.\
                render(message.message['tc'], True, (0,0,0))
            self.aviliable_rooms[message.message['name']] = {
                'tc': tc,
                'button': button,
                'rendered_name': rendered_name,
                'rendered_tc': rendered_tc
            }
        elif message.message['msg_type'] == 'remove':
            self.aviliable_rooms.pop(message.message['name'])
        elif message.message['msg_type'] == 'confirmation':
            if message.message['to'] == self.data['name']:
                self.data['tc'] = message.message['tc']
                self.data['side'] = message.message['side']
                if self.data['side'] == 'white':
                    self.data['white'] = self.data['name']
                    self.data['black'] = message.message['name']
                else:
                    self.data['white'] = message.message['name']
                    self.data['black'] = self.data['name']
                self.data['chname'] = message.message['chname']
                self.finished = True
                self.next_stage = multiplayer_game.multiplayer_game_window
        print(message.message)
