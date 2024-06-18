#!/usr/bin/python3

import requests
import urllib3
from bs4 import BeautifulSoup
from datetime import datetime
import re
import pandas as pd
import os

# If you cloned this repo and haven't changed the file structure,
# this file should be in the scripts/ folder of the working
# directory. The next two lines pulls you our of the scritps/ 
# folder into the working directory
#working_dir = os.getcwd()[:-7]
#os.chdir(working_dir)

# Specify the URL for Customs and Border Patrol's data
url = "http://www.cbp.gov/document/stats/nationwide-drug-seizures"

# Make the website think we're a normal person browsing, not a bot
urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' + 
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

# Get the HTML from the URL
response = requests.get(url, headers=headers)

if response.status_code == 200:
    #print(response.text)  
    print('Page downloaded sucessfully')
else:
    print(f'Request failed with status code: {response.status_code}')
    
# Parse the content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all <td> tags, which mark the table with the CSVs
table_tags = soup.find_all('td')[2]

# See when the most recent CSV was uploaded
latest_date_str = re.sub(r'\s+', '',
                         re.sub('</td>', '',
                                re.sub('<td.*>', '', str(table_tags))))

# convert is most recent upload to date type
latest_date = datetime.strptime(latest_date_str, "%m/%d/%Y").date()
#print(latest_date)

# find the row with the latest CSV and download the file
base_url = "https://www.cbp.gov"
def get_dataset():
    """This function finds the table where the CBP upload their
    latest datasets, and grabs the URL from the first row, which 
    is the most recent data. It downloads this file with the name
    'cbp_data_YYYY-mm-dd.csv"""
    link_tags = soup.find('tbody')
    link_stub = link_tags.find('a').get('href')

    full_url = base_url + link_stub
    filename = "data/cbp_data_" + str(latest_date) + ".csv"

    query_parameters = {"downloadformat": "csv"}
    data_response = requests.get(full_url, params=query_parameters)
    if data_response.status_code == 200:
        with open(filename, mode="wb") as file:
            file.write(data_response.content)
    else:
        raise ValueError(f'Request failed with status code: {data_response.status_code}')
        
        
if len(os.listdir('data/')) > 0:
    matches = [file for file in os.listdir('data/') if "cbp_data_" in file]
    date_str = ([datetime.strptime(match.replace('cbp_data_', '')
                                   .replace('.csv', ''), "%Y-%m-%d")
                 .date() for match in matches])
    current_date = max(date_str)
    
else:
    raise ValueError('Error:\nNo files in the "data/" directory')


# See the CBP data is more recent than the data we have
def compare_dates(latest_date):
    """This takes the date of the most recent dataset we've
    downloaded and compares it to the date of CBP's latest upload.
    If the uploaded data is more recent than our download, it
    downloads the newest data."""
    if current_date < latest_date:
        get_dataset()
    elif current_date == latest_date:
        print("Dataset is already up to date")
    else:
        raise ValueError("Error:\nSomething is wrong. The current dataset\nseems to be more recent than the most\nrecent data. You should investigate whether\nthe site structure has changed or a dataset\nwas removed.")
        
        
if __name__ == '__main__':
    compare_dates(latest_date)