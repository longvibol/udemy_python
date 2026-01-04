from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from funtionai import load_prompt

# Load system prompt
EINSTEIN_SYSTEM_PROMPT = load_prompt("prompts/pythonpromp.txt")

# Initialize LLM
llm = OllamaLLM(
    model="llama3",
    temperature=0.5
)

print("Hi, I am PythonX, how can I help you today? (type 'exit' to quit)")

# Conversation history
history = []

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    # Build messages: system prompt + history + new user input
    messages = [
        SystemMessage(content=EINSTEIN_SYSTEM_PROMPT),
        *history,
        HumanMessage(content=user_input)
    ]

    # Invoke model
    response = llm.invoke(messages)

    # Print response
    print(f"PythonEx: {response}")

    # Save conversation to history
    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content=response))
