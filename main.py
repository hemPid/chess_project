import pygame
import os.path
import name_fill
import game_type_choice
import os


def get_name():
    """
    Функция получает имя из базы данных,
    если база данных не инициализирована, возвращает False
    """
    if os.path.isfile("db.txt"):
        with open('db.txt', 'r') as f:
            line = f.readlines()[0].rstrip().split(': ')
            return line[1]
    else:
        return False


def main():
    """
    Главная функция. Содержит главный цикл,
    вызывающий все окна в программе
    """
    FPS = 30
    screen_width = 1200
    screen_height = 800
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    finished = False
    screen.fill(0xffffff)
    name = get_name()
    window = None
    if not name:
        window = name_fill.name_fill_window(screen, {})
    else:
        window = game_type_choice.\
            game_type_choice_window(screen, {'name': name})
    while not finished:
        pygame.display.update()
        dt = clock.tick(FPS)
        window.loop(dt)
        events = pygame.event.get()
        window.ev(events, dt)
        for event in events:
            if event.type == pygame.QUIT:
                finished = True
        if window.finished:
            window = window.next_stage(screen, window.data)
            if not name:
                name = get_name()
    pygame.quit()
    os._exit(0)


if __name__ == '__main__':
    main()
