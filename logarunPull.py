# -*- coding: utf-8 -*-

#Logarun Data Extraction script
import csv
from datetime import datetime
import urllib2
from bs4 import BeautifulSoup

print "imports Worked"

username = "edbrodeur" # replace with command prompt later
#BASE LOGARUN STRING = http://www.logarun.com/calendars/.../..., for example: edbrodeur/2017/06/18
baseURL = "http://www.logarun.com/calendars/"
todayDateForURL = "/%s/%s/%s" % (datetime.today().year, datetime.today().month, datetime.today().day)
print todayDateForURL

urlQuery = baseURL + username + todayDateForURL
print urlQuery

page = urllib2.urlopen(urlQuery)
soup = BeautifulSoup(page, 'html.parser')

noteBox = soup.find('div', attrs={'class': 'note'})
data = noteBox.text.strip()
print data