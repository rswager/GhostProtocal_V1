import pygame
import time
import threading
#KEY LIST : https://www.pygame.org/docs/ref/key.html

class KeyBoard(object):
	def __init__(self):
		self.W = 0
		self.A = 0
		self.S = 0
		self.D = 0
		self.UP = 0
		self.DOWN = 0
		self.LEFT = 0
		self.RIGHT = 0
		self.ESCAPE = 0
		self.ENTER = 0
		self.BACKSPACE = 0
		self.SPACE = 0
		self.TAB = 0
		self.process = True

		self._monitor_thread = threading.Thread(target=self._monitor_keyboard, args=())
		self._monitor_thread.daemon = True
		self._monitor_thread.start()

	def read(self): # return the buttons/triggers that you care about in this methode
		return self.W,self.A,self.S,self.D,self.UP,self.DOWN,self.LEFT,self.RIGHT,self.ESCAPE,self.ENTER,self.BACKSPACE,self.SPACE,self.TAB

	def __del__(self):
		self.process = False

	def _monitor_keyboard(self):
		pygame.init()
		# Define the background colour
		# using RGB color coding.
		background_colour = (234, 212, 252)
		  
		# Define the dimensions of
		# screen object(width,height)
		screen = pygame.display.set_mode((300, 300))
		  
		# Set the caption of the screen
		pygame.display.set_caption('Geeksforgeeks')
		  
		# Fill the background colour to the screen
		screen.fill(background_colour)
		while self.process:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_w:
							self.W = 1
						elif event.key == pygame.K_a:
							self.A = 1
						elif event.key == pygame.K_s:
							self.S = 1
						elif event.key == pygame.K_d:
							self.D = 1
						elif event.key == pygame.K_UP:
							self.UP = 1
						elif event.key == pygame.K_DOWN:
							self.DOWN = 1
						elif event.key == pygame.K_LEFT:
							self.LEFT = 1
						elif event.key == pygame.K_RIGHT:
							self.RIGHT = 1
						elif event.key == pygame.K_ESCAPE:
							self.ESCAPE = 1
							self.process = False
						elif event.key == pygame.K_RETURN:
							self.ENTER = 1
						elif event.key == pygame.K_BACKSPACE:
							self.BACKSPACE = 1
						elif event.key == pygame.K_SPACE:
							self.SPACE = 1
						elif event.key == pygame.K_TAB:
							self.TAB = 1
				elif event.type == pygame.KEYUP:
						if event.key == pygame.K_w:
							self.W = 0
						elif event.key == pygame.K_a:
							self.A = 0
						elif event.key == pygame.K_s:
							self.S = 0
						elif event.key == pygame.K_d:
							self.D = 0
						elif event.key == pygame.K_UP:
							self.UP = 0
						elif event.key == pygame.K_DOWN:
							self.DOWN = 0
						elif event.key == pygame.K_LEFT:
							self.LEFT = 0
						elif event.key == pygame.K_RIGHT:
							self.RIGHT = 0
						elif event.key == pygame.K_ESCAPE:
							self.ESCAPE = 0
						elif event.key == pygame.K_RETURN:
							self.ENTER = 0
						elif event.key == pygame.K_BACKSPACE:
							self.BACKSPACE = 0
						elif event.key == pygame.K_SPACE:
							self.SPACE = 0
						elif event.key == pygame.K_TAB:
							self.TAB = 0
		pygame.quit()

if __name__ == '__main__':
	key = KeyBoard()
	while True:
		print(key.read())
		time.sleep(1)