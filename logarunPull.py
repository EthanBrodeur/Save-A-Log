# -*- coding: utf-8 -*-

#Logarun Data Extraction script
import csv
import sys
import time
from datetime import datetime, timedelta
import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import re
#Import username from command line
if len(sys.argv) == 1:
	print "Terminating. You need to supply a username."
	sys.exit()
username = sys.argv[1]
print ("username = " + username)

###Build URL###
#A Logarun URl looks like: http://www.logarun.com/calendars/<username>/<year>/<month>/<day>
#For example: http://www.logarun.com/calendars/edbrodeur/2017/06/18
baseURL = "http://www.logarun.com/calendars/"
currentDay = datetime.today()

#To add:loop through all the days you want

testDate = "/2017/06/17"

#urlQuery = baseURL + username + dateFormat(currentDay)
urlQuery = baseURL + username + testDate
print "We will query: " + urlQuery


###Paging logarun.com... this is what takes awhile in Python###
#Grab what we need
page = urllib2.urlopen(urlQuery)
soup = BeautifulSoup(page, 'html.parser')
logTitle = soup.find('tr', attrs={'class': 'editTblDayTitle'}).get_text()
logNote = soup.find('p', attrs={'id': 'ctl00_Content_c_note_c_note'}).get_text()


bikeBox = soup.find('div', attrs={'class': 'app Bike appColor'})
dubBikeBox = soup.find('div', attrs={'class': 'app Bike'})

swimBox = soup.find('div', attrs={'class': 'app Swim'})

if bikeBox:
	bikeDistanceFinder = bikeBox.findAll('span', id=re.compile("ctl00_c_value"))
	bikeDistance = float(bikeDistanceFinder[0].get_text())
	print bikeDistance
if dubBikeBox:
	bikeDistanceFinder = dubBikeBox.findAll('span', id=re.compile("ctl00_c_value"))
	dubBikeDistance = float(bikeDistanceFinder[0].get_text())
	print dubBikeDistance
###Append current date's data to Pandas###


###utility functions###
#Converts a Date Object to Logarun URL Format
def dateFormat(date):
	retURL = "/%s/%s/%s" % (date.year, date.month, date.day)
	return retURL

#move backwards current day
def subtractDay(date):
	retDate = date - timedelta(days=1)
	return retDate
