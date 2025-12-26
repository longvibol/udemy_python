from modules import functions
import FreeSimpleGUI as sg
import time

sg.theme("DarkBlue")

def refresh_list(window):
    # Option 2: file already contains numbering
    todos = functions.get_todos()
    window["todos"].update(values=todos)


clock = sg.Text('', key="clock")
label = sg.Text("Type in a to-do")
input_box = sg.InputText(tooltip="Enter todo", key="todo")
add_button = sg.Button("Add", bind_return_key=True, size=10)

list_box = sg.Listbox(values=functions.get_todos(), key="todos",
                      enable_events=True, size=(45, 10))
edit_button = sg.Button("Edit")
del_button = sg.Button("Delete", key="del")
exit_button = sg.Button("Exit", key="exit")

layout = [
    [clock],
    [label],
    [input_box, add_button],
    [list_box, edit_button, del_button],
    [exit_button]
]

# ✅ FIX: finalize=True so you can update elements before window.read()
window = sg.Window(
    "My To-Do App",
    layout=layout,
    font=("Times New Roman", 20),
    finalize=True
)

refresh_list(window)

while True:
    event, values = window.read(timeout=200)

    # ✅ CLOSE FIRST (critical)
    if event in (sg.WIN_CLOSED, "exit"):
        break

    # ✅ safe to update UI after close check
    window["clock"].update(time.strftime("%b %d, %Y %H:%M:%S"))

    match event:
        case "Add":
            new_todo = values.get("todo", "").strip()
            if new_todo:
                todos = functions.get_todos()
                next_number = len(todos) + 1
                todos.append(f"{next_number}. {new_todo}\n")
                functions.write_todos(todos)
                refresh_list(window)
                window["todo"].update("")

        case "todos":
            selected = values.get("todos") or []
            if selected:
                line = selected[0].strip()
                parts = line.split(". ", 1)
                window["todo"].update(parts[1] if len(parts) == 2 else line)

        case "Edit":
            selected = values.get("todos") or []
            new_todo = values.get("todo", "").strip()

            if not selected:
                sg.popup("Please select an item first.", font=("Times New Roman", 20))
            elif not new_todo:
                sg.popup("Please type a new value first.", font=("Times New Roman", 20))
            else:
                todos = functions.get_todos()
                old_line = selected[0]

                if old_line in todos:
                    idx = todos.index(old_line)
                    number_part = old_line.strip().split(". ", 1)[0]
                    todos[idx] = f"{number_part}. {new_todo}\n"

                    functions.write_todos(todos)
                    refresh_list(window)
                    window["todo"].update("")

        case "del":
            selected = values.get("todos") or []
            if selected:
                todos = functions.get_todos()
                if selected[0] in todos:
                    todos.remove(selected[0])
                    functions.write_todos(todos)
                    refresh_list(window)
                    window["todo"].update("")

        case _:
            pass


window.close()