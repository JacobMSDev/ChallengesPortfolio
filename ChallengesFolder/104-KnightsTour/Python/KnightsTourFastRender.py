import pygame, pygame.freetype as freetype

import random

class Tour():
	def __init__(self):
		self.rootWidth, self.rootHeight = 600, 600
		self.root = pygame.display.set_mode([self.rootWidth, self.rootHeight])
		self.done = False

		self.colA = (100, 100, 200)
		self.colB = (200, 100, 100)

		self.gridSize = 100
		self.gridWidth = self.rootWidth / self.gridSize
		self.gridHeight = self.rootHeight / self.gridSize

		self.knightMoves = [[-1, -2], [1, -2], [2, -1], [2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1]]

		self.path = [[random.randint(0, self.gridSize - 1), random.randint(0, self.gridSize - 1)]]
		self.remainingMoves = [0 for x in range(self.gridSize ** 2)]
		self.CalculateRemainingMoves()
		self.remainingMoves[self.path[-1][0] + self.path[-1][1] * self.gridSize] = 0

		freetype.init()
		self.font = freetype.Font(None)

	def Main(self):
		while not self.done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.done = True

			# self.root.fill((0, 0, 0))

			if (len(self.path) > 1):
				lineCol = pygame.Color(255, 255, 255)
				lineCol.hsva = (int(len(self.path))%360, 100, 100, 100)
				pygame.draw.line(self.root, lineCol,
					[(self.path[-2][0] + 0.5) * self.gridWidth, (self.path[-2][1] + 0.5) * self.gridHeight],
					[(self.path[-1][0] + 0.5) * self.gridWidth, (self.path[-1][1] + 0.5) * self.gridHeight],
				1)

			# if (len(self.path) > 0):
			# 	lineCol = pygame.Color(255, 255, 255)
			# 	lineCol.hsva = (int(len(self.path)/5)%360, 100, 100, 100)
			# 	pygame.draw.circle(self.root, lineCol,
			# 		[(self.path[-1][0] + 0.5) * self.gridWidth, (self.path[-1][1] + 0.5) * self.gridHeight],
			# 	5)
				# pygame.draw.rect(self.root, lineCol,
				# 	[(self.path[-1][0] + 0.5) * self.gridWidth, (self.path[-1][1] + 0.5) * self.gridHeight,
				# 	self.gridWidth, self.gridHeight],
				# )

			self.UpdatePath()

			pygame.display.flip()

	def CalculateRemainingMoves(self):
		for i in range(self.gridSize ** 2):
			x = i % self.gridSize
			y = i // self.gridSize

			total = 0
			for point in self.knightMoves:
				if (-1 < x + point[0] < self.gridSize) and (-1 < y + point[1] < self.gridSize):
					total += 1
			self.remainingMoves[i] = total

	def RemoveMoves(self, pos):
		self.remainingMoves[pos[0] + pos[1] * self.gridSize] = 0

		for point in self.knightMoves:
			if (-1 < pos[0] + point[0] < self.gridSize) and (-1 < pos[1] + point[1] < self.gridSize):
				self.remainingMoves[(pos[0] + point[0]) + (pos[1] + point[1]) * self.gridSize] -= 1

	def UpdatePath(self):
		weights = [-1 for x in range(8)]

		minVal = 9
		for i, pos in enumerate(self.knightMoves):
			if (-1 < self.path[-1][0] + pos[0] < self.gridSize) and (-1 < self.path[-1][1] + pos[1] < self.gridSize):
				tileVal = self.remainingMoves[self.path[-1][0] + pos[0] + (self.path[-1][1] + pos[1]) * self.gridSize]
				if (tileVal > 0):
					minVal = min(minVal, tileVal)
					weights[i] = tileVal
		num = 0
		for weight in weights: num = num + 1 if weight == minVal else num
		if (num > 0):
			move = random.randint(0, num - 1)
			decision = 0
			for i in range(8):
				if weights[i] == minVal:
					if (move == 0):
						decision = i
						break
					else:
						move -= 1

			self.path.append([self.path[-1][0] + self.knightMoves[decision][0], self.path[-1][1] + self.knightMoves[decision][1]])
			self.RemoveMoves(self.path[-1])
		else:
			if (len(self.path) == (self.gridSize**2 - 1)):
				for pos in self.knightMoves:
					if (-1 < self.path[-1][0] + pos[0] < self.gridSize) and (-1 < self.path[-1][1] + pos[1] < self.gridSize):
						if self.remainingMoves[self.path[-1][0] + pos[0] + (self.path[-1][1] + pos[1]) * self.gridSize] == 0:
							self.path.append([self.path[-1][0] + pos[0], self.path[-1][1] + pos[1]])

			elif (len(self.path) < self.gridSize**2 - 1):
				self.root.fill((0, 0, 0))
				self.path = [[random.randint(0, self.gridSize - 1), random.randint(0, self.gridSize - 1)]]
				self.remainingMoves = [0 for x in range(self.gridSize ** 2)]
				self.CalculateRemainingMoves()
				self.remainingMoves[self.path[-1][0] + self.path[-1][1] * self.gridSize] = 0

if __name__ == "__main__":
	Tour().Main()
