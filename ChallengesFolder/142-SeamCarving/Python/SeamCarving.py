'''

Programming Challenge 142
Seam carving

Started: 7/1/2022
Finished: 11/1/2022

'''

from PIL import Image

# Create a very large number as a 'maximum' for cases where
# comparing minimums
largeNumber = 10**20

fileName = input("Please enter file name (With extension!)\n >>> ")
with Image.open(fileName) as inImage:
	# Get the necessary information from the image
	imgWidth = inImage.getbbox()[2]
	imgHeight = inImage.getbbox()[3]
	pixels = list(inImage.getdata())

	# Determine the numbers of pixels to be removed from the image
	toRemove = 0
	while True:
		try:
			toRemove = int(input("\nThe image is %d pixels wide. Please enter desired width\n >>> " % (imgWidth)))
			if (0 < toRemove < imgWidth):
				break
			else:
				print("The amount to remove must be less than the image width.")
		except ValueError:
			print("Please enter a valid number.")

	print("")

	# Define the storage arrays for the process
	storage = [0 for x in range(imgWidth * imgHeight)]
	energy = [0 for x in range(imgWidth * imgHeight)]
	# The area affected by pixel removal
	minX, maxX = 0, imgWidth

	toRemove = imgWidth - toRemove

	for i in range(toRemove):
		# Gradient stage
		# Determine the gradient magnitude of each pixel
		# i.e. higher value, more contrast between that pixel and its neighbours
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
		# Gradient stage

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
		
		minVal = largeNumber
		index = 0
		# Determine the lowest energy pixel along the bottom row of the image
		for x in range(imgWidth):
			sample = energy[x + (imgHeight - 1) * imgWidth]
			if sample < minVal:
				minVal = sample
				index = x

		minX, maxX = index, index # Horizontal bounds of the seam
		# Work up the image, determining the seem
		for y in range(imgHeight - 1, -1, -1):
			A = energy[index + y * imgWidth]
			B = largeNumber if index == 0 else energy[(index - 1) + y * imgWidth]
			C = largeNumber if index == (imgWidth - 1) else energy[(index + 1) + y * imgWidth]

			# Shift the working X-pos to the minimum energy
			smallest = min(A, min(B, C))
			if smallest == B:
				index -= 1
			elif smallest == C:
				index += 1

			# Remove the pixel from all arrays
			pixels.pop(index + y * imgWidth)
			storage.pop(index + y * imgWidth)
			energy.pop(index + y * imgWidth)

			# Track the bounds of the seam
			if (index < minX):
				minX = index
			if (index > maxX):
				maxX = index

		imgWidth -= 1
		# Seam stage

		# Print the progress (as a %) so far
		print("{:.2f}%".format((i + 1) / toRemove * 100), end="\r")

	# Create output image
	finalOutputImage = Image.new("RGB", [imgWidth, imgHeight])
	for y in range(imgHeight):
		for x in range(imgWidth):
			finalOutputImage.putpixel([x, y], pixels[x + y * imgWidth])
	finalOutputImage.save("OutputImage.png")
	finalOutputImage.close()

	input("\n\nCompleted!\nPress enter to close")
