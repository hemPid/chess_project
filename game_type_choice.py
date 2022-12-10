import pygame
import timecontrol_choice
import multiplayer_choice


class game_type_choice_window:
    """
    Окно выбора режима игры
    """
    def __init__(self, screen, data):
        """
        init
        Args:
        screen - экран для рисования
        data - данные, переданные предыдущим окном
        Возможные поля data:
        name - имя пользователя
        """
        self.screen = screen
        self.data = data
        self.buttons = []
        self.finished = False
        self.next_stage = None
        # rendering header
        self.header_font = pygame.font.SysFont('arial', 40, True)
        header_text = "Choose game type:"
        self.header_rendered = self.\
            header_font.render(header_text, True, (0, 0, 0))
        # rendering icon text
        self.icon_font = pygame.font.SysFont('arial', 20, True)
        single_player_icon_text = "single board"
        multiplayer_icon_text = "online game"
        self.single_rendered_text = self.icon_font.\
            render(single_player_icon_text, True, (0, 0, 0))
        self.multiplayer_rendered_text = self.icon_font.\
            render(multiplayer_icon_text, True, (0, 0, 0))
        # initial drawing
        self.draw_initial_choice()

    def loop(self, dt):
        """
        Главный цикл окна
        Args:
        dt - параметр pygame.time.Clock
        """
        return dt

    def ev(self, events, dt):
        """
        Обработчик событий окнаArgs:
        events - список событий
        dt - параметр pygame.time.Clock
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for but in self.buttons:
                    if but['rect'].collidepoint(event.pos):
                        # режим игры выбран
                        self.finished = True
                        if but['name'] == 'single':
                            # Переключение на выбор контроля времени
                            # для одиночной игры
                            self.data['game_type'] = 'single'
                            self.next_stage = timecontrol_choice.\
                                timecontrol_choice_window
                        else:
                            # Переключение на выбор режима онлай игры
                            self.data['game_type'] = 'multiplayer'
                            self.next_stage = multiplayer_choice.\
                                multiplayer_type_window

    def draw_initial_choice(self):
        """
        Рисует все кнопки и текст
        """
        self.screen.fill((255, 255, 255))
        # Drawing text
        self.draw_header_text()
        # Drawing single player button
        self.draw_single_player_button()
        # Drawing multiplayer button
        self.draw_multiplayer_button()

    def draw_header_text(self):
        """
        Рисует текст загаловка
        """
        self.screen.blit(self.header_rendered, (20, 20))

    def draw_single_player_button(self):
        """
        Рисует кнопку выбора одиночной игры
        """
        pos_x = 20
        pos_y = 80
        width = 300
        height = 200
        icon_size = 150
        color = (243, 194, 105)
        text_width = self.single_rendered_text.get_width()
        text_x = pos_x + (width - text_width) // 2
        rect = pygame.draw.\
            rect(self.screen, color, (pos_x, pos_y, width, height))
        self.buttons.append({'name': 'single', 'rect': rect})
        icon_im = pygame.image.load('icons\\moni_icon.png').convert_alpha()
        icon_transformed = pygame.transform.\
            scale(icon_im, (icon_size, icon_size))
        self.screen.blit(icon_transformed,
                         (pos_x + (width // 2) - (icon_size // 2),
                          pos_y + 10))
        self.screen.blit(self.single_rendered_text,
                         (text_x, pos_y + height - 30))

    def draw_multiplayer_button(self):
        """
        Рисует кнопку выбора онлайн игры
        """
        pos_x = 340
        pos_y = 80
        width = 300
        height = 200
        icon_size = 100
        color = (243, 194, 105)
        text_width = self.multiplayer_rendered_text.get_width()
        text_x = pos_x + (width - text_width) // 2
        rect = pygame.draw.rect(self.screen, color,
                                (pos_x, pos_y, width, height))
        self.buttons.append({'name': 'multi', 'rect': rect})
        icon_im = pygame.image.load('icons\\moni_icon.png').convert_alpha()
        icon_transformed = pygame.transform.\
            scale(icon_im, (icon_size, icon_size))
        self.screen.blit(icon_transformed,
                         (pos_x + (width - 2*icon_size)//2,
                          pos_y + 10))
        self.screen.blit(icon_transformed,
                         (pos_x + (width - 2*icon_size)//2 + icon_size,
                          pos_y + 10))
        self.screen.blit(self.multiplayer_rendered_text,
                         (text_x, pos_y + height - 30))
