import functions as fun
import time

now = time.strftime('%b %d, %Y %H:%S')
print("It is", now)

while True:
    user_action = input("✅Type add, edit, del, show, clear or exit: ").strip()

    if user_action.startswith("add"):
        todo = user_action[4:]

        todos = fun.get_todos()

        todos.append(todo + "\n")

        fun.write_todos(todos)

    elif user_action.startswith("show"):
        todos = fun.get_todos()

        for index, item in enumerate(todos):
            item = item.strip('\n')
            row = f"{index+1}-{item}"
            print(row)

    elif user_action.startswith("edit"):
        todos = fun.get_todos()

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

            fun.write_todos(todos)

            print("\nUpdated list:")
            for index, item in enumerate(todos):
                item = item.strip('\n')
                row = f"{index + 1}-{item}"
                print(row)

        except ValueError:
            print("Please enter a valid number.")
            continue

    elif user_action.startswith("del"):
        todos = fun.get_todos()

        for index, item in enumerate(todos):
            print(index + 1, "-", item.strip('\n'))

        try:
            number = int(input("Enter a number: ")) - 1
            del_item = todos[number].strip('\n')
            todos.pop(number)

            fun.write_todos(todos)
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