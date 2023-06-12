# Tristan Caetano
# Vinyl Record Tracker
# Program that keeps track of what vinyl records I own.

# Importing packages
from os.path import exists
import pandas as pd
import glob
import os
import sys

# Getting inputs for record name, artist, color, LPs, jacket type, and release year
def input_record():

    # Getting inputs for record name, artist, color, LPs, jacket type, and release year
    v_title = input("Input the record title: ")
    v_artist = input("Input the artist name: ")
    v_color = input("Input the record color: ")
    v_lp_num = input("Input the amount of LPs: ")
    v_jacket = input("Input the jacket type: ")
    v_year = input("Input the record release year: ")

    save_2_csv([v_title, v_artist, v_color, v_lp_num, v_jacket, v_year])

def save_2_csv(record_info):

    # Name of default vinyl record CSV file
    record_csv = "vinyl.csv"

    # Making sure the CSV exists
    if exists(record_csv):
        records = pd.read_csv(record_csv)

    # If it doesnt exist, ask the user if they would like to make one
    else:
        choice = input("No existing record CSV found.\nWould you like to make one? (Y/N)")

        if choice[0] == "N":
            print("Closing program.")
            quit()

        else:
            records = pd.DataFrame(columns=["Title", "Artist", "Color", "LP", "Jacket", "Year"])

    # Adding new data to list
    records.loc[len(records.index)] = record_info

    # Saving data to csv file
    records.to_csv(record_csv, index=False)

    print("Record", record_info[0], "is saved!")