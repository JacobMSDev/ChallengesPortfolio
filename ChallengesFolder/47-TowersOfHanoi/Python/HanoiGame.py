import pygame
import Piece

''' Test the collision between a box and a point '''
def boxCollision(boxPos, ptPos, boxW, boxH):
	return (boxPos[0] < ptPos[0] < boxPos[0] + boxW) and (boxPos[1] < ptPos[1] < boxPos[1] + boxH)

class HanoiTowers():
	def __init__(self):
		self.rootWidth, self.rootHeight = 600, 600 # Window size
		self.root = pygame.display.set_mode([self.rootWidth, self.rootHeight]) # Main dispaly
		self.clock = pygame.time.Clock() # Pygame clock to control framerate

		self.done = False 			# Continue the program or stop

		self.towers = [[], [], []]	# The towers
		self.pieceCount = 9			# The number of pieces
		self.heldPiece = None		# The currently held piece
		self.heldOver = -1			# Last tower the held piece was over or on

		# Render settings
			# Base and poles
		self.baseOffset = int(self.rootWidth * 0.05)
		self.baseWidth = int(self.rootWidth - 2 * self.baseOffset)
		self.pillarWidth = int(self.rootWidth * 0.03)
			# pieces
		self.pieceHeight = int(self.rootHeight * 0.68 / self.pieceCount)
		self.pieceWidth = int(self.baseWidth * 0.3)

		self.mouseRelease = False # Track if the mouse has been released once pressed

		# Generate 'pieceCount' number of pieces
		for i in range(self.pieceCount):
			# Determine piece width (Higher 'i' -> Thinner piece)
			pieceW = self.pieceWidth - self.pieceWidth * 0.8 * i / self.pieceCount
			# Determine initial piece position on screen
			pieceX = int(self.baseOffset + self.baseWidth * 0.33 * 0.5 - pieceW / 2)
			pieceY = int(self.rootHeight * 0.9 - (i + 1) * self.pieceHeight)
			# Generate piece colour using HSVA values
			col = pygame.Color(255, 0, 0)
			col.hsva = (360 * i / self.pieceCount, 100, 100, 100)
			self.towers[0].append(Piece.GamePiece(
					col,				# Piece colour
					pieceW,				# Piece width
					[pieceX, pieceY]	# Piece position
				))

	def Main(self):
		while not self.done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.done = True

			self.root.fill((0, 0, 0))	# Clear screen

			self.renderBase()			# Render base of the game
			self.renderPillars()		# Render pillars and pieces on pillars
			self.movePiece()			# Render and control selected piece
			self.renderPiece()			# Render the pieces over the pillars

			self.clock.tick(60)			# Set the framerate to 60 fps

			pygame.display.flip()		# Refresh screen

	def renderPillars(self):
		# Draw pillars
		for i, tower in enumerate(self.towers):
			pillarPos = self.baseWidth * 0.33 * (i + 0.5) # Calculate pillars position across base
			pygame.draw.rect(self.root, (150, 150, 150), [
					pillarPos + self.baseOffset - self.pillarWidth / 2, self.rootHeight * 0.2, # Position
					self.pillarWidth, self.rootHeight * 0.7 # Size
				])

	def renderBase(self):
		# Draw base plate
		pygame.draw.rect(self.root, (170, 170, 170), [
				self.baseOffset, self.rootHeight * 0.9, # Position
				self.baseWidth, self.rootHeight * 0.05 # Size
			])

	def renderPiece(self):
		# Draw pieces
		for i, tower in enumerate(self.towers):
			# Draw pieces
			for piece in tower:
				pygame.draw.rect(self.root, piece.col, [*piece.pos, piece.width, self.pieceHeight])

	def movePiece(self):
		pos = pygame.mouse.get_pos() # Position of mouse
		tIndex = min(max(0, int((pos[0] - self.baseOffset) /  self.baseWidth * 3)), 2) # Tower the mouse is over
		validTower = True # Can the held piece go on the hovered tower
		fallSpeed = 0 # Speed the piece falls at if released

		# Is a piece held
		if (self.heldPiece != None):
			# Can the piece go on the hovered tower?
			if (len(self.towers[self.heldOver]) == 0 or self.heldPiece.width < self.towers[self.heldOver][-1].width):
				# Yes
				towerHeight = self.rootHeight * 0.9 - (len(self.towers[self.heldOver]) + 1) * self.pieceHeight
				# Speed is calculated by an exponential so the piece falls faster the further it must travel
				fallSpeed = max(6, 2**abs((towerHeight - self.heldPiece.pos[1]) / towerHeight * 3 + 3))
			else:
				# No
				towerHeight = self.rootHeight * 0.2 - self.pieceHeight / 2
				fallSpeed = 0
				validTower = False

		# Is the user pressing the left mouse button
		if pygame.mouse.get_pressed()[0]:
			# No piece is currently held
			if (self.heldPiece == None):
				for i, tower in enumerate(self.towers):
					# Check there are pieces on the tower
					if (len(tower) > 0):
						# Test if the mouse is over the top piece on the tower
						if boxCollision(tower[-1].pos, pos, tower[-1].width, self.pieceHeight):
							self.heldPiece = self.towers[i].pop() # Remove the piece from tower and put into self.heldPiece
							self.heldOver = i
							break

			else:
				# Test if a piece is being dragged or the mouse is over the piece while clicking
				if boxCollision(self.heldPiece.pos, pos, self.heldPiece.width, self.pieceHeight) or self.mouseRelease == False:
					self.mouseRelease = False # Allow piece to be held

					# Let piece track mouse Y-position
					self.heldPiece.pos[1] = min(
						pos[1] - self.pieceHeight / 2,	# Cursor height on piece
						towerHeight
					)

					# Held piece is above the pillars
					if (self.heldPiece.pos[1] < self.rootHeight * 0.2 - self.pieceHeight):
						self.heldOver = tIndex
						# Set held piece X-position to math the mouse
						self.heldPiece.pos[0] = pos[0] - self.heldPiece.width / 2
					# Mouse is over the same pillar the piece is on
					elif (tIndex == self.heldOver):
						pillarPos = self.baseWidth * 0.33 * (tIndex + 0.5)
						# Set held piece X-position to match the pillar
						self.heldPiece.pos[0] = pillarPos + self.baseOffset - self.heldPiece.width / 2
				else:
					# If piece is on a pillar, let it fall
					if (self.heldPiece.pos[1] > self.rootHeight * 0.2 - self.pieceHeight):
						self.heldPiece.pos[1] = min(self.heldPiece.pos[1] + fallSpeed, towerHeight)

		# Mouse released but a piece is still held
		elif (self.heldPiece != None):
			self.mouseRelease = True

			# Has the piece landed in a valid position
			if (self.heldPiece.pos[1] == towerHeight and validTower):
				self.towers[self.heldOver].append(self.heldPiece) # Add held piece to tower
				self.heldPiece = None # Clear the held piece

			else:
				# If piece is on a pillar, let it fall
				if (self.heldPiece.pos[1] > self.rootHeight * 0.2 - self.pieceHeight):
					self.heldPiece.pos[1] = min(self.heldPiece.pos[1] + fallSpeed, towerHeight)

		# Render the currently held piece
		if (self.heldPiece != None):
			pygame.draw.rect(self.root, self.heldPiece.col, [
				*self.heldPiece.pos,
				self.heldPiece.width, self.pieceHeight
			])

if __name__ == "__main__":
	HanoiTowers().Main()
