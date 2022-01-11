'''

!!!NOTE!!!
This file was used for testing the program.
Running it will fill the 'Output' folder with
many images generated from the process. This may
require a lot of storage so be advised before using.


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

	# Define the storage arrays for the process
	storage = [0 for x in range(imgWidth * imgHeight)]
	energy = [0 for x in range(imgWidth * imgHeight)]
	# The area affected by pixel removal
	minX, maxX = 0, imgWidth

	for i in range(10):
		# Gradient stage
		# Determine the gradient magnitude of each pixel
		# i.e. higher value, more contrast between that pixel and its neighbours
		gradientStage = Image.new("RGB", [imgWidth, imgHeight])
		for y in range(imgHeight):
			for x in range(max(0, minX - 1), min(imgWidth, maxX + 1)):
				A = (0, 0, 0) if y == 0 else pixels[x + (y - 1) * imgWidth] 				# Pixel above focus
				B = (0, 0, 0) if y == (imgHeight - 1) else pixels[x + (y + 1) * imgWidth] 	# Pixel below focus
				C = (0, 0, 0) if x == 0 else pixels[(x - 1) + y * imgWidth]					# Pixel left of focus
				D = (0, 0, 0) if x == (imgWidth - 1) else pixels[(x + 1) + y * imgWidth]	# Pixel right of focus

				dist1 = (A[0] - B[0]) + (A[1] - B[1]) + (A[2] - B[2])
				dist2 = (C[0] - D[0]) + (C[1] - D[1]) + (C[2] - D[2])

				val = int((dist1**2 + dist2**2)**0.5)

				storage[x + y * imgWidth] = val

		for y in range(imgHeight):
			for x in range(imgWidth):
				val = storage[x + y * imgWidth]
				gradientStage.putpixel([x, y], (val, val, val))
		gradientStage.save("Output/A-" + str(i) + ".png")
		# Gradient stage

		for x in range(imgWidth):
			energy[x] = storage[x]

		# Seam stage
		for y in range(0, imgHeight - 1):
			for x in range(imgWidth):
				base = storage[x + (y + 1) * imgWidth]
				abovePixel = energy[x + y * imgWidth]
				leftIndex = (x - 1) + y * imgWidth
				rightIndex = (x + 1) + y * imgWidth

				# Add the minimum of the above 3 pixels
				if (x == 0):
					energy[x + (y + 1) * imgWidth] = base + min(abovePixel, energy[rightIndex])
				elif (x == imgWidth - 1):
					energy[x + (y + 1) * imgWidth] = base + min(energy[leftIndex], abovePixel)
				else:
					energy[x + (y + 1) * imgWidth] = base + min(min(energy[leftIndex], abovePixel), energy[rightIndex])

		lim = max(energy)
		seamStage = Image.new("RGB", [imgWidth, imgHeight])
		for y in range(imgHeight):
			for x in range(imgWidth):
				col = int(energy[x + y * imgWidth] / lim * 255)
				seamStage.putpixel([x, y], (col, col, col))

		# Determine the lowest energy pixel along the bottom row of the image
		minVal = 1000000
		index = 0
		for x in range(imgWidth):
			sample = energy[x + (imgHeight - 1) * imgWidth]
			if sample < minVal:
				minVal = sample
				index = x

		seamStage.putpixel([index, imgHeight - 1], (0, 0, 255))

		points = [[index, imgHeight - 1]]

		minX, maxX = index, index # Horizontal bounds of the seam
		# Work up the image, determining the seem
		for y in range(imgHeight - 2, -1, -1):
			A = energy[index + y * imgWidth]
			B = 1000000 if index == 0 else energy[(index - 1) + y * imgWidth]
			C = 1000000 if index == (imgWidth - 1) else energy[(index + 1) + y * imgWidth]

			# Shift the working X-pos to the minimum energy
			smallest = min(A, min(B, C))
			if smallest == B:
				index -= 1
			elif smallest == C:
				index += 1

			seamStage.putpixel([index, y], (0, 255, 0))

			# Remove the pixel from all arrays
			pixels.pop(index + y * imgWidth)
			storage.pop(index + y * imgWidth)
			energy.pop(index + y * imgWidth)

			# Track the bounds of the seam
			if (index < minX):
				minX = index
			if (index > maxX):
				maxX = index

		seamStage.save("Output/B-" + str(i) + ".png")
		
		imgWidth -= 1
		# Seam stage

		# Finishing stage
		finalOutputImage = Image.new("RGB", [imgWidth, imgHeight])
		for y in range(imgHeight):
			for x in range(imgWidth):
				finalOutputImage.putpixel([x, y], pixels[x + y * imgWidth])
		finalOutputImage.save("Output/C-" + str(i) + ".png")
		# Finishing stage

		print("{:.2f}%".format((i + 1) / 10 * 100), end="\r")

		gradientStage.close()
		seamStage.close()
		finalOutputImage.close()
