import FreeSimpleGUI as sg
from convert_feet_inches import feet_inches_to_meters

# ------------------ Themes / Palettes ------------------
PALETTES = {
    "Dark": {
        "BG": "#0f172a",
        "CARD": "#111c3a",
        "ACCENT": "#22c55e",
        "TEXT": "#e5e7eb",
        "MUTED": "#94a3b8",
        "INPUT_BG": "#0b1226",
        "BTN_BG": "#1f2a44",
        "WARN": "#fbbf24",
        "ERR": "#fb7185",
    },
    "Light": {
        "BG": "#f5f7fb",
        "CARD": "#ffffff",
        "ACCENT": "#0ea5e9",
        "TEXT": "#0f172a",
        "MUTED": "#475569",
        "INPUT_BG": "#eef2ff",
        "BTN_BG": "#e2e8f0",
        "WARN": "#b45309",
        "ERR": "#be123c",
    },
}

def apply_options(mode: str):
    p = PALETTES[mode]
    sg.set_options(
        font=("Helvetica", 12),
        text_color=p["TEXT"],
        background_color=p["BG"],
        input_elements_background_color=p["INPUT_BG"],
        input_text_color=p["TEXT"],
        button_color=(p["TEXT"], p["BTN_BG"]),
        element_padding=(6, 6),
    )
    # set a base theme too (mostly affects defaults)
    sg.theme("DarkTeal10" if mode == "Dark" else "LightGrey1")
    return p

def build_window(mode: str):
    p = apply_options(mode)

    title = sg.Text(
        "Feet/Inches → Meters Converter",
        font=("Helvetica", 18, "bold"),
        justification="center",
        expand_x=True,
        text_color=p["TEXT"],
        pad=(0, 6),
        background_color=p["CARD"],
    )

    subtitle = sg.Text(
        "Enter a height below and convert.",
        font=("Helvetica", 11),
        justification="center",
        expand_x=True,
        text_color=p["MUTED"],
        pad=(0, 10),
        background_color=p["CARD"],
    )

    # Toggle row
    toggle_row = [
        sg.Text("Appearance:", text_color=p["MUTED"], background_color=p["CARD"]),
        sg.Combo(
            ["Light", "Dark"],
            default_value=mode,
            key="mode",
            readonly=True,
            size=(10, 1),
            enable_events=True,
        ),
        sg.Push(),
    ]

    feet_row = [
        sg.Text("Feet", size=(10, 1), text_color=p["MUTED"], background_color=p["CARD"]),
        sg.Input(key="feet", size=(12, 1), justification="right", tooltip="Example: 5"),
    ]

    inches_row = [
        sg.Text("Inches", size=(10, 1), text_color=p["MUTED"], background_color=p["CARD"]),
        sg.Input(key="inches", size=(12, 1), justification="right", tooltip="Example: 11"),
    ]

    buttons_row = [
        sg.Button("Convert", bind_return_key=True, size=(10, 1)),
        sg.Button("Clear", size=(10, 1)),
        sg.Button("Exit", size=(10, 1)),
    ]

    result_frame = sg.Frame(
        "Result",
        [[sg.Text("—", key="output", font=("Helvetica", 16, "bold"),
                  size=(22, 1), justification="center",
                  text_color=p["ACCENT"], background_color=p["CARD"])]],
        expand_x=True,
        background_color=p["CARD"],
        title_color=p["MUTED"],
        relief=sg.RELIEF_FLAT,
    )

    card = sg.Frame(
        "",
        [
            [title],
            [subtitle],
            [sg.Column([toggle_row], expand_x=True, background_color=p["CARD"])],
            [sg.HorizontalSeparator(pad=(0, 10))],
            [sg.Column([feet_row, inches_row], element_justification="left",
                       pad=(0, 8), background_color=p["CARD"])],
            [sg.Push(), *buttons_row, sg.Push()],
            [sg.HorizontalSeparator(pad=(0, 10))],
            [result_frame],
        ],
        background_color=p["CARD"],
        border_width=0,
        pad=(10, 10),
    )

    layout = [[sg.Push(), card, sg.Push()]]

    window = sg.Window(
        "Converter",
        layout,
        background_color=p["BG"],
        margins=(20, 20),
        resizable=False,
        finalize=True,
    )

    # focus first input
    window["feet"].set_focus()
    return window

def parse_number(text: str):
    if text is None:
        return None
    text = text.strip()
    if text == "":
        return None
    try:
        return float(text)
    except ValueError:
        return None

# ------------------ App Loop (rebuild window on theme change) ------------------
mode = "Dark"
window = build_window(mode)

# keep inputs/result when switching modes
state = {"feet": "", "inches": "", "output": "—"}

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, "Exit"):
        break

    # Handle theme switch
    if event == "mode":
        new_mode = values["mode"]
        if new_mode != mode:
            # save current state
            state["feet"] = values.get("feet", "")
            state["inches"] = values.get("inches", "")
            state["output"] = window["output"].get()

            mode = new_mode
            window.close()
            window = build_window(mode)

            # restore state
            window["feet"].update(state["feet"])
            window["inches"].update(state["inches"])
            window["output"].update(state["output"])
        continue

    if event == "Clear":
        window["feet"].update("")
        window["inches"].update("")
        window["output"].update("—", text_color=PALETTES[mode]["ACCENT"])
        window["feet"].set_focus()
        continue

    if event == "Convert":
        p = PALETTES[mode]

        feet_val = parse_number(values.get("feet", ""))
        inches_val = parse_number(values.get("inches", ""))

        if feet_val is None and inches_val is None:
            window["output"].update("Enter feet/inches", text_color=p["WARN"])
            continue

        feet_val = 0.0 if feet_val is None else feet_val
        inches_val = 0.0 if inches_val is None else inches_val

        if feet_val < 0 or inches_val < 0:
            window["output"].update("No negatives please", text_color=p["ERR"])
            continue

        # Normalize inches into feet
        extra_feet = int(inches_val // 12)
        inches_val = inches_val % 12
        feet_val += extra_feet

        try:
            result = feet_inches_to_meters(feet_val, inches_val)
            window["output"].update(f"{result:.3f} m", text_color=p["ACCENT"])
        except Exception:
            window["output"].update("Conversion error", text_color=p["ERR"])

window.close()
