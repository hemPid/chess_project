import pygame
import pygame_textinput
import single_game


class oponents_name_window:
    """docstring for oponents_name_window"""
    def __init__(self, screen, data):
        self.screen = screen
        self.data = data
        self.next_stage = None
        self.finished = False
        self.alert = False
        self.f1 = pygame.font.SysFont('arial', 40, True)
        self.f_alert = pygame.font.SysFont('arial', 20)
        self.alert_obj = self.f_alert.render(str(''), True, 0xff0000)
        self.text1 = self.f1.\
            render(str('Enter your oponents name (20 symb. max, eng. letters or _):'),
                   True, 0x000000)
        self.manager = pygame_textinput.TextInputManager(validator=self.valid)
        self.t_imp = pygame_textinput.\
            TextInputVisualizer(font_object=self.f1, manager=self.manager)

    def valid(self, inp):
        if len(inp) >= 20:
            return False
        elif len(inp) == 0:
            return True
        else:
            letter = inp[len(inp)-1]
            if ("a" <= letter.lower() <= "z") or letter == "_":
                return True
            else:
                return False

    def make_alert(self, text):
        self.alert = True
        self.alert_obj = self.f_alert.render(str(text), True, (255, 0, 0))

    def loop(self, dt):
        self.screen.fill(0xffffff)
        self.screen.blit(self.text1, (50, 100))
        self.screen.blit(self.t_imp.surface, (50, 150))
        if self.alert:
            self.screen.blit(self.alert_obj, (50, 200))

    def ev(self, events, dt):
        self.t_imp.update(events)
        for event in events:
            if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                val = self.t_imp.value
                if len(val) > 0:
                    # validation succesful
                    print('great:', val)
                    self.data['op_name'] = val
                    self.finished = True
                    self.next_stage = single_game.single_game_window
                else:
                    self.make_alert('You need to enter something')
