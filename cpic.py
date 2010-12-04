import urllib
import re

from BeautifulSoup import BeautifulSoup
from pyscraper import PyScraper

def scrape(serial_number):
    scraper = PyScraper()
    scraper.get('http://www.cpic-cipc.ca/English/searchForm.cfm')
    
    url = 'http://www.cpic-cipc.ca/English/searchFormResults.cfm'
    raw_params = {
        'ser': serial_number,
        'sType': 'Bicycles',
        'Submit': 'Begin Search',
    }
    
    params = urllib.urlencode(raw_params)
    data = scraper.post(url, params)

    soup = BeautifulSoup(data)
    entries = []
    for row in soup.findAll(lambda tag: tag.name == 'tr', valign='top'):
        items = []
        for cell in row.findAll(lambda tag: tag.name == 'td', {'class': 'style12'}, height=None):
            items.append(cell.text)
        entry = {
            'Status': items[0],
            'Serial': items[1],
            'Make': items[2],
            'Model': items[3],
            'Color': items[4],
            'Speeds': items[5],
        }
        entries.append(entry)
    return entries

if __name__ == '__main__':
    serial_number = 'LY22361081'
    for entry in scrape(serial_number):
        print entry
