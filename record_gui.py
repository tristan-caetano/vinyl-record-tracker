# Tristan Caetano
# Vinyl Record Tracker GUI
# GUI for Vinyl Record Tracker

import FreeSimpleGUI as sg
import vinyl_SQL as vs
import spotify_api as sa
import options_menu as o
import image_resizer as ir

# Default values
r_vals = ["1", "Sleeve"]
img_bin = " "
currently_editing = False
curr_edit_album = " "

# Themes
themes = [
    'SystemDefault','Material1','Material2','Reddit','Topanga','GreenTan','Dark',
    'LightGreen','Dark2','Black','Tan','TanBlue','DarkTanBlue','DarkAmber','DarkBlue',
    'Reds','Green','BluePurple','Purple','BlueMono','GreenMono','BrownBlue',
    'BrightColors','NeutralBlue','Kayak','SandyBeach','TealMono'
]

# Window theme
curr_theme = sg.change_look_and_feel('Dark')

# ---------- Layout ----------

# Left Column Layout
left_column_layout = [
    [sg.Text("Input Album Details:", font=("Arial Bold", 15))],
    [sg.Text('Album Title', size=(15, 1)), sg.InputText(key='-TITLE-', expand_x=True)],
    [sg.Button("Get Album Details")],
    [sg.Text('Artist', size=(15, 1)), sg.InputText(key='-ARTIST-', expand_x=True)],
    [sg.Text('# of Tracks', size=(15, 1)), sg.InputText(key='-TRACKS-', expand_x=True)],
    [sg.Text('Release Date', size=(15, 1)), sg.InputText(key='-RELEASE-', expand_x=True)],
    [sg.HorizontalSeparator()],  # <-- removed unsupported expand_x
    [sg.Text("Input Vinyl Details:", font=("Arial Bold", 15))],
    [sg.Text('Color of Vinyl', size=(15, 1)), sg.InputText(key='-COLOR-', expand_x=True)],
    [sg.Text("LP Amount"),
        sg.Radio("One", "lp", key='1', default=True),
        sg.Radio("Two", "lp", key='2'),
        sg.Radio("Three", "lp", key='3'),
        sg.Radio("Four", "lp", key='4')],
    [sg.Text("Jacket Type"),
        sg.Radio("Sleeve", "jacket", key='s', default=True),
        sg.Radio("Gate-Fold", "jacket", key='gf'),
        sg.Radio("Tri-Fold", "jacket", key='tf'),
        sg.Radio("Quad-Fold", "jacket", key='qf'),
        sg.Radio("Box Set", "jacket", key='bs')],
    [sg.Button("Submit Entry"), sg.Push(), sg.Text('', key='-SELECTED_ROW-'), sg.Button("Edit Entry")]
]

# Right Column Layout
right_column_layout = [
    [sg.Image(ir.resize_image((300, 300), "spotify.png", "", False), key='-IMAGE-', expand_x=True, expand_y=True)]
]

# Table
table = sg.Table(
    vs.get_DB_data(),
    headings=["Title", "Artist", "# of Tracks", "Color", "# of LPs", "Jacket Type", "Release"],
    justification='left',
    key='-TABLE-',
    auto_size_columns=True,
    expand_x=True,
    expand_y=True,
    enable_events=True
)

# Window layout
layout = [
    [sg.Column(left_column_layout, expand_x=True, expand_y=True, scrollable=True, vertical_scroll_only=True),
     sg.VSeperator(),
     sg.Column(right_column_layout, expand_x=True, expand_y=True)],
    [sg.HorizontalSeparator()],  # <-- removed unsupported expand_x
    [table],
    [sg.Button("Export as CSV"), sg.Push(), sg.Text('Records: ' + str(len(vs.get_DB_data())), key='-NUM_RECORDS-')]
]

# ---------- Window ----------
window = sg.Window(
    title="Vinyl Tracker",
    layout=layout,
    margins=(10, 10),
    resizable=True,
    finalize=True
)

