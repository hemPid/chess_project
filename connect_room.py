import pygame
import connection

class connect_window:
    def __init__(self, screen, data):
        self.screen = screen
        self.data = data
        self.finished = False
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

    def loop(self, dt):
        self.screen.fill((255, 255, 255))
        self.draw_list()

    def ev(self, events, dt):
        pass

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
                     (self.list_pos[0] + 150,
                      self.list_pos[1] +\
                      i*self.list_item_height +\
                      (self.list_item_height - data['rendered_name'].get_height()) / 2))
            pygame.draw.rect(self.screen, self.buttons_color, data['button'])
            self.screen.\
                blit(self.button_text,
                     (self.list_pos[0] + 402,
                      self.list_pos[1] +\
                      i*self.list_item_height +\
                      (self.list_item_height - self.button_text.get_height()) / 2))
            i += 1



    def get_button_coords(self):
        return (self.list_pos[0] + 400,
                self.list_pos[1] + len(self.aviliable_rooms)*self.list_item_height + 2,
                self.button_text.get_width() + 4, self.list_item_height - 4)

    def request(self):
        self.con.write({'msg_type': 'request'})

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
        print(message.message)
        print(self.aviliable_rooms)
