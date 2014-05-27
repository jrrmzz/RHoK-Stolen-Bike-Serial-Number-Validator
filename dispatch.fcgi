#!/home/bikebikebike/local/bin/python
# HACK for local install of python to work.  This is what you'd usually put as
# the first line:
#!/usr/bin/env python

"""Web app for IsThisBikeStolen?

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

import cpic 
import cgi
import simplejson
import re
import logging

LOG_FILENAME = 'isthisbikestolen.log'
logger       = logging.getLogger('myapp')
hdlr         = logging.FileHandler(LOG_FILENAME)
formatter    = logging.Formatter('%(asctime)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


def myapp(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    qs = cgi.parse_qs(environ['QUERY_STRING'])

    response = {}
    try:
	serial = qs['serial'][0]
        serial = re.sub('[^A-Za-z0-9]','',serial)   # remove non word characters
        serial = serial[:30].upper()                # cap length of serial number

        response['data']   = cpic.scrape(serial)
    	response['status'] =  'success'
    except: 
	response['status'] = 'fail' 
	response['data']   = [] 

    logger.info('dispatch.cgi: Search for "%s" returned %i results.', serial, len(response['data']))
    return str(cpic.format_result('result.html.template', '<!-- $CONTENT -->', response['data']))

if __name__ == '__main__':
    from fcgi import WSGIServer
    WSGIServer(myapp).run()

