import pygame
import os.path
import name_fill

def get_name():
    if os.path.isfile("db.txt"):
        pass
    else:
        return False

def main():
    FPS = 30
    screen_width = 1200
    screen_height = 800
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    stage = "initialization"
    finished = False
    screen.fill(0xffffff)
    name = get_name()
    window = None
    if name == False:
        stage = "name_fill"
        window = name_fill.name_fill_window(screen)
    else:
        stage = "game_type_choice"
    while not finished:
        pygame.display.update()
        dt = clock.tick(FPS)
        if stage == "name_fill":
            window.loop()
            events = pygame.event.get()
            window.ev(events)
            for event in events:
                if event.type == pygame.QUIT:
                    finished = True
        else:
            finished = True
    pygame.quit()

if __name__ == '__main__':
    main()