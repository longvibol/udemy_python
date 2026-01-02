from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

@tool
def add_task(task: str) -> str:
    """Add a new task to the user's task list."""
    # TODO: call Todoist here
    return f"✅ Task added: {task}"

tools = [add_task]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=gemini_api_key,
    temperature=0.3,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Help the user manage tasks using tools when needed."),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

response = agent_executor.invoke({"input": "Add task: Study LangChain for 30 minutes tonight"})
print(response)
