import pygame
import own_tc_choice
import oponents_name_input
import loading_room


class timecontrol_choice_window:
    """
    Класс окна выбора контроля времени
    """
    def __init__(self, screen, data):
        """
        init
        Args:
        screen - экран для рисования
        data - данные, переданные предыдущим окном
        Возможные поля data:
        name - имя пользователя
        game_type - тип игры
        """
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
        """
        Главный цикл окна
        Args:
        dt - параметр pygame.time.Clock
        """
        pass

    def ev(self, events, dt):
        """
        Обработчик событий окна
        Args:
        events - список событий
        dt - параметр pygame.time.Clock
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for but in self.buttons:
                    if but['rect'].collidepoint(event.pos):
                        print(but['name'])
                        if but['name'] == 'own game':
                            # запуск ввода собственного контроля времени
                            self.finished = True
                            self.next_stage = own_tc_choice.\
                                own_tc_choice_window
                        else:
                            self.data['tc'] = but['name']
                            self.finished = True
                            if self.data['game_type'] == 'single':
                                # запуск одиночной игры
                                self.next_stage = oponents_name_input.\
                                    oponents_name_window
                            else:
                                # запуск онлайн игры
                                self.next_stage = loading_room.\
                                    waiting_room_window

    def draw_buttons(self):
        """
        Рисует кнопки выбора контроля времени
        """
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
        """
        Рисует кнопку
        Args:
        pos_x - положение кнопки по оси Ox
        pos_y - положение кнопки по оси Oy
        width - ширина кнопки
        height - высота кнопки
        text - текст кнопки
        """
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
