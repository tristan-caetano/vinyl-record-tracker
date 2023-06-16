# Tristan Caetano
# Vinyl Record Tracker SQL
# SQL database for storing vinyl data.

# Importing packages
import sqlite3
from os.path import exists
import pandas as pd

# Initiate DB
def init_DB():

    # Name of default vinyl record CSV file
    record_sql = "vinyl.db"

    # Making sure the SQL exists
    if not exists(record_sql):
        # Connecting to DB
        con = sqlite3.connect("vinyl.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE vinyl(Title TEXT, Artist TEXT, Tracks INT, Color TEXT, LP INT, Jacket TEXT, Release TEXT, IMG MEDIUMBLOB)")

    else:
        # Connecting to DB
        con = sqlite3.connect("vinyl.db")

    # Returning DB info
    return con

# CSV file to SQL converter
def csv_2_sql():

    # Getting DB info
    con = init_DB()
    cur = con.cursor()

    # Name of default vinyl record CSV file
    record_csv = "vinyl.csv"

    # Making sure the CSV exists
    if exists(record_csv):
        records = pd.read_csv(record_csv, index_col=False)
    else:
        print("CSV file does not exist.")
        return

    # Setting
    for x in range(len(records)):
        entry = records.iloc[x].to_list()
        entry[3] = entry[3].item()
        entry[5] = entry[5].item()
        cur.execute("INSERT INTO vinyl VALUES(?, ?, ?, ?, ?, ?, ?)", entry)

    # Saving database info
    con.commit()

# Exporting SQL data to CSV
def sql_2_csv():

    # Getting database info
    db_data = get_DB_data(True)
        
    # Saving data to dataframe and exporting to CSV file
    records = pd.DataFrame(db_data, columns=["Title", "Artist", "# of Tracks", "Color", "# of LPs", "Jacket Type", "Release"])
    records.to_csv('vinyl.csv',index=False)

# Adding single entry to the DB
def add_entry(record):

    # Getting DB info
    con = init_DB()
    cur = con.cursor()

    # Sending 1 entry to the DB
    cur.execute("INSERT INTO vinyl VALUES(?, ?, ?, ?, ?, ?, ?, ?)", record)

    # Saving database info
    con.commit()

# Recieving DB info
def get_DB_data(no_img=False):

    # Getting DB info
    con = init_DB()
    cur = con.cursor()

    # If True, everything but the image is grabbed
    if no_img:
        # SQL query to get all info from DB except IMG
        result = cur.execute('''SELECT Title, Artist, Tracks, Color, LP, Jacket, Release FROM VINYL ORDER BY ARTIST,RELEASE''').fetchall()

    else:
        # SQL query to get all info from DB
        result = cur.execute('''SELECT Title, Artist, Tracks, Color, LP, Jacket, Release, IMG FROM VINYL ORDER BY ARTIST,RELEASE''').fetchall()

    # Returning DB data
    return result

# Getting single row by name of album
def get_album_by_name(title):

    # Getting DB info
    con = init_DB()
    cur = con.cursor()

    # Query to get record info for 1 specific album by name
    query = 'SELECT * FROM VINYL WHERE TITLE LIKE "'+title+'"'
    result = cur.execute(query).fetchone()

    # Returning DB data
    return result

# Getting single row by name of album
def delete_album_by_name(title):

    # Getting DB info
    con = init_DB()
    cur = con.cursor()

    # Query that deletes 1 record for a specific album by name
    query = 'DELETE FROM VINYL WHERE TITLE LIKE "'+title+'"'

    # Executing the query and saving changes
    cur.execute(query)
    con.commit()