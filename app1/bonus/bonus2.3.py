todos = []

while True:
    user_action = input("Type add, edit or show: ").strip()

    match user_action:
        case "add":
            todo = input("Enter a todo item: ")
            todos.append(todo)
        case "show" | "s":
            for item in todos:
                item = item.title()
                print(item)
        case "edit":
            print(todos)
            number = int(input("Enter a number: ")) -1
            print(todos[number])
            edit_item = input("Please input your edit: ")
            todos[number] = edit_item
            print(todos)
        case "exit":
            break
        case _:
            print("Invalid input")
print("Goodbye!")