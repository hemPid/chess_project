import pygame
import timecontrol_choice
import connect_room

class multiplayer_type_window:
    """docstring for multiplayer_type_window"""
    def __init__(self, screen, data):
        self.screen = screen
        self.data = data
        self.finished = False
        self.next_stage = None
        self.screen.fill((255, 255, 255))
        self.draw_buttons()


    def loop(self, dt):
        pass

    def ev(self, events, dt):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for but in self.buttons:
                    if self.buttons[but].collidepoint(event.pos):
                        self.finished = True
                        if but == 'create':
                            self.next_stage = timecontrol_choice.\
                                timecontrol_choice_window
                        else:
                            self.next_stage = connect_room.connect_window

    def draw_buttons(self):
        buttons_color = (243, 194, 105)
        buttons_font = pygame.font.SysFont('arial', 40, True)
        create_but_text = buttons_font.\
            render('Create room', True, (0, 0, 0))
        connect_but_text = buttons_font.\
            render('Connect room', True, (0, 0, 0))
        self.buttons = {
            'create': pygame.draw.rect(self.screen,
                                       buttons_color,
                                       (100, 100, 400, 100)),
            'connect': pygame.draw.rect(self.screen,
                                        buttons_color,
                                        (100, 300, 400, 100))
        }
        self.screen.blit(create_but_text,
                         (300 - create_but_text.get_width()/2,
                          150 - create_but_text.get_height()/2))
        self.screen.blit(connect_but_text,
                         (300 - connect_but_text.get_width()/2,
                          350 - connect_but_text.get_height()/2))
