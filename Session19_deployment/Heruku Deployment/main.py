import streamlit as st
import functions

todos = functions.get_todos()

st.set_page_config(layout="wide")

def add_todo():
    todo = st.session_state["add_todo"].strip()
    if todo:
        todos.append(todo + "\n")
        functions.write_todos(todos)
    st.session_state["add_todo"] = ""   # 👈 clear input


st.title("My Todo App")

st.subheader("This is my first app")
st.write("<h1>This app is to increase your productivity</h1>",unsafe_allow_html=True)

for index, todo in enumerate(todos):
    checkbox = st.checkbox(todo,key=todo)
    if checkbox:
        todos.pop(index)
        functions.write_todos(todos)
        del st.session_state[todo]
        st.rerun()


st.text_input(label="New todo",placeholder="Add a new todos...",
              on_change=add_todo,key="add_todo")
