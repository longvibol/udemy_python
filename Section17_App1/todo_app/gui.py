from modules import functions
import FreeSimpleGUI as sg

label = sg.Text("Type in a to-do")
input_box = sg.InputText(tooltip="Enter todo", key="todo")
add_button = sg.Button("Add")
list_box = sg.Listbox(values=functions.get_todos(), key="todos",
                      enable_events=True, size=(45, 10))
edit_button = sg.Button("Edit")
layout = [[label], [input_box, add_button], [list_box, edit_button]]

window = sg.Window(
    "My To-Do App",
    layout= layout,
    font=("Times New Roman", 20),
)

while True:
    event, values = window.read()
    print(1, event)
    print(2, values)

    # Safe print: only when a selection exists
    selected = values.get("todos")
    if selected:
        print(3, selected[0])

    match event:
        case "Add":
            new_todo = values.get("todo", "").strip()
            if new_todo:
                todos = functions.get_todos()
                todos.append(new_todo + "\n")  # keep consistent with add
                functions.write_todos(todos)
                window["todos"].update(values=todos)
                window["todo"].update(value="")  # clear input

        case "Edit":
            selected = values.get("todos")
            new_todo = values.get("todo", "").strip()
            if selected and new_todo:
                todos = functions.get_todos()
                idx = todos.index(selected[0])
                todos[idx] = new_todo + "\n"  # keep consistent with add
                functions.write_todos(todos)
                window["todos"].update(values=todos)

        case "todos":
            selected = values.get("todos")
            if selected:
                window["todo"].update(value=selected[0].strip())

        case sg.WIN_CLOSED:
            break

window.close()