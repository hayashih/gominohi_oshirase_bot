# -*= coding: utf-8 -*=

import os
import sys
import logging

from datetime import datetime, timedelta, date
from calendar import *

class Gomi_No_Hi_Data:
    def read(self, filename):
        data = []

        fp = open(filename,'r')  
        lines = fp.readlines()  
        fp.close()  

        for line in lines:
            line = line.decode('utf-8')
            line = line.rstrip('\r\n')
            fields = line.split(',')
            dict = {'daynum': self.japanese_to_num(fields[0]), 
                 'weeknum': fields[1] == '' if [] else  [ int(f)  for f in fields[1] ],
                 'detail':fields[2] }

            data.append(dict)

        return data

    # 第曜日計算
    def __get_order_of_day(self, target_date):
        order = 1
        d = target_date.day
        while d > 7:
            d = d -7
            order = order + 1

        return order

    
    @classmethod
    def num_to_japanese(self, day_number):
        num2j_days = {0:u'月', 1:u'火', 2:u'水', 3:u'木', 4:u'金', 5:u'土', 6:u'日'}
        return num2j_days.get(day_number, u'謎')
     
    @classmethod
    def japanese_to_num(self, ja_day):
        j_days2num = {u'月':0, u'火':1, u'水':2, u'木':3, u'金':4, u'土':5, u'日':6}
        return j_days2num.get(ja_day, u'Infinity')


    def get_info(self, date):
        # 曜日
        day_of_today = date.weekday() 
        # 第何何曜日とか
        order_of_day = self.__get_order_of_day(date) 

        return order_of_day, day_of_today


class Checker():
    def check(self, date):
        message = None
        
        datadir = os.path.join(os.path.dirname(__file__), 'data')
        datafile = os.path.join(datadir, 'gominohi.csv')


        gominohi = Gomi_No_Hi_Data()
        data = gominohi.read(datafile)
        order_of_today, day_of_today =  gominohi.get_info(date)

        for d in data:
            if d['daynum'] == day_of_today:
                if len( d['weeknum'] ) == 0:
                    message = u'今日は %s曜日。%sごみの日です。' % (gominohi.num_to_japanese(day_of_today), d['detail'])
                else:
                    for w in d["weeknum"]:
                        if order_of_today == w:
                            message = u'今日は第%s%s曜日。%sごみの日です。' % (order_of_today,  gominohi.num_to_japanese(day_of_today), d['detail'])

        return message    

def test():
    date = datetime(2013,6,3,0,0,0)  #(datetime.utcnow() + timedelta(hours = 9 )).date()
    chk = Checker()
    print chk.check(date)

if __name__ == '__main__':
    test()
