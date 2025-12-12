date = input("Enter a date: ")
mood = input("Enter a mood from 1 to 10: ")
thought = input("what is on your mind: \n")

with open(f"./journal/{date}.txt","w") as file:
    file.write(mood + 2 * "\n")
    file.write(thought)