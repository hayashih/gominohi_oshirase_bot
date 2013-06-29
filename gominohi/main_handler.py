# -*= coding: utf-8 -*=

import os
import sys
sys.path.append('.')
import webapp2
import jinja2
import logging
import json
import cgi

from google.appengine.api import memcache, users
from google.appengine.ext import db

from datetime import datetime, timedelta, date
from calendar import *

from gominohi_data import *

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Home(webapp2.RequestHandler):
    def get(self):
        today = (datetime.utcnow() + timedelta(hours = 9 )).date()
        chk = Checker()
        message = chk.check(today)

        if message != None:
            self.response.out.write(u'%s月%s日 %s' % (today.month, today.day, message))
        else:
            self.response.out.write(u'%s月%s日 今日のゴミ捨てはありません。' % (today.month, today.day) )


