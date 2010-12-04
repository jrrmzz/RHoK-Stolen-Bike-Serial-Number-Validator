import urllib

from pyscraper import PyScraper

scraper = PyScraper()
scraper.get('http://www.cpic-cipc.ca/English/searchForm.cfm')

serial_number = 'LY22361081'
url = 'http://www.cpic-cipc.ca/English/searchFormResults.cfm'
raw_params = {
    'ser': serial_number,
    'sType': 'Bicycles',
    'Submit': 'Begin Search',
}

params = urllib.urlencode(raw_params)
data = scraper.post(url, params)
print data