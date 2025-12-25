import FreeSimpleGUI as sg

def km_to_miles(km):
    return km / 1.6

def miles_to_km(miles):
    return miles * 1.6

label_M = sg.Text("Miles:")
input_box_miles = sg.InputText(tooltip="Enter miles", key="miles")

label_K = sg.Text("Kilometers:")
input_box_Km = sg.InputText(tooltip="Enter kilometers", key="km")

button_miles = sg.Button("Convert-Miles", key="button_miles")
button_km = sg.Button("Convert-Km", key="button_km")

output_box_miles = sg.Text("", key="output_m")
output_box_km = sg.Text("", key="output_km")

window = sg.Window(
    'Km to Miles Converter',
    layout=[
        [label_M, input_box_miles, output_box_miles],
        [label_K, input_box_Km, output_box_km],
        [button_miles, button_km]
    ],
    font=('Helvetica', 15)
)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    # Pressing Enter in the Miles box returns "miles"
    if event == "button_miles" or event == "miles":
        try:
            miles = float(values["miles"])
            result = miles_to_km(miles)
            window["output_m"].update(f"{result:.2f} Km")
        except ValueError:
            window["output_m"].update("Invalid input")

    # Pressing Enter in the Km box returns "km"
    elif event == "button_km" or event == "km":
        try:
            km = float(values["km"])
            result = km_to_miles(km)
            window["output_km"].update(f"{result:.2f} Miles")
        except ValueError:
            window["output_km"].update("Invalid input")

window.close()