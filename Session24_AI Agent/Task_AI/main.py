
# -*- coding: utf-8 -*-
"""
Updated agent code:
- Removes LangChain Hub prompt (uses a fully custom ReAct-style prompt).
- Includes both tools: add_task and show_tasks.
- Adds clear error handling and concise outputs.
- Optional chat loop maintained.
- Supports passing chat history into the prompt.
- FIX: agent_scratchpad must be a string placeholder, not MessagesPlaceholder.
"""
from typing import Any

from langchain_core.messages import HumanMessage, AIMessage
from todoist_api_python.api import TodoistAPI
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os
import sys
import traceback

# ---------- Environment & API ----------
load_dotenv()

# NOTE: Prefer the standard env var name "TODOIST_API_KEY" (fallback to "TODOLIST_API_KEY")
todoist_api_key = os.getenv("TODOIST_API_KEY") or os.getenv("TODOLIST_API_KEY")
if not todoist_api_key:
    raise ValueError(
        "Missing Todoist API key. Set environment variable 'TODOIST_API_KEY' "
        "(or 'TODOLIST_API_KEY')."
    )

todoist = TodoistAPI(todoist_api_key)

# ---------- Tools ----------
@tool
def add_task(task: str) -> str:
    """Add a new task to the user's tasks list. Use this when the user wants to add a new task."""
    try:
        new_task = todoist.add_task(content=task)
        return f'Success: added task "{new_task.content}" (id: {new_task.id})'
    except Exception as e:
        return f"Error adding task: {e}"


@tool
def show_tasks() -> list[Any]:
    """Show all tasks from Todoist. Use this when the user wants to show all tasks."""
    results_pagination = todoist.get_tasks()
    tasks =[]
    for result_list in results_pagination:
        for task in result_list:
            tasks.append(task.content)
    return tasks

tools = [add_task, show_tasks]

# ---------- LLM ----------
# Ensure your Ollama server is running (`ollama serve`)
# and the model exists (`ollama pull llama3`)
llm = ChatOllama(model="llama3:latest", temperature=0.2)

prompt = ChatPromptTemplate.from_messages([
    ("system",
        (
            "You will help the user add tasks.\n"
            "You will help the user show existing tasks. If the user ask to show the tasks: for example,""show me all the tasks.\n"
            "print out the tasks to the user. Print them in a bullet list format.\n"
            "You are a helpful task assistant that uses tools when needed.\n"
            "You have access to the following tools:\n\n{tools}\n\n"
            "Guidelines:\n"
            "- Think step by step before acting.\n"
            "- Only call a tool if it's necessary for the user's request.\n"
            "- If a tool fails, explain the error clearly.\n"
            "- Keep responses concise and actionable.\n"
            "- If the user asks to add a task, call the add_task tool.\n"
            "- If the user asks to list tasks, call the show_tasks tool.\n\n"
            "You can call these tools by name: {tool_names}.\n\n"
            "Use the following format:\n"
            "Thought: reflect on what to do\n"
            "Action: the tool name (one of [{tool_names}])\n"
            "Action Input: the input for the tool\n"
            "Observation: the tool result\n"
            "... (repeat Thought/Action/Action Input/Observation as needed)\n"
            "Final Answer: your final response to the user"
        ),
    ),
    # Include prior chat messages for multi-turn context
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
    # ✅ The scratchpad must be injected as a string into the assistant role
    ("ai", "{agent_scratchpad}"),
])

# ---------- Agent ----------
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,                # show internal chain logs if True
    handle_parsing_errors=True,
    max_iterations=2,            # enough for tool + final answer
    early_stopping_method="force"
)

def print_exception(e: Exception) -> None:
    print("ERROR:", str(e), file=sys.stderr)
    traceback.print_exc()

# ---------- Quick self-test (single turn) ----------
try:
    test_output = agent_executor.invoke({"input": "Add a task: Buy milk", "history": []})
    print("\n[Self-test output]")
    print(test_output)
    print("\n[Self-test final answer]")
    print(test_output.get("output"))
except Exception as e:
    print_exception(e)

# ---------- Chat Loop ----------
history = []
while True:
    try:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        response = agent_executor.invoke({"input": user_input, "history": history})
        # Show full response for debugging
        print("\n[Agent raw response]")
        print(response)

        # Print final answer
        print("\nAssistant:", response.get("output"))

        # Maintain history
        history.append(HumanMessage(content=user_input))
        history.append(AIMessage(content=response.get("output", "")))
    except Exception as e:
        print_exception(e)
        continue
