from email import message_from_file

while True:
    user_action = input("Type add, edit, del or show or exit: ").strip()

    match user_action:
        case "add":
            todo = input("Enter a todo item: ") +"\n"
            # open the file
            with open("files/todos.txt", "r") as file:
                todos = file.readlines()

            todos.append(todo)
            # we get the list of file
            with open("files/todos.txt", "w") as file:
                file.writelines(todos)

        case "show":
            with open("files/todos.txt", "r") as file:
                todos = file.readlines()

            for index, item in enumerate(todos):
                item = item.strip('\n')
                row= f"{index+1}-{item}"
                print(row)

        case "edit":
            with open("files/todos.txt", "r") as file:
                todos = file.readlines()

            # Display current list
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

                with open("files/todos.txt", "w") as file:
                    file.writelines(todos)

                # ✅ Show updated list (same as case "show")
                print("\nUpdated list:")
                for index, item in enumerate(todos):
                    item = item.strip('\n')
                    row = f"{index + 1}-{item}"
                    print(row)

            except ValueError:
                print("Please enter a valid number.")

        case "del":
            with (open("files/todos.txt", "r")) as file:
                todos = file.readlines()

            for index, item in enumerate(todos):
                print(index +1,"-", item.strip('\n'))
            number = int(input("Enter a number: ")) - 1

            del_item = todos[number].strip('\n')
            todos.pop(number)

            with open("files/todos.txt", "w") as file:
                file.writelines(todos)
            print(f'''Todo " {del_item} ", has been deleted.''')
        case "exit":
            break
        case _:
            print("Invalid input")
print("Goodbye!")