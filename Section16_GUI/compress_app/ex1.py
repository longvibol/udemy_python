import FreeSimpleGUI as sg

label_feel = sg.Text("Enter Feel")
input_feel = sg.Input()

label_inches = sg.Text("Enter inches")
input_inches = sg.Input()

button_convert = sg.Button("Convert")

layout = [[label_feel,input_feel],[label_inches,input_inches],button_convert]

window = sg.Window("Convertor", layout=[layout])

window.read()
window.close()