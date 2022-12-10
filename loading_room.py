import pygame
import connection

class waiting_room_window:
	"""docstring for witing_room_window"""
	def __init__(self, screen, data):
		self.screen = screen
		self.data = data
		self.finished = False
		self.next_stage = None
		self.screen.fill((255,255,255))

	def loop(self, dt):
		pass

	def ev(self, events, dt):
		pass
