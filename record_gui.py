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

# Default edit state is false
currently_editing = False
curr_edit_album = " "

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
        sg.Radio("Quad-Fold", "jacket", key='qf'),
        sg.Radio("Box Set", "jacket", key='bs')]

# Input text
title_text = [sg.Text('Album Title', size =(15, 1)), sg.InputText()]
artist_text = [sg.Text('Artist', size =(15, 1)), sg.InputText()]
tracks_text = [sg.Text('# of Tracks', size =(15, 1)), sg.InputText()]
release_text = [sg.Text('Release Date', size =(15, 1)), sg.InputText()]
headings = ["Title", "Artist", "# of Tracks", "Color", "# of LPs", "Jacket Type", "Release"]
table = [sg.Table(vs.get_DB_data(), headings=headings, justification='left', key='-TABLE-', 
auto_size_columns=False, size=(10,10), max_col_width=40, def_col_width=13, enable_events=True)]
image = [sg.Image(ir.resize_image((300,300), "spotify.png", "", False))]
edit_button = sg.Button("Edit Entry")
submit_button = sg.Button("Submit Entry")
selected_row = sg.Text('')
color_button = [sg.Text('Color of Vinyl', size =(15, 1)), sg.InputText()]
#[sg.Image(ir.resize_image("tpab.png", (300,300)))]

left_column = [[sg.Text("Input Album Details:", font = ("Arial Bold",15))], 
    title_text,
    [sg.Button("Get Album Details")],
    artist_text,
    tracks_text,
    release_text,
    [sg.HorizontalSeparator()],
    [sg.Text("Input Vinyl Details:", font = ("Arial Bold",15))],
    color_button,
    lp_radio,
    jacket_radio,
    [submit_button, sg.Push(), selected_row, edit_button]]

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
        if currently_editing == False:
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
            elif values["bs"] == True: r_vals[1] = "Box Set"

            # Sending values to be saved
            #vi.save_2_csv([values[0], values[1], values[2], values[3], r_vals[0], r_vals[1], values[4]])

            # List of Items to send to add_entry
            # values[0] Title
            # values[1] Artist 
            # values[2] Tracks 
            # values[5] Color
            # r_vals[0] LP
            # r_vals[1] Jacket
            # values[3] Release
            # img_bin IMG
            
            vs.add_entry([values[0], values[1], values[2], values[5], r_vals[0], r_vals[1], values[3], img_bin])
            
            table[0].update(vs.get_DB_data())
            window.refresh()

        elif currently_editing == True:
            print("here")
            vs.delete_album_by_name(curr_edit_album)
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
    
    # If the user selects a record
    elif event == "Edit Entry" and currently_editing == False:
        currently_editing = True
        edit_button.update("Submit Change")
        submit_button.update("Delete Entry")
        selected_row.update("Currently Editing: None")

    # If the user is done editing
    elif event == "Edit Entry" and currently_editing == True:
        currently_editing = False
        edit_button.update("Submit Entry")
        submit_button.update(disabled=False)
        selected_row.update("")
        print(curr_edit_album)
        if curr_edit_album != " ":
            
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
            elif values["bs"] == True: r_vals[1] = "Box Set"

            # Sending values to be saved
            #vi.save_2_csv([values[0], values[1], values[2], values[3], r_vals[0], r_vals[1], values[4]])

            # List of Items to send to add_entry
            # values[0] Title
            # values[1] Artist 
            # values[2] Tracks 
            # values[5] Color
            # r_vals[0] LP
            # r_vals[1] Jacket
            # values[3] Release
            # img_bin IMG
            
            print(values)
            vs.delete_album_by_name(curr_edit_album)
            vs.add_entry([values[0], values[1], values[2], values[5], r_vals[0], r_vals[1], values[3], img_bin])
            
            table[0].update(vs.get_DB_data())
            window.refresh()

        values[0] = ""
        values[1] = ""
        values[2] = ""
        values[4] = ""
        values[5] = ""
        title_text[1].update(values[0])
        artist_text[1].update(values[1])
        tracks_text[1].update(values[2])
        release_text[1].update(values[4])
        color_button[1].update(values[5])
        image[0].update(ir.resize_image((300,300), "spotify.png", "", False))

        # If statement for jacket type
        values["s"] = True
        values["gf"] = False
        values["tf"] = False
        values["qf"] = False
        values["bs"] = False

        # If statement for LPs
        values["1"] = True
        values["2"] = False
        values["3"] = False
        values["4"] = False

        window.Element('1').Update(value=True)
        window.Element('s').Update(value=True)

        window.refresh()


    elif event == '-TABLE-' and currently_editing == True:
        db_data = vs.get_DB_data()
        if curr_edit_album != db_data[values[event][0]][0]:
            curr_edit_album = db_data[values[event][0]][0]
            submit_button.update(disabled=False)
            selected_row.update("Currently Editing: " + curr_edit_album)
            results = vs.get_album_by_name(curr_edit_album)

            # List of Items 
            # values[0] Title
            # values[1] Artist 
            # values[2] Tracks 
            # values[5] Color
            # r_vals[0] LP
            # r_vals[1] Jacket
            # values[3] Release
            # img_bin IMG

            values[0] = results[0]
            values[1] = results[1]
            values[2] = results[2]
            values[4] = results[6]
            values[5] = results[3]
            title_text[1].update(values[0])
            artist_text[1].update(values[1])
            tracks_text[1].update(values[2])
            release_text[1].update(values[4])
            color_button[1].update(values[5])
            image[0].update(results[7])

            # If statement for jacket type
            values["s"] = False
            values["gf"] = False
            values["tf"] = False
            values["qf"] = False

            # If statement for LPs
            values["1"] = False
            values["2"] = False
            values["3"] = False
            values["4"] = False

            print(results[4])

            # If statement for LPs
            if results[4] == 1: r_vals[0] = "1"; values["1"] = True; window.Element('1').Update(value=True)
            elif results[4] == 2: r_vals[0] = "2"; values["2"] = True; window.Element('2').Update(value=True)
            elif results[4] == 3: r_vals[0] = "3"; values["3"] = True; window.Element('3').Update(value=True)
            elif results[4] == 4: r_vals[0] = "4"; values["4"] = True; window.Element('4').Update(value=True)

            # If statement for LPs
            if results[5] == "Sleeve": r_vals[1] = "Sleeve"; values["s"] = True; window.Element('s').Update(value=True)
            elif results[5] == "Gate-Fold": r_vals[1] = "Gate-Fold"; values["gf"] = True; window.Element('gf').Update(value=True)
            elif results[5] == "Tri-Fold": r_vals[1] = "Tri-Fold"; values["tf"] = True; window.Element('tf').Update(value=True)
            elif results[5] == "Quad-Fold": r_vals[1] = "Quad-Fold"; values["qf"] = True; window.Element('qf').Update(value=True)
            elif results[5] == "Box Set": r_vals[1] = "Box Set"; values["bs"] = True; window.Element('bs').Update(value=True)

            window.refresh()

        else:
            curr_edit_album = " "
            submit_button.update(disabled=True)
            selected_row.update("Currently Editing: None")

    # If window is Xed out the window will close
    elif event == sg.WIN_CLOSED:
        break

# Closing window when the program ends
window.close()