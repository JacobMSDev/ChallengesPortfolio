
from PIL import Image

def getNewCol(oldCol, nc):
	return (getNewRGBVal(oldCol[0], nc), getNewRGBVal(oldCol[1], nc), getNewRGBVal(oldCol[2], nc))

def getNewRGBVal(oldVal, nc):
	return round((oldVal * (nc - 1)), 0) / (nc - 1)

for num in [2, 4, 8, 16, 32]:
	with Image.open("blackAndWhite.jpg") as inImage:
		imgWidth = inImage.getbbox()[2]
		imgHeight = inImage.getbbox()[3]
		pixels = list(inImage.getdata())

		# Convert each pixel to range [0, 1]
		for i in range(len(pixels)):
			pixel = pixels[i]
			pixels[i] = (pixel[0]/255, pixel[1]/255, pixel[2]/255)

		# # Algorithm
		# for i in range(len(pixels)):
		# 	pixel = pixels[i]
		# 	pixels[i] = getNewCol(pixel, num)

		# Dithering
		for y in range(imgHeight - 1):
			for x in range(imgWidth - 1):
				old = pixels[x + y * imgWidth]
				new = getNewCol(old, num)
				pixels[x + y * imgWidth] = new

				err = (old[0] - new[0], old[1] - new[1], old[2] - new[2])

				col = pixels[(x + 1) + y * imgWidth]
				pixels[(x + 1) + y * imgWidth] = (col[0] + err[0] * 7/16, col[1] + err[1] * 7/16, col[2] + err[2] * 7/16)

				col = pixels[(x - 1) + (y + 1) * imgWidth]
				pixels[(x - 1) + (y + 1) * imgWidth] = (col[0] + err[0] * 3/16, col[1] + err[1] * 3/16, col[2] + err[2] * 3/16)

				col = pixels[x + (y + 1) * imgWidth]
				pixels[x + (y + 1) * imgWidth] = (col[0] + err[0] * 5/16, col[1] + err[1] * 5/16, col[2] + err[2] * 5/16)

				col = pixels[(x + 1) + (y + 1) * imgWidth]
				pixels[(x + 1) + (y + 1) * imgWidth] = (col[0] + err[0] * 1/16, col[1] + err[1] * 1/16, col[2] + err[2] * 1/16)

		# Convert each pixel to range [0, 255]
		for i in range(len(pixels)):
			pixel = pixels[i]
			pixels[i] = (min(int(pixel[0]*255), 255), min(int(pixel[1]*255), 255), min(int(pixel[2]*255), 255))

		outputImage = Image.new("RGB", [imgWidth, imgHeight])
		for y in range(imgHeight):
			for x in range(imgWidth):
				outputImage.putpixel([x, y], pixels[x + y * imgWidth])
		outputImage.save("output" + str(num) + ".jpg")
		outputImage.close()
