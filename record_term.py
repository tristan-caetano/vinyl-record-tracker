# Tristan Caetano
# Vinyl Record Tracker Terminal Interface
# Terminal Interface for Vinyl Record Tracker

# Importing
import vinyl_SQL as vs
import spotify_api as sa
import image_resizer as ir

# Main menu for terminal interface
def main_menu():

    # While loop for main menu
    while(True):
        print("########## VINYL RECORD TRACKER MAIN MENU ##########\n")
        print("1). Add a new entry.\n")
        print("2). Remove an entry.\n")
        print("3). Search album by name.\n")
        print("4). View Database.\n")
        print("5). Export to CSV.\n")
        print("6). Quit.\n")
        print("####################################################\n")

        # User input for menu selection
        user_in = input("What would you like to do?\n")

        # Switch case for menu selection
        match user_in:

            # Adding vinyl to menu
            case "1":
                add_entry_term()

            case "2":
                remove_entry_term()

            case "3":
                search_db_by_name()

            case "4":
                print_database_to_term()

            case "5":
                vs.sql_2_csv()

            # Quitting the program
            case "6":
                return

            case _:
                print("Please choose a valid option.\n")

# Adding entry to DB from terminal
def add_entry_term():

    # Boolean for sleeve check loop
    sleeve_check = True
        
    # Loop for adding album to db    
    while(True):
        user_in = input("Type in the name of the album you would like to add.\nLeave blank to quit.\n")

        # Making sure the user doesn't search for nothing
        if user_in == "":
            return

        # Try except block in case an error is thrown
        try:
            # Replacing spaces with "+" to work in the query URL
            album_query = user_in.replace(" ", "+")

            # Getting data from spotify for album name
            spotify_details = sa.get_album_info(album_query)

            # Printing recieved data to user can verify
            print("\nAlbum Title: ", spotify_details[0],
                "\nArtist Name: " ,spotify_details[1],
                "\n# of Tracks: " ,spotify_details[2],
                "\nRelease Date: ", spotify_details[3])

        except:
            print("\nCannot find album using that search.\n")

        user_in = input("\nIs this album correct?\n(Y) or (y) for yes, any other character for no.\n")

        # If the user verified the album grabbed was correct, proceed
        if(user_in == "y" or user_in == "Y"):

            # Getting number of vinyl discs
            num_of_discs = input("\nHow many records (discs) are there?\n")

            # Getting color of vinyl discs
            color_of_discs = input("\nWhat color are the discs?\n")

            # Loop for jacket selection
            while(sleeve_check):
                print("\nChoose one of the following for the sleeve type:\n1). Sleeve\n2). Gate-Fold\n3). Tri-Fold\n4). Quad-Fold\n5). Box Set\n")
                sleeve_choice = input()

                match sleeve_choice:
                    case "1":
                        sleeve_choice = "Sleeve"
                        sleeve_check = False

                    case "2":
                        sleeve_choice = "Gate-Fold"
                        sleeve_check = False

                    case "3":
                        sleeve_choice = "Tri-Fold"
                        sleeve_check = False
                    
                    case "4":
                        sleeve_choice = "Quad-Fold"
                        sleeve_check = False
                    
                    case "5":
                        sleeve_choice = "Box Set"
                        sleeve_check = False

                    case _:
                        print("\nPlease choose a valid option (1 - 5).\n")

            # Printing data for final user verification
            print("\nAlbum Title: ", spotify_details[0],
                "\nArtist Name: " ,spotify_details[1],
                "\n# of Tracks: " ,spotify_details[2],
                "\nRelease Date: ", spotify_details[3],
                "\n# of Discs: ", num_of_discs,
                "\nColor of Discs: ", color_of_discs,
                "\nSleeve Type: ", sleeve_choice)
            
            final_check = input("\nIs this correct?\n(Y) or (y) for yes, any other character for no.\n")

            # Image url is converted to blob to be stored in db
            img_blob = ir.resize_image((300,300), spotify_details[4], album_query, True)
            
            if(user_in == "y" or user_in == "Y"):

                # Adding new entry to db
                vs.add_entry([spotify_details[0], spotify_details[1], spotify_details[2], color_of_discs, num_of_discs, sleeve_choice, spotify_details[3], img_blob])

# Function for removing album from db
def remove_entry_term():

    # Loop for removing album from db    
    while(True):
        user_in = input("Type in the name of the album you would like to remove.\nLeave blank to quit.\n")

        # If the input is blank, return to main menu
        if user_in == "":
            return

        # Making sure the user doesn't search for nothing
        if user_in != "":

            # Try except block in case an error is thrown
            try:
                # Replacing spaces with "+" to work in the query URL
                album_query = user_in.replace(" ", "+")

                # Getting data from spotify for album name
                spotify_details = sa.get_album_info(album_query)

                # Printing recieved data to user can verify
                print("\nAlbum Title: ", spotify_details[0],
                    "\nArtist Name: " ,spotify_details[1],
                    "\n# of Tracks: " ,spotify_details[2],
                    "\nRelease Date: ", spotify_details[3])

            except:
                print("\nCannot find album using that search.\n")

            # Making sure the album requested exists in the database
            results = vs.get_album_by_name(spotify_details[0])

            # If the album exists in the database, remove it
            if results is not None:
                user_in = input("\nIs this album correct?\n(Y) or (y) for yes, any other character for no.\n")
                
                # If the user verified the album grabbed was correct, proceed
                if(user_in == "y" or user_in == "Y"):
                    vs.delete_album_by_name(spotify_details[0])
                    print(spotify_details[0], " has been removed from your database!")
            else: 
                print("\nThis album is not in your database.\n")

# Search database for an album
def search_db_by_name():

    # Loop for removing album from db    
    while(True):
        user_in = input("Type in the name of the album you would like to search for.\nLeave blank to quit.\n")

        # If the input is blank, return to main menu
        if user_in == "":
            return
        else:

            # Try except block in case an error is thrown
            try:
                # Replacing spaces with "+" to work in the query URL
                album_query = user_in.replace(" ", "+")

                # Getting data from spotify for album name
                spotify_details = sa.get_album_info(album_query)

            except:
                print("\nCannot find album using that search.\n")

            # Making sure the album requested exists in the database
            results = vs.get_album_by_name(spotify_details[0])

            # If the album exists in the database, print it
            if results is not None:

                # Printing data for final user verification
                print("\nAlbum Title: ", results[0],
                    "\nArtist Name: " ,results[1],
                    "\n# of Tracks: " ,results[2],
                    "\nRelease Date: ", results[3],
                    "\n# of Discs: ", results[4],
                    "\nColor of Discs: ", results[5],
                    "\nSleeve Type: ", results[6],
                    "\n")
            else:
                print("\nCan't find searched album in database.\n")
                

# Print database to terminal
def print_database_to_term():
    
    # Getting DB and how many
    results = vs.get_DB_data()
    counter = 1

    # For loop that goes through every album
    for album in results:

        # Printing data for final user verification
        print("\n",
            str(counter) + ").",
            "\nAlbum Title: ", album[0],
            "\nArtist Name: " ,album[1],
            "\n# of Tracks: " ,album[2],
            "\nRelease Date: ", album[3],
            "\n# of Discs: ", album[4],
            "\nColor of Discs: ", album[5],
            "\nSleeve Type: ", album[6],
            "\n")
        counter += 1
    
    input("Press enter to return to the main menu.\n")
    return

main_menu()