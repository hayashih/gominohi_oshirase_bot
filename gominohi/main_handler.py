# -*= coding: utf-8 -*=

import os
import sys
sys.path.append('.')
sys.path.append('..')
import webapp2
import jinja2
import logging
import json
import cgi
import tweepy

from google.appengine.api import memcache, users
from google.appengine.ext import db

from datetime import datetime, timedelta, date
from calendar import *

from gominohi_data import *
from tw_key import *

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Home(webapp2.RequestHandler):
    def get(self):
        today = (datetime.utcnow() + timedelta(hours = 9 )).date()
        chk = Checker()
        message = chk.check(today)

        # Twitter OAuth
        o_auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
        o_auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(o_auth)

        post_message = '';
        if message != None:
            post_message = u'%s月%s日 %s' % (today.month, today.day, message)
        else:
            psot_message = u'%s月%s日 今日のゴミ捨てはありません。' % (today.month, today.day)  

        # retry
        for i in range(5):
            try:
                api.update_status( post_message )
                self.response.out.write( post_message )
                break
            except:
                pass
             
                                        



