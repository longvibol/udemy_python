import gradio as gr
from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from funtionai import load_prompt  # make sure this file/module exists

# Load system prompt
EINSTEIN_SYSTEM_PROMPT = load_prompt("prompts/einstein.txt")

# Initialize LLM
llm = OllamaLLM(
    model="llama3",
    temperature=0.5
)

def clear_chat():
    return "",[]

def chat(user_input, hist):
    # Gradio can pass None on first run
    hist = hist or []

    # Build LangChain messages
    messages = [SystemMessage(content=EINSTEIN_SYSTEM_PROMPT)]

    # Convert Gradio "messages" history -> LangChain history
    for item in hist:
        role = item.get("role")
        content = item.get("content", "")

        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))

    # Add current user message
    messages.append(HumanMessage(content=user_input))

    # Invoke LLM
    response = llm.invoke(messages)

    # Ensure response is string
    response_text = response if isinstance(response, str) else str(response)

    # Return updated history in Gradio "messages" format
    hist = hist + [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": response_text},
    ]

    return "", hist

with gr.Blocks(title="ChatBot", theme=gr.themes.Soft()) as page:
    gr.Markdown(
        """
# Chat with Einstein System
Welcome to your personal chatbot system!
"""
    )

    chatbot = gr.Chatbot(
        # tuple format (default) works best in gradio 6.x
        avatar_images=[None, "./einstein.png"],
        show_label=False
    )

    msg = gr.Textbox(label="Message", placeholder="Type your question and press Enter...")

    msg.submit(chat, inputs=[msg, chatbot], outputs=[msg, chatbot])

    # clear = gr.Button("Clear Chat", variant="Secondary")
    clear = gr.Button("Clear Chat", variant="primary")
    clear.click(clear_chat, outputs=[msg, chatbot])

page.launch(share=True)
