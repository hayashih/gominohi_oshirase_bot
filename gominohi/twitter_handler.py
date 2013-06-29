# -*= coding: utf-8 -*=

import os
import sys
sys.path.append('..')
import webapp2
import logging
import json
import cgi

from datetime import datetime, timedelta, date

class UserInfo(db.Model):
    user_id    = db.StringProperty(required=True)
    nickname   = db.StringProperty(required=True)
    email      = db.EmailProperty(required=True)
    date       = db.DateTimeProperty(auto_now_add=True)

class Main(webapp2.RequestHandler):
    def get(self):
        pass
