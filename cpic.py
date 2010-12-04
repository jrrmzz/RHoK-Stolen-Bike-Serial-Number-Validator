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

def format_result(template_path, replacement_token, entries):
    template = open(template_path, 'rU').read()
    
    row_template = '''
    <ul class='field'>
        <li><h3>Status:</h3> {Status}</li>
        <li><h3>Color:</h3> {Color}</li>
        <li><h3>Make</h3> {Make}</li>
        <li><h3>Serial:</h3> {Serial}</li>
        <li><h3>Model:</h3> {Model}</li>
        <li><h3>Speeds:</h3> {Speeds}</li>
    </ul>
    '''
    
    if len(entries) == 0:
        content = '<h1>This serial number has no active entries in CPIC</h1>'
    else:
        content = ''
        for entry in entries:
            content += row_template.format(**entry)
    
    page = template.replace(replacement_token, content)
    return page

if __name__ == '__main__':
    serial_number = 'LY22361081'
    entries = scrape(serial_number)
    print format_result('public/result.html', '<!-- $CONTENT -->', entries)
    
    