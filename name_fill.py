import pygame
import pygame_textinput


class name_fill_window:
	"""docstring for name_fill_window"""
	def __init__(self, screen):
		self.screen = screen
		self.f1 = pygame.font.SysFont('arial', 40, True)
		self.text1 = self.f1.render(str('Enter your name (20 symb. max, eng. letters or _):'), True, 0x000000)
		self.manager = pygame_textinput.TextInputManager(validator = self.valid)
		self.t_imp = pygame_textinput.TextInputVisualizer(font_object=self.f1, manager=self.manager)

	def valid(self, inp):
		if len(inp) >= 20:
			return False
		elif len(inp) == 0:
			return True
		else:
			letter = inp[len(inp)-1]
			if ("a" <= letter <= "z") or ("A" <= letter <= "Z") or letter == "_":
				return True
			else:
				return False

	def loop(self):
		self.screen.fill(0xffffff)
		self.screen.blit(self.text1, (100, 100))
		self.screen.blit(self.t_imp.surface, (100, 150))

	def ev(self, events):
		self.t_imp.update(events)
		for event in events:
			if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
				val = self.t_imp.value
				if len(val) > 0:
					print('great:', val)
				else:
					print('Nope')
