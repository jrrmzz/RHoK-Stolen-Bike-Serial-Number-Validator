#!/usr/bin/env python
import cpic 
import cgi

def myapp(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    qs = cgi.parse_qs(environ['QUERY_STRING'])
    if 'ser' not in qs: 
	return "Expected 'ser' parameter"
    serial = qs['ser'][0]
    return serial + " -> " + str(cpic.scrape(serial))

if __name__ == '__main__':
    from fcgi import WSGIServer
    WSGIServer(myapp).run()

