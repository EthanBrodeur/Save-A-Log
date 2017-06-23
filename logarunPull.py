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

testDate = "/2017/06/21"

#urlQuery = baseURL + username + dateFormat(currentDay)
urlQuery = baseURL + username + testDate
print "We will query: " + urlQuery


###Paging logarun.com... this is what takes awhile in Python###
#Grab what we need
page = urllib2.urlopen(urlQuery)
soup = BeautifulSoup(page, 'html.parser')

logTitle = soup.find('tr', attrs={'class': 'editTblDayTitle'}).get_text()
logNote = soup.find('p', attrs={'id': 'ctl00_Content_c_note_c_note'}).get_text()
print type(logTitle)
bikeDistances = []
bikeTypes = []
bikePaces = []
bikeTimes = []
rawHTMLbikeDistances = []
rawHTMLbikeTypes = []
rawHTMLbikePaces = []
rawHTMLbikeTimes = []
#switch the below to go through activitiesview
#workoutBox = soup.find('div', attrs={'class': 'applications'})
bikeBoxes = soup.findAll(attrs={'class': re.compile("app Bike.*")})
if bikeBoxes:
	for item in bikeBoxes: #for each bike that day
		rawHTMLbikeDistances += item.findAll(attrs={'id': re.compile("ctl00_c_value")})
		rawHTMLbikeTypes += item.findAll(attrs={'id': re.compile("ctl01_c_value")})
		rawHTMLbikeTimes += item.findAll(attrs={'id': re.compile("ctl02_c_value")})
		rawHTMLbikePaces += item.findAll(attrs={'id': re.compile("ctl03_c_value")})
	#Seems like a dumb way to grab this all but
	for span in rawHTMLbikeDistances:
		bikeDistances.append(float(span.text))
	for i in rawHTMLbikeTypes:
		#cleanedText = i.text.replace("(s)", "s")
		bikeTypes.append(unicode(i.text.replace("(s)", "s")))
	for i in rawHTMLbikeTimes:
		bikeTimes.append(unicode(i.text))#Probably change this cast later
	for i in rawHTMLbikePaces:
		bikePaces.append(unicode(i.text))

dailyBike = zip(bikeDistances,bikeTypes,bikeTimes, bikePaces)
print dailyBike

swimBox = soup.find('div', attrs={'class': 'app Swim'})

###Append current date's data to Pandas###


###utility functions###
#Converts a Date Object to Logarun URL Format
def dateFormat(date):
	#retURL = "/%s/%s/%s" % (date.year, date.month, date.day) #not clean
	return date.strftime("/%Y/%m/%d") # much cleaner

#move backwards current day
def subtractDay(date):
	retDate = date - timedelta(days=1)
	return retDate

#pull an activity from a day
#activityString: "Run", "Bike", "Elliptical", etc.
def getActivity(activityString):
	if type(activityString) != unicode:
		print "error! Didn't pass a string to getActivity"
		print 'you passed:'  
		print(type(activityString))
		sys.exit()

	regExString = "app %s.*" % activityString
	activityBoxes = soup.findAll(attrs={'class': re.compile(regExString)})
	if activityBoxes:
		activityDistances = []
		activityTypes = []
		activityPaces = []
		activityTimes = []
		rawHTMLActivityDistances = []
		rawHTMLActivityTypes = []
		rawHTMLActivityPaces = []
		rawHTMLActivityTimes = []
		for item in activityBoxes: #for each bike that day
			rawHTMLActivityTypes += (item.findAll(attrs={'id': re.compile("ctl01_c_value")}))
			rawHTMLActivityDistances += (item.findAll(attrs={'id': re.compile("ctl00_c_value")}))
			rawHTMLActivityTimes += (item.findAll(attrs={'id': re.compile("ctl02_c_value")}))
			rawHTMLActivityPaces += (item.findAll(attrs={'id': re.compile("ctl03_c_value")}))
		#Seems like a dumb way to grab this all but
		for span in rawHTMLActivityDistances:
			activityDistances.append(float(span.text))
		for i in rawHTMLActivityTypes:
			#cleanedText = i.text.replace("(s)", "s")
			activityTypes.append(unicode(i.text.replace("(s)", "s")))
		for i in rawHTMLActivityTimes:
			activityTimes.append(unicode(i.text))#Probably change this cast later
		for i in rawHTMLActivityPaces:
			activityPaces.append(unicode(i.text))
		
		dailyActivity = zip(activityDistances, activityTypes, activityTimes, activityPaces)
		return dailyActivity
	else:
		return 0

print getActivity(unicode("Bike"))
