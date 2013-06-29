# coding: UTF-8
# vim: fileencoding=utf-8 :

import os
from google.appengine.ext.webapp import template
import cgi
import webapp2

from google.appengine.api import users
from google.appengine.ext import db
from gominohi.main_handler import *

PREFIX = "/gominohi"


app = webapp2.WSGIApplication(
  [
      (PREFIX + '/', Home),
  ],
  debug=True)


