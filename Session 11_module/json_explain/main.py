import json

# ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

# Load questions from file
with open('questions.json', 'r') as file:
    data = json.load(file)

score = 0

# Ask questions
for question in data:
    print(question["question_text"])
    for index, alternative in enumerate(question["alternatives"], start=1):
        print(index, "-", alternative)

    # Input validation
    while True:
        try:
            user_choice = int(input("Enter your choice: "))
            if 1 <= user_choice <= len(question["alternatives"]):
                break
            else:
                print("Invalid choice. Please enter a number between 1 and", len(question["alternatives"]))
        except ValueError:
            print("Invalid input. Please enter a number.")

    question["user_choice"] = user_choice

    if user_choice == question["correct_answer"]:
        score += 1

# Show results
print("\n--- Results ---")
for index, question in enumerate(data, start=1):
    user_answer_text = question["alternatives"][question["user_choice"] - 1]
    correct_answer_text = question["alternatives"][question["correct_answer"] - 1]

    # Add colored symbols ✔️ (green) or ✘ (red)
    if question["user_choice"] == question["correct_answer"]:
        symbol = f"{GREEN}✔️{RESET}"
    else:
        symbol = f"{RED}✘{RESET} | Correct answer-{question['correct_answer']}: {correct_answer_text}"

    message = f"{index}.Your answer: {user_answer_text} {symbol}"
    print(message)

print(f"\nYour Score: {score}/{len(data)}")