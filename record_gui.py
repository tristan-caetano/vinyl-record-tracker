# Tristan Caetano
# Vinyl Record Tracker GUI
# GUI for Vinyl Record Tracker

# Importing
import PySimpleGUI as sg
import vinyl_SQL as vs
import spotify_api as sa
import options_menu as o
import image_resizer as ir

# Default for radio button values
r_vals = ["1", "Sleeve"]

# Default image is blank
img_bin = " "

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

# Window theme
curr_theme = sg.change_look_and_feel('Dark')

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

# Input text
title_text = [sg.Text('Title', size =(15, 1)), sg.InputText()]
artist_text = [sg.Text('Artist', size =(15, 1)), sg.InputText()]
tracks_text = [sg.Text('# of Tracks', size =(15, 1)), sg.InputText()]
release_text = [sg.Text('Release Date', size =(15, 1)), sg.InputText()]
headings = ["Title", "Artist", "# of Tracks", "Color", "# of LPs", "Jacket Type", "Release"]
table = [sg.Table(vs.get_DB_data(), headings=headings, justification='left', key='-TABLE-', auto_size_columns=False, size=(10,10), max_col_width=40, def_col_width=13)]
image = [sg.Image(ir.resize_image((300,300), "spotify.png", "", False))]
#[sg.Image(ir.resize_image("tpab.png", (300,300)))]

left_column = [[sg.Text("Input record details.")], 
    title_text,
    [sg.Button("Get Album Details")],
    artist_text,
    tracks_text,
    [sg.Text('Color', size =(15, 1)), sg.InputText()],
    lp_radio,
    jacket_radio,
    release_text,
    [sg.Button("Submit Entry")]]

right_column = [[sg.Button("Options")], image]

# Window layout
layout=[[sg.Column(left_column),
    sg.VSeperator(),
    sg.Column(right_column)],
    [sg.HorizontalSeparator()],
    table,
    [sg.Button("Export as CSV")]
    ]

# Instantiating the window
window = sg.Window(title="Vinyl Tracker", layout=layout, margins=(10,10))

# Loop for button events
while True:

    # Getting button values
    event, values = window.read()

    # Submitting to CSV/SQL
    if event == "Submit Entry":

        # If statement for LPs
        if values["1"] == True: r_vals[0] = "1"
        elif values["2"] == True: r_vals[0] = "2"
        elif values["3"] == True: r_vals[0] = "3"
        elif values["4"] == True: r_vals[0] = "4"

        # If statement for jacket type
        if values["s"] == True: r_vals[1] = "Sleeve"
        elif values["gf"] == True: r_vals[1] = "Gate-Fold"
        elif values["tf"] == True: r_vals[1] = "Tri-Fold"
        elif values["qf"] == True: r_vals[1] = "Quad-Fold"

        # Sending values to be saved
        #vi.save_2_csv([values[0], values[1], values[2], values[3], r_vals[0], r_vals[1], values[4]])
        vs.add_entry([values[0], values[1], values[2], values[3], r_vals[0], r_vals[1], values[4], img_bin])

        table[0].update(vs.get_DB_data())
        window.refresh()

    # Getting album details from Spotify API
    elif event == "Get Album Details":
        album_query = values[0].replace(" ", "+")
        spotify_details = sa.get_album_info(album_query)
        values[0] = spotify_details[0]
        values[1] = spotify_details[1]
        values[2] = spotify_details[2]
        values[4] = spotify_details[3]
        title_text[1].update(values[0])
        artist_text[1].update(values[1])
        tracks_text[1].update(values[2])
        release_text[1].update(values[4])
        img_bin = ir.resize_image((300,300), spotify_details[4], album_query, True)
        image[0].update(img_bin)
        window.refresh()
    
    # Exporting DB table as CSV
    elif event == "Export as CSV":
        vs.sql_2_csv()

    # Opening options menu
    elif event == "Options":
        o.options(curr_theme, window)

    # If window is Xed out the window will close
    elif event == sg.WIN_CLOSED:
        break

# Closing window when the program ends
window.close()