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
        cur.execute("CREATE TABLE vinyl(Title TEXT, Artist TEXT, Color TEXT, LP INT, Jacket TEXT, Year INT)")

    else:
        # Connecting to DB
        con = sqlite3.connect("vinyl.db")

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
        cur.execute("INSERT INTO vinyl VALUES(?, ?, ?, ?, ?, ?)", entry)

    con.commit()

# def sql_2_csv():

# Adding single entry to the DB
def add_entry(record):

    # Getting DB info
    con = init_DB()
    cur = con.cursor()

    # Sending 1 entry to the DB
    cur.execute("INSERT INTO vinyl VALUES(?, ?, ?, ?, ?, ?)", record)

    con.commit()
