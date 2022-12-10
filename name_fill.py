import pygame
import pygame_textinput
import game_type_choice


class name_fill_window:
    """
    окно ввода имени, при отсутствии базы данных
    """
    def __init__(self, screen, data):
        """
        init
        Args:
        screen - экран для рисования
        data - данные, переданные предыдущим окном
        """
        self.screen = screen
        self.data = data
        self.alert = False
        self.finished = False
        self.next_stage = ""
        # инициализация шрифтов и обработка текста
        self.f1 = pygame.font.SysFont('arial', 40, True)
        self.f_alert = pygame.font.SysFont('arial', 20)
        self.alert_obj = self.f_alert.render(str(''), True, 0xff0000)
        self.text1 = self.f1.\
            render(str('Enter your name (20 symb. max, eng. letters or _):'),
                   True, 0x000000)
        # инициализация поля ввода
        self.manager = pygame_textinput.TextInputManager(validator=self.valid)
        self.t_imp = pygame_textinput.\
            TextInputVisualizer(font_object=self.f1, manager=self.manager)

    def valid(self, inp):
        """
        Валидатор для поля ввода
        Проверяет на допустимые символы и их число
        Args:
        inp - содержимое поля ввода
        """
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
        """
        включает отображение сообщения об ошибке
        Args:
        text - текст сообщения об ошибке
        """
        self.alert = True
        self.alert_obj = self.f_alert.render(str(text), True, (255, 0, 0))

    def create_db(self, name):
        """
        создаёт базу данных после успешного ввода имени
        Args:
        name - введённое имя
        """
        with open('db.txt', 'w') as f:
            f.write('name: ' + name + '\n')

    def loop(self, dt):
        """
        Главный цикл окна.
        Args:
        dt - параметр pygame.time.Clock
        """
        self.screen.fill(0xffffff)
        self.screen.blit(self.text1, (100, 100))
        self.screen.blit(self.t_imp.surface, (100, 150))
        if self.alert:
            self.screen.blit(self.alert_obj, (100, 200))

    def ev(self, events, dt):
        """
        Обработчик событий окна
        Args:
        events - список событий
        dt - параметр pygame.time.Clock
        """
        self.t_imp.update(events)  # обновление содержимого поля ввода
        for event in events:
            if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                val = self.t_imp.value
                if len(val) > 0:
                    # validation succesful
                    print('great:', val)
                    self.create_db(val)
                    self.data = {'name': val}
                    self.finished = True
                    self.next_stage = game_type_choice.game_type_choice_window
                else:
                    self.make_alert('You need to enter something')
