import pygame
import connection

class connect_window:
	def __init__(self, screen, data):
		self.screen = screen
		self.data = data
		self.finished = False
		self.next_stage = None
		self.screen.fill((255, 255, 255))
		self.buttons = []
		self.con = connection.Connection('waiting_room', self.data['name'], self.msg_listener, self.request)
		self.con.connect()

	def loop(self, dt):
		pass

	def ev(self, events, dt):
		pass

	def draw_list(self):
		pass

	def request(self):
		self.con.write({'msg_type': 'request'})

	def msg_listener(self, message):
		if message.message['msg_type'] == 'introduction':
			print(message.message)
		elif message.message['msg_type'] == 'remove':
			print(message.message)
