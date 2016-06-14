#!/usr/bin/env python3

"""
Scrape U-boat data and create dataframe

Only works for WWI
WWII has a different page format

file = ./Documents/Python/uboat/uboat.py
output file = ./Documents/Python/uboat/uboat_db.xlsx
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd


BASE_URL = 'http://uboat.net/wwi/ships_hit/'


# Use BeautifulSoup to Extract Individual U-Boat data.
def get_data(ship):
    ship_url = BASE_URL + str(ship) + ".html"
    r = requests.get(ship_url)
    soup = BeautifulSoup(r.text, 'lxml')

    # Find info table within soup.
    name_table = soup.find(class_='table_subtle width550')
    info_table = soup.find(class_='info-table')
    
    try:
        row_data = [d.get_text() for d in
        info_table.find_all('tr')[1]].get_text()
    except IndexError:
        pass

    try:
        ship_name = name_table.find_all('tr')[0].find_all('td')[1].get_text()
    except IndexError:
        pass

    try:
        ship_type = name_table.find_all('tr')[1].find_all('td')[1].get_text()
    except IndexError:
        pass

    row_data[0] = ship_name
    row_data.insert(1, ship_type)

    return row_data

# print(get_data(124))


# Make database.
def make_database():
    col_labels = ['Ship Name', 'Ship Type', 'Date', 'U-Boat', 'Loss Type', 'Position', 'Location',
    'Route', 'Cargo', 'Casualties']

    rows = {}

    for id in range(1, 7751):
        rows[id] = get_data(id)

    uboat_df = pd.DataFrame.from_dict(rows, orient = 'index')
    uboat_df.columns = col_labels
    
    return uboat_df

# print(make_database())


def write_to_xl():
    df = make_database()
    writer = pd.ExcelWriter('uboat_db.xlsx', engine = 'xlsxwriter')
    df.to_excel(writer, sheet_name = 'wwi')

write_to_xl()



