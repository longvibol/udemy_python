import random

# Generate a random integer between start and stop (inclusive)
start = int(input("enter the starting number: "))
stop = int(input("enter the ending number: "))
num = random.randint(start +1, stop-1)

print(num)