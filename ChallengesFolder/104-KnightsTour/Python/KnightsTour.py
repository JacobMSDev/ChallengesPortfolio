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

				# if event.type == pygame.MOUSEBUTTONDOWN:

			if pygame.mouse.get_pressed()[0]:
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
					self.removeMoves(self.path[-1])
				else:
					if (len(self.path) == (self.gridSize**2 - 1)):
						for pos in self.knightMoves:
							if self.remainingMoves[self.path[-1][0] + pos[0] + (self.path[-1][1] + pos[1]) * self.gridSize] == 0:
								self.path.append([self.path[-1][0] + pos[0], self.path[-1][1] + pos[1]])

			self.root.fill((0, 0, 0))

			for y in range(self.gridSize):
				for x in range(self.gridSize):
					# Create checkerboard pattern with the colours
					col = self.colA if ((x & 1) ^ (y & 1)) else self.colB
					pygame.draw.rect(self.root, col, [x * self.gridWidth, y * self.gridHeight, self.gridWidth + 1, self.gridHeight + 1])

			for point in self.path:
				pygame.draw.rect(self.root, (0, 0, 0), [point[0] * self.gridWidth, point[1] * self.gridHeight, self.gridWidth + 1, self.gridHeight + 1])

			for i in range(len(self.path) - 1):
				lineCol = pygame.Color(255, 255, 255)
				lineCol.hsva = (i%360, 100, 100, 100)
				pygame.draw.line(self.root, lineCol,
					[(self.path[i][0] + 0.5) * self.gridWidth, (self.path[i][1] + 0.5) * self.gridHeight],
					[(self.path[i + 1][0] + 0.5) * self.gridWidth, (self.path[i + 1][1] + 0.5) * self.gridHeight],
				3)

			# for i, val in enumerate(self.remainingMoves):
				# self.font.render_to(self.root, [i%self.gridSize*self.gridWidth, i//self.gridSize*self.gridHeight], str(val), (0, 0, 0), size = int(self.gridHeight * 0.5))

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

	def removeMoves(self, pos):
		self.remainingMoves[pos[0] + pos[1] * self.gridSize] = 0

		for point in self.knightMoves:
			if (-1 < pos[0] + point[0] < self.gridSize) and (-1 < pos[1] + point[1] < self.gridSize):
				self.remainingMoves[(pos[0] + point[0]) + (pos[1] + point[1]) * self.gridSize] -= 1

if __name__ == "__main__":
	Tour().Main()
