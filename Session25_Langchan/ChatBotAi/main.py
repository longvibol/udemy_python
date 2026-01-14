import time
import gradio as gr
from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from funtionai import load_prompt

SYSTEM_PROMPT = load_prompt("prompts/einstein.txt")

llm = OllamaLLM(model="llama3", temperature=0.5)


def normalize_history(history):
    """
    Convert whatever Gradio provides into a clean list of (user, assistant) tuples.
    Supports:
      - [(user, assistant), ...]
      - [[user, assistant], ...]
      - items with extra fields
      - [{"role":"user","content":"..."}, {"role":"assistant","content":"..."}, ...]
    """
    if not history:
        return []

    # Case A: already tuples/lists
    if isinstance(history, list) and len(history) > 0:
        first = history[0]

        # A1: list of dict messages
        if isinstance(first, dict) and "role" in first and "content" in first:
            pairs = []
            pending_user = None
            for item in history:
                role = item.get("role")
                content = item.get("content", "")
                if role == "user":
                    pending_user = content
                elif role == "assistant":
                    # pair with last user if exists
                    if pending_user is None:
                        pending_user = ""
                    pairs.append((pending_user, content))
                    pending_user = None
            # if last user has no assistant yet
            if pending_user is not None:
                pairs.append((pending_user, ""))
            return pairs

        # A2: list of tuple/list messages
        pairs = []
        for item in history:
            if isinstance(item, (list, tuple)):
                # Take only first 2 safely
                if len(item) >= 2:
                    pairs.append((str(item[0]), str(item[1])))
                elif len(item) == 1:
                    pairs.append((str(item[0]), ""))
            else:
                # unknown single item
                pairs.append((str(item), ""))
        return pairs

    # fallback
    return []


def build_messages(history_pairs, user_text):
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    for user, assistant in history_pairs:
        if user:
            messages.append(HumanMessage(content=user))
        if assistant:
            messages.append(AIMessage(content=assistant))
    messages.append(HumanMessage(content=user_text))
    return messages


def respond(message, history):
    message = (message or "").strip()
    if not message:
        return ""

    history_pairs = normalize_history(history)
    messages = build_messages(history_pairs, message)

    # Get full response (stable)
    response = llm.invoke(messages)
    text = response if isinstance(response, str) else str(response)

    # Stream-like output for better UX
    out = ""
    for ch in text:
        out += ch
        time.sleep(0.001)  # faster
        yield out


demo = gr.ChatInterface(respond)
demo.queue().launch(share=True)
