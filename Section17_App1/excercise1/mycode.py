import FreeSimpleGUI as sg
from convert_feet_inches import feet_inches_to_meters

feet_label = sg.Text("Enter feet:")
enter_feet = sg.InputText(key="feet", size=(25,1))

inches_label = sg.Text("Enter inches:")
enter_inches = sg.InputText(key="inches", size=(25,1))

convert_button = sg.Button("Convert")

output = sg.Text(key="output")

layout = [
    [feet_label, enter_feet],
    [inches_label, enter_inches],
    [convert_button, output]
]

window = sg.Window("Convertor", layout, finalize=True)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:   # check first
        break

    if event == "Convert":
        feet_value = values["feet"]
        inches_value = values["inches"]
        result = feet_inches_to_meters(feet_value, inches_value)
        window["output"].update(value=f"{result} m", text_color="white")

window.close()