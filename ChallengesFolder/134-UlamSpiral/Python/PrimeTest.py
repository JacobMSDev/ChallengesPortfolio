
def IsPrime(num: int) -> bool:
	''' Test if a number is prime or not '''
	# Check for 2 or 3
	if (num < 4):
		return num > 1

	# Check for 2 or 3 division
	if (num % 2 == 0 or num % 3 == 0):
		return False

	# Next minimum prime
	i = 5
	# Iterature up to square root of num
	while i**2 < num + 1:
		# Attempt division by 1 above and 1 below
		# a multiple of 6
		if (num % i == 0 or num % (i + 2) == 0):
			return False
		i += 6
	# No divisors found, must be prime
	return True
