import pygame
import timecontrol_choice
import connect_room


class multiplayer_type_window:
    """
    класс окна выбора типа инициализации онлайн игры
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
        self.finished = False
        self.next_stage = None
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
        Обработчик событий окнаArgs:
        events - список событий
        dt - параметр pygame.time.Clock
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for but in self.buttons:
                    if self.buttons[but].collidepoint(event.pos):
                        self.finished = True
                        if but == 'create':
                            # переключение на создание комнаты
                            self.next_stage = timecontrol_choice.\
                                timecontrol_choice_window
                        else:
                            # подключение к существующей комнате
                            self.next_stage = connect_room.connect_window

    def draw_buttons(self):
        """
        рисует кнопки
        """
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
