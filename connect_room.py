import pygame
import connection

class connect_window:
	def __init__(self, screen, data):
		self.screen = screen
		self.data = data
		self.finished = False
		self.next_stage = None
		self.screen.fill((255, 255, 255))
		self.aviliable_rooms = {}
		self.buttons = []
		self.buttons_color = (243, 194, 105)
		self.con = connection.Connection('waiting_room', self.data['name'], self.msg_listener, self.request)
		self.con.connect()

	def loop(self, dt):
		pass

	def ev(self, events, dt):
		pass

	def draw_list(self):
		pass

	def get_button_coords(self):
		return (100, 100, 100, 100)

	def request(self):
		self.con.write({'msg_type': 'request'})

	def msg_listener(self, message):
		if message.message['msg_type'] == 'introduction':
			self.aviliable_rooms[message.message['name']] = {
				'tc': message.message['tc'],
				'button': pygame.draw.rect(self.screen, self.buttons_color, self.get_button_coords())
			}
		elif message.message['msg_type'] == 'remove':
			self.aviliable_rooms.pop(message.message['name'])
		print(message.message)
		print(self.aviliable_rooms)
