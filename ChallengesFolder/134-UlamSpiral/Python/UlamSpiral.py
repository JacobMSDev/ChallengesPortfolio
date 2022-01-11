'''

Programming Challenge 134
Ulam Spiral

Started: 11/1/2022
Finished: 11/1/2022

'''

import pygame, math
import PrimeTest

class UlamSpiral():
	def __init__(self):
		self.rootWidth, self.rootHeight = 600, 600
		self.root = pygame.display.set_mode([self.rootWidth, self.rootHeight])
		self.done = False

		self.winWidth, self.winHeight = 300, 300
		self.canvas = pygame.Surface([self.winWidth, self.winHeight])

		self.colA = (140, 140, 255)
		self.colB = (20, 20, 100)

	def Main(self):
		# Different options for renderer
		# Currently no way to choose other than uncomment the selection
		
		# self.ScanLines()
		self.Spiral()
		# self.Triangle()
		# self.AltSpiral()

		while not self.done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.done = True

	def AddPixel(self, x: int, y: int, i: int):
		''' Add a pixel to the surface and refresh the screen '''

		prime = PrimeTest.IsPrime(i) # Test if the number if prime
		self.canvas.set_at([x, y], self.colA if prime else self.colB) # Add the pixel
		pygame.transform.scale(self.canvas, [self.rootWidth, self.rootHeight], self.root)
		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				self.done = True

	def ScanLines(self):
		''' Scans left to right, top to bottom '''

		for i in range(self.winWidth * self.winHeight):
			self.AddPixel(i % self.winWidth, i // self.winHeight, i)
			if self.done:
				break

	def Spiral(self):
		''' The ulam spiral '''

		x = self.winWidth // 2
		y = self.winHeight // 2
		direction = -1

		val = 1	# Storage of the number to test primality

		self.AddPixel(x, y, val)
		for i in range(self.winWidth):
			# Walk i units horizontally
			for dx in range(i):
				x += direction
				val += 1
				self.AddPixel(x, y, val)
			# Walk i units vertically
			for dy in range(i):
				y -= direction
				val += 1
				self.AddPixel(x, y, val)

			# Flip walk direction
			direction *= -1

	def Triangle(self):
		''' Creates a triangle from the center top down '''
		val = 1
		baseX = self.winWidth // 2
		for width in range(self.winHeight):
			for i in range(width):
				self.AddPixel(baseX - width // 2 + i, width, val)
				val += 1

	def AltSpiral(self):
		''' Creates a normal spiral outwards from the center '''

		cX = self.winWidth // 2
		cY = self.winHeight // 2
		for i in range(self.winWidth * 15):
			self.AddPixel(int(cX + 0.05 * i * math.cos(i / 6.289)), int(cY + 0.05 * i * math.sin(i / 6.289)), i)

if __name__ == "__main__":
	UlamSpiral().Main()
