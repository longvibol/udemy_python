todos = []

while True:
    user_action = input("Type add, edit or show or exit: ").strip()

    match user_action:
        case "add":
            todo = input("Enter a todo item: ")
            todos.append(todo)
        case "show" | "s":
            for index, item in enumerate(todos):
                row= f"{index+1}. {item}"
                print(row)
            # print(f"==>length {index + 1}")
        case "edit":
            number = int(input("Enter a number: ")) -1
            print(todos[number])
            edit_item = input("Please input your edit: ")
            todos[number] = edit_item
            print(todos)
        case "com":
            for index, item in enumerate(todos):
                print(index +1,"-", item)
            number = int(input("Enter a number: ")) - 1
            todos.pop(number)
        case "exit":
            break
        case _:
            print("Invalid input")
print("Goodbye!")