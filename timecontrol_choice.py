import pygame
import own_tc_choice
import oponents_name_input


class timecontrol_choice_window:
    """docstring for timecontrol_choice_window"""
    def __init__(self, screen, data):
        self.screen = screen
        self.data = data
        self.next_stage = None
        self.finished = False
        self.buttons = []
        self.button_font = pygame.font.SysFont('arial', 40, True)
        print(data)
        self.screen.fill((255, 255, 255))
        self.draw_buttons()

    def loop(self, dt):
        pass

    def ev(self, events, dt):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for but in self.buttons:
                    if but['rect'].collidepoint(event.pos):
                        print(but['name'])
                        if but['name'] == 'own game':
                            self.finished = True
                            self.next_stage = own_tc_choice.own_tc_choice_window
                        else:
                            self.data['tc'] = but['name']
                            self.finished = True
                            if self.data['game_type'] == 'single':
                                self.next_stage = oponents_name_input.oponents_name_window
                            else:
                                pass

    def draw_buttons(self):
        button_width = 200
        button_height = 100
        pos_x = 50
        pos_y = 50
        sep = 10
        modes = [['1 + 0', '2 + 1', '3 + 0'],
                 ['3 + 2', '5 + 0', '5 + 3'],
                 ['10 + 0', '10 + 5', '15 + 10'],
                 ['30 + 0', '30 + 20', 'own game']]
        # drawing buttons
        for i in range(4):
            for j in range(3):
                self.draw_button(pos_x + j*(button_width + sep),
                                 pos_y + i*(button_height + sep),
                                 button_width, button_height,
                                 modes[i][j])

    def draw_button(self, pos_x, pos_y, width, height, text):
        color = (243, 194, 105)
        rect = pygame.draw.rect(self.screen, color,
                                (pos_x, pos_y, width, height))
        self.buttons.append({'name': text, 'rect': rect})
        rendered_text = self.button_font.render(text, True, (0, 0, 0))
        text_width = rendered_text.get_width()
        text_height = rendered_text.get_height()
        text_x = pos_x + (width - text_width) // 2
        text_y = pos_y + (height - text_height) // 2
        self.screen.blit(rendered_text, (text_x, text_y))