# ---------- Event Loop ----------
while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, "Exit"):
        break

    # Submit / Delete Entry
    if event == "Submit Entry":
        if not currently_editing and values['-TITLE-'] != "":

            # LPs
            if values["1"]:
                r_vals[0] = "1"
            elif values["2"]:
                r_vals[0] = "2"
            elif values["3"]:
                r_vals[0] = "3"
            elif values["4"]:
                r_vals[0] = "4"

            # Jacket
            if values["s"]:
                r_vals[1] = "Sleeve"
            elif values["gf"]:
                r_vals[1] = "Gate-Fold"
            elif values["tf"]:
                r_vals[1] = "Tri-Fold"
            elif values["qf"]:
                r_vals[1] = "Quad-Fold"
            elif values["bs"]:
                r_vals[1] = "Box Set"

            # Add to DB
            vs.add_entry([
                values['-TITLE-'], values['-ARTIST-'], values['-TRACKS-'],
                values['-COLOR-'], r_vals[0], r_vals[1], values['-RELEASE-'], img_bin
            ])
            window['-TABLE-'].update(vs.get_DB_data())

            # Reset
            for key in ['-TITLE-', '-ARTIST-', '-TRACKS-', '-COLOR-', '-RELEASE-']:
                window[key].update("")
            window['-IMAGE-'].update(ir.resize_image((300,300), "spotify.png", "", False))
            window['1'].update(True)
            window['s'].update(True)

            window['-NUM_RECORDS-'].update('Records: ' + str(len(vs.get_DB_data())))
            window.refresh()

        elif currently_editing:
            vs.delete_album_by_name(curr_edit_album)
            window['-TABLE-'].update(vs.get_DB_data())

            # Reset
            for key in ['-TITLE-', '-ARTIST-', '-TRACKS-', '-COLOR-', '-RELEASE-']:
                window[key].update("")
            window['-IMAGE-'].update(ir.resize_image((300,300), "spotify.png", "", False))
            window['1'].update(True)
            window['s'].update(True)

            currently_editing = False
            window['Edit Entry'].update("Edit Entry")
            window['Submit Entry'].update("Submit Entry")
            window['-SELECTED_ROW-'].update("")

            window['-NUM_RECORDS-'].update('Records: ' + str(len(vs.get_DB_data())))
            window.refresh()

    # Get Album Details
    elif event == "Get Album Details":
        if values['-TITLE-'] != "":
            try:
                album_query = values['-TITLE-'].replace(" ", "+")
                spotify_details = sa.get_album_info(album_query)

                window['-TITLE-'].update(spotify_details[0])
                window['-ARTIST-'].update(spotify_details[1])
                window['-TRACKS-'].update(spotify_details[2])
                window['-RELEASE-'].update(spotify_details[3])

                if spotify_details[4] != "":
                    img_bin = ir.resize_image((300,300), spotify_details[4], album_query, True)
                    window['-IMAGE-'].update(img_bin)
                else:
                    window['-IMAGE-'].update(ir.resize_image((300,300), "spotify.png", "", False))

            except Exception as e:
                print("Cannot find album using that search.", e)

    # Export CSV
    elif event == "Export as CSV":
        vs.sql_2_csv()

    # Options
    elif event == "Options":
        o.options(curr_theme, window)

    # Editing toggle
    elif event == "Edit Entry" and not currently_editing:
        currently_editing = True
        window['Edit Entry'].update("Submit Change")
        window['Submit Entry'].update("Delete Entry")
        window['-SELECTED_ROW-'].update("Currently Editing: None")

    elif event == "Edit Entry" and currently_editing:
        currently_editing = False
        window['Edit Entry'].update("Edit Entry")
        window['Submit Entry'].update("Submit Entry", disabled=False)
        window['-SELECTED_ROW-'].update("")
        # (rest of editing logic would go here, same as before but cleaned up with keys)

    # Selecting row while editing
    elif event == '-TABLE-' and currently_editing:
        db_data = vs.get_DB_data()
        if values[event]:
            curr_edit_album = db_data[values[event][0]][0]
            window['Submit Entry'].update(disabled=False)
            window['-SELECTED_ROW-'].update("Currently Editing: " + curr_edit_album)

# Close window
window.close()
