import pygame
import pygame_textinput
import oponents_name_input

class own_tc_choice_window:
    """docstring for own_tc_choice_window"""
    def __init__(self, screen, data):
        self.screen = screen
        self.data = data
        self.next_stage = None
        self.finished = False
        self.invalid_format = False
        # rendering text
        self.font = pygame.font.SysFont('arial', 40, True)
        self.text1_rendered = self.font.render('Enter game time in minutes:', True, (0, 0, 0))
        self.text2_rendered = self.font.render('Enter added time in seconds:', True, (0, 0, 0))
        self.alert_font = pygame.font.SysFont('arial', 30, True)
        self.alert_text = self.font.render('Invalid format', True, (255, 0, 0))
        # adding input rects
        self.time_inp_rect = pygame.draw.rect(self.screen, (100,100,100),
                                              (70 + self.text1_rendered.get_width(), 20, 100, self.text1_rendered.get_height()))
        self.add_inp_rect = pygame.draw.rect(self.screen, (100,100,100), (70 + self.text2_rendered.get_width(),
                                        30 + self.text1_rendered.get_height(),
                                        100, self.text2_rendered.get_height()))
        # adding text inputs
        self.manager1 = pygame_textinput.TextInputManager(validator=self.valid)
        self.manager2 = pygame_textinput.TextInputManager(validator=self.valid)
        self.time_inp = pygame_textinput.TextInputVisualizer(font_object=self.font, manager=self.manager1)
        self.add_inp = pygame_textinput.TextInputVisualizer(font_object=self.font, manager=self.manager2)
        self.time_inp_active = False
        self.add_inp_active = False
        # drawing button
        self.button_text = self.font.render('continue', True, (0, 0, 0))
        self.button = pygame.draw.rect(self.screen, (243, 194, 105),
                                       (50, 200, self.button_text.get_width() + 20, self.button_text.get_height() + 10))

    def loop(self, dt):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.text1_rendered, (50, 20))
        self.screen.blit(self.text2_rendered, (50, 30 + self.text1_rendered.get_height()))
        time_color = (150, 150, 150)
        add_color = (150, 150, 150)
        if self.time_inp_active:
            time_color = (200, 200, 200)
        if self.add_inp_active:
            add_color = (200, 200, 200)
        pygame.draw.rect(self.screen, time_color, self.time_inp_rect)
        pygame.draw.rect(self.screen, add_color, self.add_inp_rect)
        self.screen.blit(self.time_inp.surface, (70 + self.text1_rendered.get_width(), 20))
        self.screen.blit(self.add_inp.surface, (70 + self.text2_rendered.get_width(), 30 + self.text1_rendered.get_height()))
        pygame.draw.rect(self.screen, (243, 194, 105), self.button)
        self.screen.blit(self.button_text, (60, 205))
        if self.invalid_format:
            self.screen.blit(self.alert_text, (50, 220 + self.button_text.get_height()))

    def ev(self, events, dt):
        if self.time_inp_active:
            self.time_inp.update(events)
        if self.add_inp_active:
            self.add_inp.update(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.time_inp_active = self.time_inp_rect.collidepoint(event.pos)
                self.add_inp_active = self.add_inp_rect.collidepoint(event.pos)
                if self.button.collidepoint(event.pos):
                    time = self.time_inp.value
                    add = self.add_inp.value
                    if (not len(time)*len(add)) or (time[0] == '0') or (add[0] == '0' and len(add) > 1):
                        self.invalid_format = True
                    else:
                        self.data['tc'] = time + ' + ' + add
                        self.finished = True
                        if self.data['game_type'] == 'single':
                            self.next_stage = oponents_name_input.oponents_name_window
                        else:
                            pass

    def valid(self, text):
        if not len(text):
            return True
        symbol = text[len(text) - 1]
        return ('0' <= symbol <= '9') and (len(text) <= 3)
