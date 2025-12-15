while True:
    user_action = input("Type add, edit, del or show or exit: ").strip()

    if "add" in user_action:
        todo = user_action[4:]
        with open("files/todos.txt", "r") as file:
            todos = file.readlines()

        todos.append(todo)
        # we get the list of file
        with open("files/todos.txt", "w") as file:
            file.writelines(todos)

    elif "show" in user_action:
        with open("files/todos.txt", "r") as file:
            todos = file.readlines()

        for index, item in enumerate(todos):
            item = item.strip('\n')
            row= f"{index+1}-{item}"
            print(row)

    elif "edit" in user_action:

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

    elif "del" in user_action:

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
    elif "exit" in user_action:
        break
    else:
        print("Invalid input. Please try again.")
print("Goodbye!")