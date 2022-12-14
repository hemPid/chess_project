import pygame
import game_type_choice
import connection
import multiplayer_game
import random


class waiting_room_window:
    """
    класс окна ожидания подключения к созданной комнате
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
        tc - контроль времени
        """
        self.screen = screen
        self.data = data
        self.finished = False
        self.next_stage = None
        self.screen.fill((255, 255, 255))
        # drawing text and quit button
        self.button_font = pygame.font.SysFont('arial', 40, True)
        self.text_font = pygame.font.SysFont('arial', 50, True)
        self.text_rend = self.text_font.\
            render('waiting for someone to connect', True, (0, 0, 0))
        self.screen.blit(self.text_rend, (100, 100))
        self.but_text_rend = self.button_font.\
            render('quit', True, (0, 0, 0))
        # кнопка выхода из окна
        self.buttons_color = (243, 194, 105)
        self.quit_but = pygame.draw.\
            rect(self.screen, self.buttons_color,
                 (100, 200,
                  self.but_text_rend.get_width() + 10,
                  self.but_text_rend.get_height() + 10))
        self.screen.blit(self.but_text_rend, (105, 205))
        # forming connection
        self.con = connection.Connection('waiting_room',
                                         self.data['name'],
                                         self.msg_listener,
                                         self.introduce)
        self.con.connect()
        self.data_to_send = self.data.copy()
        self.data_to_send['msg_type'] = 'introduction'

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
                if self.quit_but.collidepoint(event.pos):
                    # удаление комнаты и возврат на главную
                    self.remove()
                    self.con.disconnect()
                    self.finished = True
                    self.data = {'name': self.data['name']}
                    self.next_stage = game_type_choice.game_type_choice_window
            if event.type == pygame.QUIT:
                # разрыв соединения и удаление комнаты
                self.remove()
                self.con.disconnect()

    def introduce(self):
        """
        Заявляет о создании комнаты в канал
        """
        self.con.write(self.data_to_send)

    def remove(self):
        """
        Заявляет об удалении комнаты в канал
        """
        self.con.write({'msg_type': 'remove', 'name': self.data['name']})

    def start_game(self, op_name):
        """
        Переключается на партию
        Создаёт канал и передаёт подтверждение начал партии оппоненту
        Args:
        op_name - имя оппонента
        """
        side = random.randint(0, 1)
        op_side = ''
        if side:
            self.data['white'] = self.data['name']
            self.data['black'] = op_name
            self.data['side'] = 'white'
            op_side = 'black'
        else:
            self.data['white'] = op_name
            self.data['black'] = self.data['name']
            self.data['side'] = 'black'
            op_side = 'white'
        # генерация имени канала
        self.data['chname'] = self.data['name'] + '_' + op_name
        # отправка сообщения типа confirmation
        self.con.write({'msg_type': 'confirmation',
                        'to': op_name,
                        'chname': self.data['chname'],
                        'side': op_side,
                        'name': self.data['name'],
                        'tc': self.data['tc']})
        # разрыв соединения и переход на окно партии
        self.con.disconnect()
        self.finished = True
        self.next_stage = multiplayer_game.multiplayer_game_window

    def msg_listener(self, message):
        """
        Обработчик сообщений в канале
        """
        if self.finished:
            return 0
        if message.message['msg_type'] == 'request':
            # запрос от нового пользователя
            self.introduce()
        elif message.message['msg_type'] == 'connect' and\
                message.message['to'] == self.data['name']:
            # обработка принятия приглашения
            self.start_game(message.message['name'])
