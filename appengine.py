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

# appengine.py is designed to run in Google App Engine.  See dispatch.wsgi for 
# the original version.

import sys, os
sys.path.append(os.path.dirname(__file__))

import webapp2
import cpic 
import re
import logging
import json

from google.appengine.ext import ndb

class SerialSearch(ndb.Model):
    serial = ndb.StringProperty()
    num_results = ndb.IntegerProperty()
    response = ndb.StringProperty()    
    date = ndb.DateTimeProperty(auto_now_add=True)

class DispatchRequest(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        response = {}
        try:
            serial = self.request.get('serial')
            serial = re.sub('[^A-Za-z0-9]','',serial)   # remove non word characters
            serial = serial[:30].upper()                # cap length of serial number

            response['data'] = cpic.scrape(serial)
            response['status'] = 'success'
        except:
            response['data'] = []
            response['status'] = 'fail'

        logging.info('dispatch.cgi: Search for "%s" returned %i results.', serial, len(response['data']))
        serial_search = SerialSearch(
            serial = serial,
            num_results = len(response['data']),
            response = json.dumps(response['data'])
        )
        serial_search.put()

        self.response.write(str(cpic.format_result(
            os.path.dirname(__file__)+'/result.html.template',
            '<!-- $CONTENT -->',
            response['data'])
        ))

application = webapp2.WSGIApplication([
    ('/dispatch', DispatchRequest),
], debug=True)
