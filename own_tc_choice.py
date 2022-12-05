import pygame
import pygame_textinput


class own_tc_choice_window:
	"""docstring for own_tc_choice_window"""
	def __init__(self, screen, data):
		self.screen = screen
		self.data = data
		self.next_stage = None
		self.finished = False
		self.screen.fill((255, 255, 255))
		print('Yeah')

	def loop(self, dt):
		pass

	def ev(self, events, dt):
		pass
