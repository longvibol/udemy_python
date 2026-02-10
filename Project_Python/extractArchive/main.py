import FreeSimpleGUI as sg
from zip_extractor import extract_archive
import os
import sys
import subprocess

# ---------- Helper ----------
def open_folder(path: str):
    """Open a folder in the OS file explorer (Windows/macOS/Linux)."""
    if not path:
        return
    if sys.platform.startswith("win"):
        os.startfile(path)  # Windows
    elif sys.platform == "darwin":
        subprocess.run(["open", path])
    else:
        subprocess.run(["xdg-open", path])

# ---------- Theme / Look ----------
sg.theme("TealMono")

TITLE_FONT = ("Segoe UI", 18, "bold")
LABEL_FONT = ("Segoe UI", 12)
INPUT_FONT = ("Segoe UI", 12)
BTN_FONT = ("Segoe UI", 12, "bold")
STATUS_FONT = ("Segoe UI", 11)

# ---------- Layout ----------
title = sg.Text("📦 Archive Extractor", font=TITLE_FONT, justification="center", expand_x=True)

label1 = sg.Text("Archive file (.zip / .rar)", font=LABEL_FONT)
input1 = sg.Input(key="archive", font=INPUT_FONT, expand_x=True)
choose_button1 = sg.FileBrowse(
    "Browse",
    file_types=(("Archives", "*.zip *.rar"), ("All Files", "*.*")),
    font=BTN_FONT
)

label2 = sg.Text("Destination folder", font=LABEL_FONT)
input2 = sg.Input(key="out", font=INPUT_FONT, expand_x=True)
choose_button2 = sg.FolderBrowse("Browse", font=BTN_FONT)

extract_button = sg.Button("Extract", key="extract", font=BTN_FONT, size=(12, 1))
open_button = sg.Button("Open Folder", key="open", font=BTN_FONT, size=(12, 1), disabled=True)
exit_button = sg.Button("Exit", key="exit", font=BTN_FONT, size=(12, 1))

status_label = sg.Text(
    "Ready ✅   (Press Esc to exit)",
    key="output",
    font=STATUS_FONT,
    text_color="white",
    expand_x=True
)

layout = [
    [title],
    [sg.HorizontalSeparator()],
    [label1],
    [input1, choose_button1],
    [sg.Text("")],
    [label2],
    [input2, choose_button2],
    [sg.Text("")],
    [extract_button, open_button, exit_button],
    [sg.HorizontalSeparator()],
    [status_label],
]

window = sg.Window(
    "Archive Extractor",
    layout,
    finalize=True,
    resizable=True,
    margins=(18, 16),
    return_keyboard_events=True  # ✅ enables Esc key event
)

# ---------- Event Loop ----------
last_output_folder = ""

while True:
    event, values = window.read()

    # ✅ close on X, Exit button, or Esc key
    if event in (sg.WIN_CLOSED, "exit", "Escape:27"):
        break

    match event:
        case "extract":
            archive_path = (values.get("archive") or "").strip()
            output_path = (values.get("out") or "").strip()

            if not archive_path:
                window["output"].update("⚠️ Please choose an archive file first.")
                continue
            if not output_path:
                window["output"].update("⚠️ Please choose a destination folder first.")
                continue

            try:
                window["output"].update("⏳ Extracting... Please wait.")
                window.refresh()

                extract_archive(archive_path, output_path)

                last_output_folder = output_path
                window["output"].update("✅ Extraction completed successfully! (Press Esc to exit)")
                window["open"].update(disabled=False)

                # Auto-open after success
                open_folder(output_path)

            except Exception as e:
                window["output"].update(f"❌ Error: {e}")
                window["open"].update(disabled=True)

        case "open":
            if last_output_folder:
                open_folder(last_output_folder)

        case _:
            pass

window.close()
