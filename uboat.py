#!/usr/bin/env python3

"""
Scrape U-boat data and create dataframe

Iterates through www.uboat.net/wwi/ships_hit/
Each page (#.html) displays a ship
- Currently only pulls first row/incident
file = ./Documents/Python/uboat/uboat.py
output file = ./Documents/Python/uboat/uboat_db.xlsx
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd


BASE_URL = 'http://uboat.net/wwi/ships_hit/'


# Use BeautifulSoup to Extract Individual U-Boat data
def get_data(ship):
    ship_url = BASE_URL + str(ship) + ".html"
    r = requests.get(ship_url)
    soup = BeautifulSoup(r.text, 'lxml')

    
    # Pull ship name
    ship_name = soup.find("div", id="content").h1.get_text()

    # Pull ship type and tonnage from top table
    top_table = soup.find(class_='table_subtle width550')
    ship_type = top_table.find_all('tr')[1].find_all('td')[1].get_text()
    ship_grt = top_table.find_all('tr')[2].find_all('td')[1].get_text()
    ship_grt = ship_grt[:-5]

    # Pull incident info from info-table
    info_table = soup.find(class_='info-table')
    if len(info_table.find_all('tr')) >= 2:
        date = info_table.find_all('tr')[1].find_all('td')[1].get_text()
        uboat = info_table.find_all('tr')[1].find_all('td')[2].get_text()
        loss_type = info_table.find_all('tr')[1].find_all('td')[3].get_text()
        position = info_table.find_all('tr')[1].find_all('td')[4].get_text()
        location = info_table.find_all('tr')[1].find_all('td')[5].get_text()
        route = info_table.find_all('tr')[1].find_all('td')[6].get_text()
        cargo = info_table.find_all('tr')[1].find_all('td')[7].get_text()
        casualties = info_table.find_all('tr')[1].find_all('td')[8].get_text()

    else:
        date=uboat=loss_type=position=location=route=cargo=casualties=''

    # Remove \r\n from position
    position = position.strip('\r\n')

    row_data = [ship_name, ship_type, ship_grt, date, uboat, loss_type,
    position, location, route, cargo, casualties] 


    return row_data

# print(get_data(32))

"""
The program runs slowly - possible solution:
Instead of building full pandas database then writing to xlsx,
Skip dataframe and append each row_data to xlsx.
"""

# Make database
def make_database():
    col_labels = ['Ship Name', 'Ship Type', 'GRT', 'Date', 'U-Boat', 'Loss Type', 'Position', 'Location',
    'Route', 'Cargo', 'Casualties']

    rows = {}

    # Debug: log where AttibuteError is raised
    error_log = open('error_log.txt', 'w')

    # Iterate through each page, max = 7750
    for id in range(1, 7751):
        try:
            rows[id] = get_data(id)
        except Exception as e:
            error_log.write("Failure {0}: {1}".format(str(id), str(e)))
            pass
    error_log.close() 
            

    uboat_df = pd.DataFrame.from_dict(rows, orient = 'index')
    uboat_df.columns = col_labels
    
    return uboat_df

# print(make_database())


# Write pandas dataframe to xlsx file
def write_to_xl():
    df = make_database()
    writer = pd.ExcelWriter('uboat_db.xlsx', engine = 'xlsxwriter')
    df.to_excel(writer, sheet_name = 'wwi')

write_to_xl()




