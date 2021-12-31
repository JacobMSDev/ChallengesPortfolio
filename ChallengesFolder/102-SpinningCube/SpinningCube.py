'''

Programming Challenge 102
Draw a 3D spinning cube

'''

import pygame
from math import cos, sin
from random import randint

class SpinningCube():
	def __init__(self):
		self.screenWidth, self.screenHeight = 600, 600

		self.root = pygame.display.set_mode([self.screenWidth, self.screenHeight])
		self.programComplete = False

		self.time = 0.0005

		# Settings
		self.cubeScale = 0.5	# % width of screen the cube fills
		# Settings

		self.vertexBuffer = self.GeneratePoints()
		self.indexBuffer = self.GenerateIndexes()

	def Main(self):
		while not self.programComplete:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.programComplete = True

			self.root.fill((0, 0, 0))	# Clear the screen
			self.RenderCube()			# Render the cube
			self.RotateCube()
			pygame.display.flip()		# Refresh the screen

	def GeneratePoints(self):
		points = [
			[ self.cubeScale, -self.cubeScale,  self.cubeScale], # ( 1,  1,  1) i0
			[ self.cubeScale, -self.cubeScale, -self.cubeScale], # ( 1,  1, -1) i1
			[-self.cubeScale, -self.cubeScale,  self.cubeScale], # (-1,  1,  1) i2
			[-self.cubeScale, -self.cubeScale, -self.cubeScale], # (-1,  1, -1) i3
			[ self.cubeScale,  self.cubeScale,  self.cubeScale], # ( 1, -1,  1) i4
			[ self.cubeScale,  self.cubeScale, -self.cubeScale], # ( 1, -1, -1) i5
			[-self.cubeScale,  self.cubeScale,  self.cubeScale], # (-1, -1,  1) i6
			[-self.cubeScale,  self.cubeScale, -self.cubeScale]  # (-1, -1, -1) i7
		]

		return points

	def GenerateIndexes(self):
		indexes = [
			(0, 1), (1, 3), (3, 2), (2, 0),	# Top face
			(0, 4), (1, 5), (2, 6), (3, 7), # Edges
			(4, 5), (5, 7), (7, 6), (6, 4)	# Bottom face
		]

		return indexes

	def RotateCube(self):
		rotMat = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
		mX = [
			[1, 0, 0],
			[0, cos(self.time), -sin(self.time)],
			[0, sin(self.time), cos(self.time)]
		]
		mY = [
			[cos(self.time*2), 0, sin(self.time*2)],
			[0, 1, 0],
			[-sin(self.time*2), 0, cos(self.time*2)]
		]
		mZ = [
			[cos(-self.time*0.5), -sin(-self.time*0.5), 0],
			[sin(-self.time*0.5), cos(-self.time*0.5), 0],
			[0, 0, 1]
		]

		for j in range(3):
			for i in range(3):
				rotMat[j][i] = mX[j][0] * mY[0][i] + mX[j][1] * mY[1][i] + mX[j][2] * mY[2][i]
		for j in range(3):
			for i in range(3):
				rotMat[j][i] = rotMat[j][0] * mZ[0][i] + rotMat[j][1] * mZ[1][i] + rotMat[j][2] * mZ[2][i]

		for point in self.vertexBuffer:
			point[0] = point[0] * rotMat[0][0] + point[1] * rotMat[0][1] + point[2] * rotMat[0][2]
			point[1] = point[0] * rotMat[1][0] + point[1] * rotMat[1][1] + point[2] * rotMat[1][2]
			point[2] = point[0] * rotMat[2][0] + point[1] * rotMat[2][1] + point[2] * rotMat[2][2]

	def RenderCube(self):
		'''
			Render the cube by drawing lines between
			the vertices based on the indexbuffer
		'''

		for (indexA, indexB) in self.indexBuffer:
			# Convert coordinates from [-1, 1] to pixel range
			ax = (self.vertexBuffer[indexA][0] + 1) / 2 * self.screenWidth
			ay = (self.vertexBuffer[indexA][1] + 1) / 2 * self.screenHeight
			bx = (self.vertexBuffer[indexB][0] + 1) / 2 * self.screenWidth
			by = (self.vertexBuffer[indexB][1] + 1) / 2 * self.screenHeight

			pygame.draw.line(
				self.root,
				(255, 255, 255),
				[ax, ay],	# First point of line
				[bx, by],	# Second point of line
				5			# Line thickness
			)

		for i, point in enumerate(self.vertexBuffer):
			ax = (point[0] + 1) / 2 * self.screenWidth
			ay = (point[1] + 1) / 2 * self.screenHeight
			pygame.draw.circle(self.root, (255, 0, i * 29), [ax, ay], 20)

if __name__ == "__main__":
	SpinningCube().Main()
