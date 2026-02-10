from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from funtionai import load_prompt
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm= ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5
)

system_prompt = load_prompt("prompts/einstein.txt")

prompt = ChatPromptTemplate.from_messages([
    ("system",system_prompt),
    (MessagesPlaceholder(variable_name="history")),
    ("user","{input}")]
)

chain = prompt | llm | StrOutputParser()

print("Hi, I am Albert, how can I help you today? (type 'exit' to quit)")
history = []

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = chain.invoke({"input":user_input, "history":history})
    print(f"Albert: {response}")
    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content=response))

