import pygame

class game_type_choice_window:
	"""docstring for game_type_choice_window"""
	def __init__(self, screen):
		self.screen = screen
        self.buttons = []
		self.finished = False
        self.header_font = pygame.font.SysFont('arial', 40, True)

	def loop(self):
		self.screen.fill((255, 255, 255))
        # Drawing text


	def ev(self, events):
		pass

    def draw_header_text(self):
        pass

		