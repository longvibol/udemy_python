user_prompt = "Enter a todo: "
todos=[]
user_prompt.title()
user_prompt.capitalize()

while True:
    todo = input(user_prompt)
    todos.append(todo)
    print(todos)