import pygame

class game_type_choice_window:
    """docstring for game_type_choice_window"""
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []
        self.finished = False
        self.header_font = pygame.font.SysFont('arial', 40, True)
        header_text = "Choose game type:"
        self.header_rendered = self.header_font.render(header_text, True, (0, 0, 0))

    def loop(self, dt):
        self.screen.fill((255, 255, 255))
        # Drawing text
        self.draw_header_text()


    def ev(self, events, dt):
        pass

    def draw_header_text(self):
        self.screen.blit(self.header_rendered, (20, 20))

