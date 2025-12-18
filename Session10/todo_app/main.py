def get_todos(file_path):
    with open(file_path, "r") as file_local:
        todos_local = file_local.readlines()
    return todos_local

def write_todos(f,todos_arg):
    with open(f, "w") as file_local:
        file_local.writelines(todos_arg)

file_path = "files/todos.txt"

while True:
    user_action = input("✅Type add, edit, del, show, clear or exit: ").strip()

    if user_action.startswith("add"):
        todo = user_action[4:]

        todos = get_todos(file_path)

        todos.append(todo + "\n")

        write_todos(file_path, todos)

    elif user_action.startswith("show"):
        todos = get_todos(file_path)

        for index, item in enumerate(todos):
            item = item.strip('\n')
            row = f"{index+1}-{item}"
            print(row)

    elif user_action.startswith("edit"):
        todos = get_todos(file_path)

        for index, item in enumerate(todos):
            item = item.strip('\n')
            row = f"{index + 1}-{item}"
            print(row)

        try:
            index = int(input("Enter a number: ")) - 1
            if index < 0 or index >= len(todos):
                print("Invalid number. Please try again.")
                continue

            edit_item = input("Please input your new edit: ")
            todos[index] = edit_item + "\n"

            write_todos(file_path, todos)

            print("\nUpdated list:")
            for index, item in enumerate(todos):
                item = item.strip('\n')
                row = f"{index + 1}-{item}"
                print(row)

        except ValueError:
            print("Please enter a valid number.")
            continue

    elif user_action.startswith("del"):
        todos = get_todos(file_path)

        for index, item in enumerate(todos):
            print(index + 1, "-", item.strip('\n'))

        try:
            number = int(input("Enter a number: ")) - 1
            del_item = todos[number].strip('\n')
            todos.pop(number)

            write_todos(file_path, todos)
            print(f'Todo "{del_item}" has been deleted.')

        except (IndexError, ValueError):
            print(f"Please enter a valid number (from 1 to {len(todos)}).")
            # ✅ continue goes back to the main menu loop
            continue

    elif "exit" in user_action:
        break
    else:
        print("Invalid input. Please try again.")

print("Goodbye!")