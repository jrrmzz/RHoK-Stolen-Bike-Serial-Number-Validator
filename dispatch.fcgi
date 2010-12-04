#!/home/bikebikebike/local/bin/python
# HACK for local install of python to work.  This is what you'd usually put as
# the first line:
#!/usr/bin/env python

import cpic 
import cgi
import simplejson
import re

def myapp(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
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

    return cpic.format_result('public/result.html', '<!-- $CONTENT -->', response['data'])

if __name__ == '__main__':
    from fcgi import WSGIServer
    WSGIServer(myapp).run()

