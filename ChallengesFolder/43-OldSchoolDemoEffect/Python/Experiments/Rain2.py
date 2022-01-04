'''

Programming Challenge 43
Old School Demo Effect

This file implements the Rain effect

Screen resolution is small so that it is able to run
at a sufficient framerate.
A later implementation in C++ with OpenGL will
run at a much higher resolution.

Started: 1/3/2022

'''

import pygame
import random

class FireDemoEffect():
	def __init__(self):
		self.rootWidth, self.rootHeight = 700, 700
		self.root = pygame.display.set_mode([self.rootWidth, self.rootHeight], pygame.HWSURFACE)
		self.winWidth, self.winHeight = 60, 60
		self.drawTo = pygame.Surface([self.winWidth, self.winHeight], pygame.HWSURFACE)
		self.done = False


		self.layerA = [0 for x in range(self.winWidth * self.winHeight)]
		self.layerB = [0 for x in range(self.winWidth * self.winHeight)]

		#self.layerB[30 + 30 * 60] = 255
		self.layerB[31 + 30 * 60] = 255
		#self.layerB[32 + 30 * 60] = 255
		self.layerB[30 + 31 * 60] = 255
		self.layerB[32 + 31 * 60] = 255
		self.layerB[30 + 32 * 60] = 255
		self.layerB[31 + 32 * 60] = 255
		#self.layerB[32 + 32 * 60] = 255
		#self.layerB[31 + 31 * 60] = 255

		self.clock = pygame.time.Clock()

	def Main(self):
		while not self.done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.done = True

			self.clock.tick(20)

			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				self.layerB[int(pos[0]/self.rootWidth * self.winWidth) + int(pos[1]/self.rootHeight * self.winHeight) * self.winWidth] = 255
				#self.layerA[int(pos[0]/self.rootWidth * self.winWidth) + int(pos[1]/self.rootHeight * self.winHeight) * self.winWidth] = 255

			for y in range(1, self.winHeight - 1):
				for x in range(1, self.winWidth - 1):
					# avgVal = int((
					# 	self.layerB[(x - 1) + (y - 1) * self.winWidth] + self.layerB[(x) + (y - 1) * self.winWidth] +
					# 	self.layerB[(x + 1) + (y - 1) * self.winWidth] + self.layerB[(x - 1) + (y) * self.winWidth] + 
					# 	self.layerB[(x + 1) + (y) * self.winWidth] + self.layerB[(x - 1) + (y + 1) * self.winWidth] + 
					# 	self.layerB[(x) + (y + 1) * self.winWidth] + self.layerB[(x + 1) + (y + 1) * self.winWidth]
					# ) / 8)

					total = 0
					avg = 0
					for offset in [[x-1, y-1], [x, y-1], [x+1, y-1], [x-1, y], [x+1, y], [x-1, y+1], [x, y+1], [x+1, y+1]]:
						avg += self.layerB[offset[0] + offset[1] * self.winWidth]
						total += 1
					if (total != 0):
						avgVal = int(avg / total - self.layerA[x + y * self.winWidth])

						self.layerA[x + y * self.winWidth] = min(abs(avgVal * 0.97), 255)
						col = self.layerA[x + y * self.winWidth]

						self.drawTo.set_at((x, y), (col, col, col))

			self.layerA, self.layerB = self.layerB, self.layerA

			pygame.transform.scale(self.drawTo, [self.rootWidth, self.rootHeight], self.root)

			pygame.display.flip()

if __name__ == "__main__":
	FireDemoEffect().Main()
