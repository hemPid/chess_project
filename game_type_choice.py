import pygame

class game_type_choice_window:
    """docstring for game_type_choice_window"""
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []
        self.finished = False
        # rendering header
        self.header_font = pygame.font.SysFont('arial', 40, True)
        header_text = "Choose game type:"
        self.header_rendered = self.header_font.render(header_text, True, (0, 0, 0))
        # rendering icon text
        self.icon_font = pygame.font.SysFont('arial', 20, True)
        single_player_icon_text = "single board"
        multiplayer_icon_text = "online game"
        self.single_rendered_text = self.icon_font.render(single_player_icon_text, True, (0, 0, 0))
        self.multiplayer_rendered_text = self.icon_font.render(multiplayer_icon_text, True, (0, 0, 0))
        self.draw_initial_choice()

    def loop(self, dt):
        pass


    def ev(self, events, dt):
        pass

    def draw_initial_choice(self):
        self.screen.fill((255, 255, 255))
        # Drawing text
        self.draw_header_text()
        # Drawing single player button
        self.draw_single_player_button()

    def draw_header_text(self):
        self.screen.blit(self.header_rendered, (20, 20))

    def draw_single_player_button(self):
        pos_x = 20
        pos_y = 80
        width = 300
        height = 200
        icon_size = 150
        color = (243, 194, 105)
        rect = pygame.draw.rect(self.screen, color, (pos_x, pos_y, width, height))
        self.buttons.append({'name': 'single', 'rect': rect})
        icon_im = pygame.image.load('icons\\moni_icon.png').convert_alpha()
        icon_transformed = pygame.transform.scale(icon_im, (icon_size, icon_size))
        self.screen.blit(icon_transformed, (pos_x + (width // 2) - (icon_size // 2), pos_y + 10))
        self.screen.blit(self.single_rendered_text, (pos_x + 80, pos_y + icon_size + 20))

