import streamlit as st
import functions
from datetime import date

st.set_page_config(page_title="Todo App", page_icon="✅", layout="centered")

# -------------------- LIGHT THEME CSS (ONLY) --------------------
def inject_css():
    bg = "linear-gradient(-45deg, #f8fafc, #eef2ff, #ecfeff, #fff7ed)"
    text = "rgba(15, 23, 42, 0.95)"
    card = "rgba(255, 255, 255, 0.70)"
    border = "rgba(15, 23, 42, 0.10)"
    input_bg = "rgba(255,255,255,0.85)"
    shadow = "0 10px 30px rgba(15,23,42,0.10)"
    blob_opacity = "0.30"

    st.markdown(
        f"""
        <style>
        .block-container {{ padding-top: 2rem; }}

        [data-testid="stAppViewContainer"] {{
            background: {bg};
            background-size: 400% 400%;
            animation: gradientMove 16s ease infinite;
        }}
        @keyframes gradientMove {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        .bg-blobs {{
            position: fixed;
            inset: 0;
            overflow: hidden;
            z-index: 0;
            pointer-events: none;
        }}
        .blob {{
            position: absolute;
            width: 460px;
            height: 460px;
            filter: blur(70px);
            opacity: {blob_opacity};
            border-radius: 50%;
            animation: floaty 14s ease-in-out infinite;
            mix-blend-mode: screen;
        }}
        .blob.b1 {{ background: #60a5fa; top: -140px; left: -160px; }}
        .blob.b2 {{ background: #a78bfa; bottom: -180px; right: -160px; }}
        .blob.b3 {{ background: #34d399; top: 35%; left: 55%; width: 560px; height: 560px; }}

        @keyframes floaty {{
            0% {{ transform: translate(0px, 0px) scale(1); }}
            50% {{ transform: translate(70px, -50px) scale(1.10); }}
            100% {{ transform: translate(0px, 0px) scale(1); }}
        }}

        section.main {{ position: relative; z-index: 1; }}
        [data-testid="stHeader"] {{ background: transparent; }}

        h1, h2, h3, p, span, label, div {{ color: {text}; }}

        div[data-testid="stContainer"] > div {{
            background: {card};
            border: 1px solid {border};
            border-radius: 18px;
            backdrop-filter: blur(12px);
            box-shadow: {shadow};
        }}

        input, textarea {{
            background: {input_bg} !important;
            border: 1px solid {border} !important;
            border-radius: 12px !important;
        }}

        button {{
            border-radius: 12px !important;
        }}
        </style>

        <div class="bg-blobs">
          <div class="blob b1"></div>
          <div class="blob b2"></div>
          <div class="blob b3"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -------------------- STORAGE HELPERS --------------------
def normalize(lines: list[str]) -> list[str]:
    return [t.strip() for t in lines if t.strip()]

def persist(todo_list: list[str]) -> None:
    functions.write_todos([t + "\n" for t in todo_list])

SEPARATOR = " | "

def pack_todo(text: str, due: date | None) -> str:
    if due:
        return f"{text}{SEPARATOR}{due.isoformat()}"
    return text

def unpack_todo(item: str):
    if SEPARATOR in item:
        txt, due = item.split(SEPARATOR, 1)
        return txt.strip(), due.strip()
    return item, None

# -------------------- CALLBACKS --------------------
def add_todo():
    text = st.session_state["add_todo"].strip()
    if text:
        st.session_state.todos.append(pack_todo(text, st.session_state.due_date))
        persist(st.session_state.todos)
    st.session_state["add_todo"] = ""

def delete_todo(i):
    st.session_state.todos.pop(i)
    persist(st.session_state.todos)

def start_edit(i):
    st.session_state.editing = i
    txt, due = unpack_todo(st.session_state.todos[i])
    st.session_state.edit_text = txt
    st.session_state.edit_due = due

def save_edit(i):
    if st.session_state.edit_text.strip():
        st.session_state.todos[i] = pack_todo(
            st.session_state.edit_text,
            st.session_state.edit_due_picker
        )
        persist(st.session_state.todos)
    st.session_state.editing = None

def cancel_edit():
    st.session_state.editing = None

def clear_completed():
    st.session_state.todos = [
        t for i, t in enumerate(st.session_state.todos)
        if not st.session_state.done.get(i, False)
    ]
    st.session_state.done = {}
    persist(st.session_state.todos)

# -------------------- SESSION INIT --------------------
if "todos" not in st.session_state:
    st.session_state.todos = normalize(functions.get_todos())

st.session_state.setdefault("done", {})
st.session_state.setdefault("editing", None)
st.session_state.setdefault("edit_text", "")
st.session_state.setdefault("edit_due", None)
st.session_state.setdefault("due_date", date.today())

# Inject light theme
inject_css()

# -------------------- UI --------------------
st.title("✅ My Todo App")
st.caption("Clean & modern todo app with calendar support")

total = len(st.session_state.todos)
completed = sum(st.session_state.done.get(i, False) for i in range(total))
remaining = total - completed

if total > 0 and remaining == 0:
    st.balloons()

c1, c2, c3 = st.columns(3)
c1.metric("Remaining", remaining)
c2.metric("Completed", completed)
c3.metric("Total", total)

st.divider()

left, mid, right = st.columns([2, 1, 1])
with left:
    st.text_input(
        "New todo",
        placeholder="Add a new todo…",
        key="add_todo",
        on_change=add_todo,
        label_visibility="collapsed",
    )

with mid:
    st.date_input("Due date", key="due_date", label_visibility="collapsed")

with right:
    st.button(
        "🧹 Clear completed",
        use_container_width=True,
        disabled=(completed == 0),
        on_click=clear_completed,
        key="clear_completed_btn",
    )

view = st.segmented_control(
    "View",
    ["All", "Active", "Completed"],
    default="All",
    label_visibility="collapsed",
)

search = st.text_input(
    "Search",
    placeholder="Search todos…",
    label_visibility="collapsed",
    key="search_box",
)

if total == 0:
    st.info("No todos yet. Add one above 👆")
else:
    for i, raw in enumerate(st.session_state.todos):
        todo, due = unpack_todo(raw)
        is_done = st.session_state.done.get(i, False)

        if view == "Active" and is_done:
            continue
        if view == "Completed" and not is_done:
            continue
        if search and search.lower() not in todo.lower():
            continue

        with st.container(border=True):
            a, b, c = st.columns([0.08, 0.72, 0.20])

            with a:
                st.checkbox(
                    "Mark complete",
                    key=f"done_{i}",
                    value=is_done,
                    label_visibility="collapsed",
                )
                st.session_state.done[i] = st.session_state[f"done_{i}"]

            with b:
                if st.session_state.editing == i:
                    st.text_input(
                        "Edit todo",
                        key="edit_text",
                        label_visibility="collapsed",
                    )
                    st.date_input(
                        "Edit due date",
                        key="edit_due_picker",
                        value=date.fromisoformat(due) if due else date.today(),
                        label_visibility="collapsed",
                    )
                else:
                    badge = f" 📅 {due}" if due else ""
                    text = f"~~{todo}~~" if is_done else f"**{todo}**"
                    st.markdown(text + badge)

            with c:
                if st.session_state.editing == i:
                    st.button("💾", on_click=save_edit, args=(i,), key=f"save_{i}")
                    st.button("✖", on_click=cancel_edit, key=f"cancel_{i}")
                else:
                    st.button("✏️", on_click=start_edit, args=(i,), key=f"edit_{i}")
                    st.button("🗑️", on_click=delete_todo, args=(i,), key=f"del_{i}")
