# Tristan Caetano
# Vinyl Record Tracker GUI
# Option Menu GUI for Vinyl Record Tracker
# Not currently used

# Importing
import PySimpleGUI as sg

# Options menu
def options(global_theme, win):

    # Window theme
    curr_theme = sg.change_look_and_feel('Dark')

    # List of themes
    themes = ['SystemDefault',
            'Material1',
            'Material2',
            'Reddit',
            'Topanga',
            'GreenTan',
            'Dark',
            'LightGreen',
            'Dark2',
            'Black',
            'Tan',
            'TanBlue',
            'DarkTanBlue',
            'DarkAmber',
            'DarkBlue',
            'Reds',
            'Green',
            'BluePurple',
            'Purple',
            'BlueMono',
            'GreenMono',
            'BrownBlue',
            'BrightColors',
            'NeutralBlue',
            'Kayak',
            'SandyBeach',
            'TealMono']

    # Changing local theme (not global)
    layout=[[sg.Button("Change Theme")],[sg.Combo(themes, font=('Arial Bold', 14),  expand_x=True, enable_events=True,  readonly=False, key='-COMBO-')]]

    # Instantiating the window
    window = sg.Window(title="Options Menu", layout=layout, margins=(50,20))

    while True:

        # Getting button values
        event, values = window.read()

        if event == "Change Theme":
            print("Theme: " + values["-COMBO-"])
            sg.change_look_and_feel(values["-COMBO-"])
            window.refresh()
            # global_theme[0] = values["-COMBO-"]

        # If window is Xed out the window will close
        elif event == sg.WIN_CLOSED:
            break

# User sign in window
def sign_in():

    # Window theme
    curr_theme = sg.change_look_and_feel('Dark')

    # Changing local theme (not global)
    layout=[[sg.Text("Username"), sg.InputText()], [sg.Text("Password"), sg.InputText()], [sg.Button("Sign In")]]

    # Instantiating the window
    window = sg.Window(title="Options Menu", layout=layout, margins=(50,20))

    while True:

        # Getting button values
        event, values = window.read()

        if event == "Sign In":
            print("Theme: " + values["-COMBO-"])
            sg.change_look_and_feel(values["-COMBO-"])
            window.refresh()
            # global_theme[0] = values["-COMBO-"]

        # If window is Xed out the window will close
        elif event == sg.WIN_CLOSED:
            break