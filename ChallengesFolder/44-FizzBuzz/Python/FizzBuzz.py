# Standard implementation
n = 50
for i in range(1, n):
	if (i % 15 == 0):
		print("FizzBuzz")
	elif (i % 5 == 0):
		print("Buzz")
	elif (i % 3 == 0):
		print("Fizz")
	else:
		print(i)

# One line implementation
# !!! BAD PRACTICE AND PURELY AS AN EXAMPLE !!! #
for i in range(1, 20): print(i, "\rFizz" * (i%3 == 0) + "\rBuzz" * (i%5 == 0) + "\rFizzBuzz" * (i%15 == 0))
