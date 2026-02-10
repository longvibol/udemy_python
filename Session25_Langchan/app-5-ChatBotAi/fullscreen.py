import time
import gradio as gr
from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from funtionai import load_prompt

SYSTEM_PROMPT = load_prompt("prompts/einstein.txt")
llm = OllamaLLM(model="llama3", temperature=0.5)

def normalize_history(history):
    pairs = []
    pending_user = None
    for item in history or []:
        if isinstance(item, dict):
            if item.get("role") == "user":
                pending_user = item.get("content", "")
            elif item.get("role") == "assistant":
                pairs.append((pending_user or "", item.get("content", "")))
                pending_user = None
        elif isinstance(item, (list, tuple)):
            if len(item) >= 2:
                pairs.append((item[0], item[1]))
    if pending_user is not None:
        pairs.append((pending_user, ""))
    return pairs

def build_messages(pairs, user_text):
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    for u, a in pairs:
        if u:
            messages.append(HumanMessage(content=u))
        if a:
            messages.append(AIMessage(content=a))
    messages.append(HumanMessage(content=user_text))
    return messages

def respond(message, history):
    message = (message or "").strip()
    if not message:
        return ""

    pairs = normalize_history(history)
    messages = build_messages(pairs, message)

    response = llm.invoke(messages)
    text = response if isinstance(response, str) else str(response)

    out = ""
    for ch in text:
        out += ch
        yield out

# 🌐 FULL SCREEN CSS (SAFE)
FULLSCREEN_CSS = """
html, body {
    height: 100%;
    margin: 0;
}

.gradio-container {
    height: 100vh !important;
    max-width: 100% !important;
}

.chatbot {
    height: calc(100vh - 130px) !important;
    overflow-y: auto !important;
}
"""

with gr.Blocks(css=FULLSCREEN_CSS) as demo:
    gr.ChatInterface(
        respond,
        title="🧠 Einstein Chat",
        description="Full-screen AI chatbot with long conversation support"
    )

demo.queue().launch(share=True)
