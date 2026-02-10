# -*- coding: utf-8 -*-
"""
Interactive ReAct agent with an Ollama LLM and a Todoist tool to add tasks.
"""

from dotenv import load_dotenv
import os

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_ollama import ChatOllama
from todoist_api_python.api import TodoistAPI

# Import your system prompt from your local module without shadowing
from course import system_prompt  # keep only what you need

# ---------- Env & clients ----------

load_dotenv()

todolist_api_key = os.getenv("TODOLIST_API_KEY")
if not todolist_api_key:
    raise RuntimeError(
        "Missing TODOLIST_API_KEY in environment. "
        "Set it in your .env or export it before running."
    )

todoist = TodoistAPI(todolist_api_key)

# ---------- Tools ----------

@tool
def add_task(task: str) -> str:
    """Add a new task to the user's Todoist list. Use this when the user asks to add a task."""
    try:
        todoist.add_task(content=task)
        return f"Success: added task '{task}'."
    except Exception as e:
        # Provide a concise, useful error message
        return f"Error adding task: {e}"

tools = [add_task]

# ---------- LLM ----------

# If your Ollama is not on localhost:11434, add base_url="http://<host>:<port>"

llm = ChatOllama(model="llama3", temperature=0.2, base_url="http://localhost:11434")


# ---------- Prompt ----------

# Use LangChain's recommended builder
react_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("history"),           # conversation memory passed in
        ("user", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

# ---------- Agent ----------

agent = create_react_agent(llm=llm, tools=tools, prompt=react_prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,   # True or a str message
    max_iterations=2,             # enough for one tool + final answer
    early_stopping_method="force" # stop cleanly when out of iterations
)

# ---------- REPL loop ----------

def main():
    print("Assistant is ready. Type Ctrl+C to exit.")
    history = []  # list[HumanMessage | AIMessage]
    try:
        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            result = agent_executor.invoke({"input": user_input, "history": history})
            output = result.get("output", "")
            print(output)
            # Maintain message history for context
            history.append(HumanMessage(content=user_input))
            history.append(AIMessage(content=output))
    except KeyboardInterrupt:
        print("\nGoodbye!")

if __name__ == "__main__":
    main()
