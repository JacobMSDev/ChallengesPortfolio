import PrimeTest

def primeValTest():
	with open("testData.txt") as f:
		primeList = []

		# Ignore first 4 lines of file
		for x in range(4):
			f.readline()
		for x in f:
			# Split lines into the numbers
			nums = x.split()
			if nums != []:
				# Test each number
				for val in nums:
					# assert PrimeTest.IsPrime(int(val)) == True, "Failed value is: " + val
					primeList.append(int(val))

					# If primes up to 100000 have been collected, break
					if primeList[-1] > 100000:
						break
			if primeList[-1] > 100000:
				break


		# Perform prime test on all n from 1 to 100000
		for i in range(1, 100000):
			res = PrimeTest.IsPrime(i)	# Result of prime test
			comp = i in primeList		# Expected result
			assert res == comp, "Failed on: " + str(i) + ". Got " + str(res) + ", expected " + str(comp)

if __name__ == "__main__":
	primeValTest()
	print("All tests passed!")
