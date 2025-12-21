FILEPATH = "files/todos.txt"

def get_todos(filepath = FILEPATH):
    """ Read a text file and return the list of todos """
    with open(filepath, "r") as file_local:
        todos_local = file_local.readlines()
    return todos_local

# procedure
def write_todos(todos_arg, filepath = FILEPATH):
    """ Write a text file to a list of todos """
    with open(filepath, "w") as file_local:
        file_local.writelines(todos_arg)


if __name__ == "__main__":
    print(__name__)
    print("Hello")