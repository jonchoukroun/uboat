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
import csv


BASE_URL = 'http://uboat.net/wwi/ships_hit/'


# Use BeautifulSoup to Extract Individual U-Boat data
def get_data(ship):
    ship_url = BASE_URL + str(ship) + ".html"
    r = requests.get(ship_url)
    soup = BeautifulSoup(r.text, 'lxml')
    
    # Container to house ship data
    row_data = []

    # Pull ship name
    ship_name = soup.find("div", id="content").h1.get_text()

    # Pull ship type and tonnage from top table
    top_table = soup.find(class_='table_subtle width550')
    ship_type = top_table.find_all('tr')[1].find_all('td')[1].get_text()
    ship_grt = top_table.find_all('tr')[2].find_all('td')[1].get_text()
    ship_grt = ship_grt[:-5]

    # Use while loop to iterate through all valid rows
    info_table = soup.find(class_='info-table')
    row_count = len(info_table.find_all('tr'))

    for r in range(row_count):
        if info_table.find_all('tr')[r].find_all('td')[0].get_text():
            date = info_table.find_all('tr')[r].find_all('td')[1].get_text()
            uboat = info_table.find_all('tr')[r].find_all('td')[2].get_text()
            loss_type = info_table.find_all('tr')[r].find_all('td')[3].get_text()
            position = info_table.find_all('tr')[r].find_all('td')[4].get_text()
            location = info_table.find_all('tr')[r].find_all('td')[5].get_text()
            route = info_table.find_all('tr')[r].find_all('td')[6].get_text()
            cargo = info_table.find_all('tr')[r].find_all('td')[7].get_text()
            casualties = info_table.find_all('tr')[r].find_all('td')[8].get_text()
            row_data.append([date, uboat, loss_type, position.strip('\r\n'), location, route, cargo, casualties])
        else:
            pass
    
    # Append ship info from top table to beginning of each row
    for r in row_data:
        r.insert(0, ship_grt)
        r.insert(0, ship_type)
        r.insert(0, ship_name)

    return row_data

# get_data(3)


# Pull each page as list of rows and write to csv individually
def write_database():
    col_labels = ['Ship Name', 'Ship Type', 'GRT', 'Date', 'U-Boat', 'Loss Type', 'Position', 'Location',
    'Route', 'Cargo', 'Casualties']

    # Debug: log where AttibuteError is raised
    error_log = open('error_log.txt', 'w')

    # csv destination file for data
    with open('uboat_db.csv', 'w') as csvfile:
        add_row = csv.writer(csvfile)
        add_row.writerow(col_labels)
        # Iterate through each page, max=7750, most rows=4725, empty table=3
        for id in range(1, 7751):
            try:
               add_row.writerows(get_data(id))
            except Exception as e:
                error_log.write("Failure {0}: {1}".format(str(id), str(e)))
                pass

    error_log.close() 
            
write_database()



