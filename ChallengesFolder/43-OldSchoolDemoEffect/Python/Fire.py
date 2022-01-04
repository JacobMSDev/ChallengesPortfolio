'''

Programming Challenge 43
Old School Demo Effect

This file implements the Fire effect

Screen resolution is small so that it is able to run
at a sufficient framerate.
A later implementation in C++ with OpenGL will
run at a much higher resolution.

Started: 1/3/2022

'''

import pygame
import random
import math

# Multiply an rgb by a constant
def colourMult(col, mult):
	return (int(col[0] * mult), int(col[1] * mult), int(col[2] * mult))

# Sum two rgb together
def colourSum(colA, colB):
	return (colA[0] + colB[0], colA[1] + colB[1], colA[2] + colB[2])

class FireDemoEffect():
	def __init__(self):

		# Define the main pygame window
		self.rootWidth, self.rootHeight = 700, 700
		self.root = pygame.display.set_mode([self.rootWidth, self.rootHeight], pygame.HWSURFACE)

		# Define a surface to render the effect to
		self.winWidth, self.winHeight = 55, 55
		self.drawTo = pygame.Surface([self.winWidth, self.winHeight], pygame.HWSURFACE)

		self.done = False

		# Array to store the 'fuel' line of the fire effect
		self.fuelVals = [(0, 0, 0) for x in range(self.winWidth)]
		# Pygame clock to limit the framerate
		self.clock = pygame.time.Clock()

	def Main(self):
		while not self.done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.done = True

			# Set framerate to 30 fps
			self.clock.tick(30)

			# Randomise the fuel values every frame
			for x in range(self.winWidth):
				col = random.randint(0, 255)
				self.fuelVals[x] = (col, 0 if col < 125 else col - 125, 0)

			for y in range(self.winHeight - 1):
				for x in range(self.winWidth):
					# For all lines except final line
					if (y != self.winHeight - 2):
						# Get the 3 colours below the current pixel 
						col = self.drawTo.get_at((x, y + 1))
						col = colourSum(col, self.drawTo.get_at((x - 1 if x > 1 else 0, y + 1)))
						col = colourSum(col, self.drawTo.get_at((x + 1 if x < self.winWidth - 2 else self.winWidth - 1, y + 1)))
						# Average the colour values
						col = colourMult(col, 0.333)
					# For final line
					else:
						# Get the 3 colours below the current pixel 
						col = self.fuelVals[x]
						col = colourSum(col, self.fuelVals[x - 1 if x > 1 else 0])
						col = colourSum(col, self.fuelVals[x + 1 if x < self.winWidth - 2 else self.winWidth - 1])
						# Average the colour values
						col = colourMult(col, 0.333)

					# Decay the colour a bit
					col = colourMult(col, 0.98)
					# Draw the pixel
					self.drawTo.set_at((x, y), col)

			# Scale and draw the surface to fit the window
			pygame.transform.scale(self.drawTo, [self.rootWidth, self.rootHeight], self.root)
			# Update the screen
			pygame.display.flip()

if __name__ == "__main__":
	FireDemoEffect().Main()
