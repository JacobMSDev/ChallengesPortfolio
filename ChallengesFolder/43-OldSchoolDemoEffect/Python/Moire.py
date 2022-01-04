'''

Programming Challenge 43
Old School Demo Effect

This file implements the Moire effect

Screen resolution is small so that it is able to run
at a sufficient framerate.
A later implementation in C++ with OpenGL will
run at a much higher resolution.

Started: 1/3/2022
Finished: 1/3/2022

'''

import pygame
import random
import math

class MoireDemoEffect():
	def __init__(self):

		# Define the main pygame window
		self.rootWidth, self.rootHeight = 700, 700
		self.root = pygame.display.set_mode([self.rootWidth, self.rootHeight], pygame.HWSURFACE)

		# Define a surface to render the effect onto
		self.winWidth, self.winHeight = 300, 300
		self.drawTo = pygame.Surface([self.winWidth, self.winHeight], pygame.HWSURFACE)

		self.done = False

		# Focal points of the effect
		self.focii = [
			[int(self.winWidth / 4), int(self.winHeight / 2)],
			[int(self.winWidth * 3 / 4), int(self.winHeight / 2)]
		]
		# Position the points move to
		self.fociiGoal = [
			[random.randint(0, self.winWidth), random.randint(0, self.winHeight)],
			[random.randint(0, self.winWidth), random.randint(0, self.winHeight)]
		]

		self.scale = 0.05 # Distance divisor
		self.speed = 4 # Focii step distance each frame
		self.radius = 10 # Threshold radius to pick a new point to move to

	def Main(self):
		while not self.done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.done = True

			# Move the focii to their target positions
			for i in range(2):
				if (self.focii[i][0] < self.fociiGoal[i][0] - self.radius):
					self.focii[i][0] += self.speed
				elif (self.focii[i][0] > self.fociiGoal[i][0] + self.radius):
					self.focii[i][0] -= self.speed
				else:
					# Set a new x value
					self.fociiGoal[i][0] = random.randint(0, self.winWidth)

				if (self.focii[i][1] < self.fociiGoal[i][1] - self.radius):
					self.focii[i][1] += self.speed
				elif (self.focii[i][1] > self.fociiGoal[i][1] + self.radius):
					self.focii[i][1] -= self.speed
				else:
					# Set a new y value
					self.fociiGoal[i][1] = random.randint(0, self.winHeight)

			for y in range(self.winHeight):
				for x in range(self.winWidth):
					# Calculate distance to each focii per pixel
					dist1 = int(((self.focii[0][0] - x)**2 + (self.focii[0][1] - y)**2)**0.5 * self.scale)
					dist2 = int(((self.focii[1][0] - x)**2 + (self.focii[1][1] - y)**2)**0.5 * self.scale)
					# XOR the distances
					col = dist1 ^ dist2
					# If odd set to colour A, else colour B
					col = (255, 255, 255) if col & 1 else (0, 0, 0)
					# Draw the pixel
					self.drawTo.set_at((x, y), col)

			# Scale and draw the surface to fit the window
			pygame.transform.scale(self.drawTo, [self.rootWidth, self.rootHeight], self.root)
			# Update the screen
			pygame.display.flip()

if __name__ == "__main__":
	MoireDemoEffect().Main()
