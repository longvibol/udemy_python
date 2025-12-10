while True:
    user_action = input("Type add, edit or show or exit: ").strip()

    match user_action:
        case "add":
            todo = input("Enter a todo item: ") +"\n"
            # open the file
            file=open("files/todos.txt", "r")
            todos = file.readlines()
            file.close()

            # we get the list of file
            todos.append(todo)
            file =open("files/todos.txt", "w")
            file.writelines(todos)
            file.close()
        case "show":
            file = open("files/todos.txt", "r")
            todos = file.readlines()
            file.close()

            for index, item in enumerate(todos):
                item = item.strip('\n')
                row= f"{index+1}-{item}"
                print(row)

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