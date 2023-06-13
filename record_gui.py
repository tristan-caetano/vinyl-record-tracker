# Tristan Caetano
# Vinyl Record Tracker GUI
# GUI for Vinyl Record Tracker

# Importing
import PySimpleGUI as sg
import vinyl_input as vi
import vinyl_SQL as vs

# Default for radio button values
r_vals = ["1", "Sleeve"]

# Radio buttons for number of LPs
lp_radio=[sg.Text("LP Amount"),
        sg.Radio("One", "lp", key='1', default=True), 
        sg.Radio("Two", "lp", key='2'), 
        sg.Radio("Three", "lp", key='3'), 
        sg.Radio("Four", "lp", key='4')]

# Radio button for jacket type
jacket_radio=[sg.Text("Jacket Type"),
        sg.Radio("Sleeve", "jacket", key='s', default=True), 
        sg.Radio("Gate-Fold", "jacket", key='gf'), 
        sg.Radio("Tri-Fold", "jacket", key='tf'), 
        sg.Radio("Quad-Fold", "jacket", key='qf')]

# Window theme
sg.theme("DarkBlue15")

# Window layout
layout=[[sg.Text("Input record details.")], 
    [sg.Text('Title', size =(15, 1)), sg.InputText()],
    [sg.Text('Artist', size =(15, 1)), sg.InputText()],
    [sg.Text('Color', size =(15, 1)), sg.InputText()],
    lp_radio,
    jacket_radio,
    [sg.Text('Release Year', size =(15, 1)), sg.InputText()],
    [sg.Button("Submit Entry")]]

# Instantiating the window
window = sg.Window(title="Vinyl Tracker", layout=layout, margins=(50,20))

# Loop for button events
while True:

    # Getting button values
    event, values = window.read()

    # Submitting to CSV/SQL
    if event == "Submit Entry":

        # If statement for LPs
        if values["2"] == True: r_vals[0] = "2"
        elif values["3"] == True: r_vals[0] = "3"
        elif values["4"] == True: r_vals[0] = "4"

        # If statement for jacket type
        if values["gf"] == True: r_vals[1] = "Gate-Fold"
        elif values["tf"] == True: r_vals[1] = "Tri-Fold"
        elif values["qf"] == True: r_vals[1] = "Gate-Fold"

        # Sending values to be saved
        vi.save_2_csv([values[0], values[1], values[2], r_vals[0], r_vals[1], values[3]])
        vs.add_entry([values[0], values[1], values[2], r_vals[0], r_vals[1], values[3]])

    # If window is Xed out the window will close
    elif event == sg.WIN_CLOSED:
        break

# Closing window when the program ends
window.close()
