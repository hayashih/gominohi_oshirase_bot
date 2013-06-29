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

class Checker():
    def check(self, date):
        message = None
        
        datadir = os.path.join(os.path.dirname(__file__), 'data')
        datafile = os.path.join(datadir, 'gominohi.csv')

        #(datetime.utcnow() + timedelta(hours = 9 )).date()

        gominohi = Gomi_No_Hi_Data()
        data = gominohi.read(datafile)
        order_of_today, day_of_today =  gominohi.get_info(date)
        logging.info(order_of_today)

        for d in data:
            if d.daynum == day_of_today:
                if len( d.weeknum ) == 0:
                    message = u'今日は %s 曜日。%s ごみの日です。' % (gominohi.num_to_japanese(day_of_today), d.detail)
                else:
                    for w in d.weeknum:
                        if order_of_today == w:
                            message = u'今日は第%s %s 曜日。%s ごみの日です。' % (order_of_today,  gominohi.num_to_japanese(day_of_today), d.detail)

        return message    

class Home(webapp2.RequestHandler):
    def get(self):
