import streamlit as st
import functions

todos = functions.get_todos()

def add_todo():
    todo = st.session_state["add_todo"].strip()
    if todo:
        todos.append(todo + "\n")
        functions.write_todos(todos)
    st.session_state["add_todo"] = ""   # 👈 clear input


st.title("My Todo App")

st.subheader("This is my first app")
st.write("This app is to increase your productivity")

for index, todo in enumerate(todos):
    checkbox = st.checkbox(todo,key=todo)
    if checkbox:
        todos.pop(index)
        functions.write_todos(todos)
        del st.session_state[todo]
        st.rerun()


st.text_input(label="New todo",placeholder="Add a new todos...",
              on_change=add_todo,key="add_todo")

st.session_state