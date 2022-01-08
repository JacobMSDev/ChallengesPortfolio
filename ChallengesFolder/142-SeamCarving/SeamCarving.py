'''

Programming Challenge 142
Seam carving

Started: 7/1/2022
Finished

'''

from PIL import Image

with Image.open("referenceImage.png") as inImage:
	imgWidth = inImage.getbbox()[2]
	imgHeight = inImage.getbbox()[3]
	pixels = list(inImage.getdata())

	# Gradient stage
	gradientStage = Image.new("RGB", [imgWidth, imgHeight])
	storage = [0 for x in range(imgHeight * imgWidth)]
	for x in range(imgWidth):
		for y in range(1, imgHeight - 1):
			A = pixels[x + (y-1) * imgWidth]
			B = pixels[x + (y-2) * imgWidth]
			storage[x + y * imgWidth] = (B[0]-A[0])**2 + (B[1]-A[1])**2 + (B[2]-A[2])**2
	for y in range(imgHeight):
		for x in range(1, imgWidth - 1):
			A = pixels[(x - 1) + y * imgWidth]
			B = pixels[(x + 1) + y * imgWidth]
			col1 = (B[0]-A[0])**2 + (B[1]-A[1])**2 + (B[2]-A[2])**2
			col2 = storage[x + y * imgWidth]

			val = int((col1 + col2)**0.5)

			storage[x + y * imgWidth] = val
			gradientStage.putpixel([x, y], (val, val, val))
	gradientStage.save("gradentStage.png")
	# Gradient stage

	for y in range(imgHeight):
		for x in range(imgWidth):
			storage[x + y * imgWidth] = max(0, storage[x + y * imgWidth])

	# Generate seams stage
	seamStage = Image.new("RGB", [imgWidth, imgHeight])

	for y in range(1, imgHeight - 1):
		for x in range(imgWidth):
			# base = gradientStage.getpixel((x, y))[0]
			base = storage[x + y * imgWidth]
			if (x == 0):
				storage[x + y * imgWidth] = base + min(storage[x + (y - 1) * imgWidth], storage[(x + 1) + (y - 1) * imgWidth])
			elif (x == imgWidth - 1):
				storage[x + y * imgWidth] = base + min(storage[(x - 1) + (y - 1) * imgWidth], storage[x + (y - 1) * imgWidth])
			else:
				storage[x + y * imgWidth] = base + min(min(storage[(x - 1) + (y - 1) * imgWidth], storage[x + (y - 1) * imgWidth]), storage[(x + 1) + (y - 1) * imgWidth])


	lim = 3000
	for y in range(imgHeight):
		for x in range(imgWidth):
			col = int(storage[x + y * imgWidth] / lim * 255)
			col2 = gradientStage.getpixel((x, y))[0]
			seamStage.putpixel([x, y], (col, col2, 0))

	used = []

	remove = 100
	sub = int(200 / remove)
	for j in range(remove):
		valid = True

		points = []

		xPos = 0
		minVal = 1000000
		for i in range(1, imgWidth - 1):
			if (storage[i + (imgHeight - 2) * imgWidth] < minVal and storage[i + (imgHeight - 2) * imgWidth] not in used):
				minVal = storage[i + (imgHeight - 2) * imgWidth]
				xPos = i

		used.append(minVal)

		for y in range(imgHeight - 1, -1, -1):

			A = storage[xPos + y * imgWidth]
			offset = 1
			if (xPos > 1):
				if storage[(xPos - 1) + y * imgWidth] != 999999:
					B = storage[(xPos - 1) + y * imgWidth]
				else:
					B = 1000000
					valid = False
			else:
				B = 1000000
			if (xPos < imgWidth - 2):
				if storage[(xPos + 1) + y * imgWidth] != 999999:
					C = storage[(xPos + 1) + y * imgWidth]
				else:
					C = 1000000
					valid = False
			else:
				C = 1000000

			if not valid:
				break

			smallest = min(min(A, B), C)
			if (smallest == B):
				xPos -= offset
			elif (smallest == C):
				xPos += offset

			points.append([xPos, y])

		if valid:
			for k, point in enumerate(points):
				col = seamStage.getpixel((xPos, y))
				seamStage.putpixel([xPos, y], (col[0], col[1], 255 - sub * j))
				storage[point[0] + point[1] * imgWidth] = 999999
				pixels[point[0] + point[1] * imgWidth] = (255 - sub * j, 255 - sub * j, 255 - sub * j)

		# for y in range(imgHeight - 1, -1, -1):
		# 	A = storage[xPos + y * imgWidth]
		# 	if (xPos > 1):
		# 		B = storage[(xPos - 1) + y * imgWidth]
		# 	else:
		# 		B = 1000000
		# 	if (xPos < imgWidth - 2):
		# 		C = storage[(xPos + 1) + y * imgWidth]
		# 	else:
		# 		C = 1000000

		# 	smallest = min(min(A, B), C)
		# 	if (smallest == B):
		# 		xPos -= 1
		# 	elif (smallest == C):
		# 		xPos += 1

		# 	col = seamStage.getpixel((xPos, y))
		# 	seamStage.putpixel([xPos, y], (col[0], col[1], 255 - j))

		# 	points.append([xPos, y])

		# for k, point in enumerate(points):
		# 	storage.pop((point[0]) + point[1] * imgWidth)
		# 	pixels.pop((point[0]) + point[1] * imgWidth)

		# imgWidth -= 1

	# seamStage.save("seamStage.png")
	# Generate seams stage

	# Generate completed image
	# finalOutputImage = Image.new("RGB", [imgWidth, imgHeight])
	# for y in range(imgHeight):
	# 	for x in range(imgWidth):
	# 		finalOutputImage.putpixel([x, y], pixels[x + y * imgWidth])
	# finalOutputImage.save("finalImage.png")
	# Generate completed image

	gradientStage.close()
	seamStage.close()
	finalOutputImage.close()
