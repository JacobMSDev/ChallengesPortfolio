from PIL import Image

# charList = ["@", "#", "$", "%", "&", "(", ")", "=", "!", ",", "."]
# charList = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", " "]
charList = "�@#&$%=+-!^*;,. "
charCount = len(charList)

with Image.open("testImage.png") as inImage:
	imgWidth = inImage.getbbox()[2]
	imgHeight = inImage.getbbox()[3]
	pixels = list(inImage.getdata())

	result = ""

	for y in range(imgHeight):
		for x in range(imgWidth):
			val = pixels[x + y * imgWidth][0]
			index = int(val/255 * (charCount - 1))
			# print(val, index)
			result += charList[index]
		result += "\n"

	with open("output.txt", "w") as f:
		f.write(result)
