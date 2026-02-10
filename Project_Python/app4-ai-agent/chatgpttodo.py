from dotenv import load_dotenv
import os

from langchain.tools import tool
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# NEW: OpenAI chat model for LangChain
from langchain_openai import ChatOpenAI


load_dotenv()

# Put your OpenAI key in .env as OPENAI_API_KEY=...
openai_api_key = os.getenv("OPENAI_API_KEY")


@tool
def add_task(task: str) -> str:
    """Add a new task to the user's tasks list. Use this when user wants to add or create a task."""
    # TODO: Replace this with your real API call (e.g., POST to your todolist backend)
    print("Add a new task")
    print(f"Task: {task}")
    print("Task added")
    return f"✅ Added task: {task}"


tools = [add_task]

# Choose a model. Examples: "gpt-4.1-mini", "gpt-4o-mini", etc.
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.3,
    api_key=openai_api_key,  # or omit this if OPENAI_API_KEY is set in env
)

system_prompt = "You are a helpful assistant. You will help the user add tasks."

# IMPORTANT: Use {input} so the agent can receive runtime input
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

user_input = "please add the new task: go to shopping at 6pm"
response = agent_executor.invoke({"input": user_input})

print(response["output"])
