"""CPIC Utilities

A web client for performing lookups on the CPIC bicycle serial number database.

Copyright 2010 The IsThisBikeStolen Team
- Stu Basden
- Amber Ellis
- Jason Montojo
- Jon Pipitone
- Ben Shymkiw
- John Taranu

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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
    <ul id='CPICResults'>
        <li><strong>Status:</strong> <span class="StolenStatus">%(Status)s</span></li>
        <li><strong>Color:</strong> %(Color)s</li>
        <li><strong>Make:</strong> %(Make)s</li>
        <li><strong>Serial:</strong> %(Serial)s</li>
        <li><strong>Model:</strong> %(Model)s</li>
        <li><strong>Speeds:</strong> %(Speeds)s</li>
    </ul>
    '''
    
    if len(entries) == 0:
        content = '<h2>This serial number has no active entries in CPIC</h2>'
    else:
        content = ''
        for entry in entries:
            content += row_template % entry
    
    page = template.replace(replacement_token, content)
    return page

if __name__ == '__main__':
    serial_number = 'LY22361081'
    entries = scrape(serial_number)
    print format_result('iphone/result.html', '<!-- $CONTENT -->', entries)
