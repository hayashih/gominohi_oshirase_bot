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
import random

from google.appengine.api import memcache, users
from google.appengine.ext import db

from datetime import datetime, timedelta, date
from calendar import *

from gominohi_data import *
from tw_key import *

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Yachin(webapp2.RequestHandler):
    def get(self):
        today = (datetime.utcnow() + timedelta(hours = 9 )).date()

        messege = ""
        if today.day == 26:
            messege = u'今日は家賃の振込日です。'
        elif today.day == 1:
            messege = u'もう家賃払った？'

        # tweet pay yachin
        self.response.out.write( messege  )

class ShutTheFuckUp(webapp2.RequestHandler):
    def get_face(self):

        face_list = [
        u'(^_^)',
        u'(^_^;',
        u'(-o-)',
        u'(. .)',
        ];
        rand = random.randint(0, len(face_list)-1)
        return face_list[rand]

    def get(self):

        messege_list = [ 
        u'SHUT THE FUCK UP AND WRITE SOME CODE.',
        u'コード書いた?',
        u'原稿書いた?',
        u'作曲できた？',
        u'企画書できた？',
        u'カタンやろう。',
        u'人狼やろう。',
        u'桃鉄やろう。',
        ]

        rand = random.randint(0, len(messege_list)-1)

        # tweet pay yachin
        self.response.out.write(  messege_list[rand] + self.get_face() )


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
            post_message = u'%s月%s日 今日のゴミ捨てはありません。' % (today.month, today.day)  

        # retry
        for i in range(5):
            try:
                api.update_status( post_message )
                self.response.out.write( post_message )
                break
            except:
                pass
             

