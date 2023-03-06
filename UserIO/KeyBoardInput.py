import pygame
import time
import multiprocessing as mp
# KEY LIST : https://www.pygame.org/docs/ref/key.html


class KeyBoard(object):
	def __init__(self):
		self.W = mp.Value('i', 0)
		self.A = mp.Value('i', 0)
		self.S = mp.Value('i', 0)
		self.D = mp.Value('i', 0)
		self.UP = mp.Value('i', 0)
		self.DOWN = mp.Value('i', 0)
		self.LEFT = mp.Value('i', 0)
		self.RIGHT = mp.Value('i', 0)
		self.ESCAPE = mp.Value('i', 0)
		self.ENTER = mp.Value('i', 0)
		self.BACKSPACE = mp.Value('i', 0)
		self.SPACE = mp.Value('i', 0)
		self.TAB = mp.Value('i', 0)
		self.C = mp.Value('i', 0)

		self._monitor_process = mp.Process(target=self._monitor_keyboard, args=())
		self._monitor_process.start()

	def __del__(self):
		self._monitor_process.terminate()

	# return the buttons/triggers that you care about in this methode
	def read(self):
		return self.W.value, self.A.value, self.S.value, self.D.value, \
			self.UP.value, self.DOWN.value, self.LEFT.value, self.RIGHT.value,\
			self.ESCAPE.value, self.ENTER.value, self.BACKSPACE.value, self.SPACE.value, self.TAB.value, self.C.value

	def _monitor_keyboard(self):
		process = True
		pygame.init()
		# Define the background colour
		# using RGB color coding.
		background_colour = (234, 212, 252)

		# Define the dimensions of
		# screen object(width,height)
		screen = pygame.display.set_mode((300, 300))

		# Set the caption of the screen
		pygame.display.set_caption('CLICK ON ME TO TAKE INPUT')

		# Fill the background colour to the screen
		screen.fill(background_colour)
		while process:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_w:
						self.W.value = 1
					elif event.key == pygame.K_a:
						self.A.value = 1
					elif event.key == pygame.K_s:
						self.S.value = 1
					elif event.key == pygame.K_d:
						self.D.value = 1
					elif event.key == pygame.K_UP:
						self.UP.value = 1
					elif event.key == pygame.K_DOWN:
						self.DOWN.value = 1
					elif event.key == pygame.K_LEFT:
						self.LEFT.value = 1
					elif event.key == pygame.K_RIGHT:
						self.RIGHT.value = 1
					elif event.key == pygame.K_ESCAPE:
						self.ESCAPE.value = 1
					elif event.key == pygame.K_RETURN:
						self.ENTER.value = 1
					elif event.key == pygame.K_BACKSPACE:
						self.BACKSPACE.value = 1
					elif event.key == pygame.K_SPACE:
						self.SPACE.value = 1
					elif event.key == pygame.K_TAB:
						self.TAB.value = 1
					elif event.key == pygame.K_c:
						self.C.value = 1
				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_w:
						self.W.value = 0
					elif event.key == pygame.K_a:
						self.A.value = 0
					elif event.key == pygame.K_s:
						self.S.value = 0
					elif event.key == pygame.K_d:
						self.D.value = 0
					elif event.key == pygame.K_UP:
						self.UP.value = 0
					elif event.key == pygame.K_DOWN:
						self.DOWN.value = 0
					elif event.key == pygame.K_LEFT:
						self.LEFT.value = 0
					elif event.key == pygame.K_RIGHT:
						self.RIGHT.value = 0
					elif event.key == pygame.K_ESCAPE:
						self.ESCAPE.value = 0
					elif event.key == pygame.K_RETURN:
						self.ENTER.value = 0
					elif event.key == pygame.K_BACKSPACE:
						self.BACKSPACE.value = 0
					elif event.key == pygame.K_SPACE:
						self.SPACE.value = 0
					elif event.key == pygame.K_TAB:
						self.TAB.value = 0
					elif event.key == pygame.K_c:
						self.C.value = 0
		pygame.quit()


if __name__ == '__main__':
	key = KeyBoard()
	while True:
		print(key.read())
		time.sleep(1)
