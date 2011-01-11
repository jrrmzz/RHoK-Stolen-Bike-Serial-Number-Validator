"""Adapted from PyScraper (http://code.google.com/p/pyscraper/), a screen
scraping library.

Copyright 2008-2010 Gavi Narra

Additional contributions by:
 - Jason Montojo

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


import httplib,urllib,random,sys,re,os
from urlparse import urlparse
from os.path import join, split

class PyScraper:
        def __init__(self):
                self.cookie=""
                self.currenturl=""
                self.urlhist=[]
        
        def __str__(self):
                ret=''
                for item in self.urlhist:
                        ret=ret+item+'->'
                return ret
        
        def download(self,url,localfolder):
                bufsize = 1024
                self.urlhist.append(url)
                o=urlparse(url)
                scheme,hostname,path,q,query,position=o
                head,fname = os.path.split(path)
                if(query!=''):
                        path=path+"?"+query
                        
                conn=httplib.HTTPConnection(hostname)
                conn.request('GET', path,None,{'Cookie':self.cookie})
                resp=conn.getresponse()
                total=int(resp.getheader('content-length'))
                f = open(localfolder+"/"+fname,'wb')
                sofar = 0
                while 1:
                        data = resp.read(bufsize)
                        f.write(data)
                        sofar += len(data)
                        perc = (float(sofar)/float(total))
                        count = int(perc * 20)
                        #+ (' '*(20-count)) + " | " + str('%3d' % perc*100) + "% " + str('% 5d KB' % int(float(sofar)/float(1024))) + " / "  + str('% 5d KB' % int(float(total)/float(1024)))
                        sys.stdout.write("\r%-30s|%-20s|%3d percent" % (fname,'#'*count,perc*100))
                        
                        sys.stdout.flush()
                        #sys.stdout.write("\r" + str(sofar) + " / " + str(total))total
                        if len(data)==0:
                                break
                f.close()
                if(resp.getheader('set-cookie')!=None):
                        self.cookie=resp.getheader('set-cookie')
                conn.close()
                if(resp.status==302 or resp.status ==301):
                        base_location = resp.getheader('location')
                        parts = split(url)
                        location = join(parts[0], base_location)
                        return self.get(resp.getheader('location'))
                return data
        
        def get(self,url):
                self.urlhist.append(url)
                o=urlparse(url)
                scheme,hostname,path,q,query,position=o
                if(query!=''):
                        path=path+"?"+query
                        
                conn=httplib.HTTPConnection(hostname)
                conn.request('GET', path,None,{'Cookie':self.cookie})
                resp=conn.getresponse()
                data= resp.read()
                if(resp.getheader('set-cookie')!=None):
                        self.cookie=resp.getheader('set-cookie')
                conn.close()
                if(resp.status==302 or resp.status ==301):
                        base_location = resp.getheader('location')
                        parts = split(url)
                        location = join(parts[0], base_location)
                        return self.get(location)
                return data
        
        def post(self,url,data):
                self.urlhist.append(url)
                o=urlparse(url)
                scheme,hostname,path,q,query,position=o
                conn=httplib.HTTPConnection(hostname)
                conn.request('POST', path,data,{'Content-Type':'application/x-www-form-urlencoded','Cookie':self.cookie})
                resp=conn.getresponse()
                data= resp.read()
                if(resp.getheader('set-cookie')!=None):
                        self.cookie=resp.getheader('set-cookie')
                conn.close()
                if(resp.status==302 or resp.status ==301):
                        base_location = resp.getheader('location')
                        parts = split(url)
                        location = join(parts[0], base_location)
                        return self.post(location,data)
                return data
