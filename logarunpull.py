# -*- coding: utf-8 -*-

# Logarun Data Extraction script
import csv
import sys
import time
from datetime import datetime, timedelta
import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np

currentDay = datetime.today()

def main():
	# Import username from command line
	if len(sys.argv) == 1:
		print("Terminating. You need to supply a username.")
		sys.exit()
	username = sys.argv[1]
	print("username = " + username)

	# BUILD URL
	# A Logarun URl looks like:
	# http://www.logarun.com/calendars/<username>/<year>/<month>/<day>
	# For example: http://www.logarun.com/calendars/edbrodeur/2017/06/18
	baseURL = "http://www.logarun.com/calendars/"

	#TODO: Request number of days back to go from user, set that up as a date range in pandas, set that date range as the dataframe index
	numDaysBack = 100
	index = pd.date_range(currentDay - timedelta(days=numDaysBack), periods=numDaysBack, freq='D')
	
	httpeaders = "activityName", "activityDistances", "activityTypes", "activityTimes", "activityPaces"
	#df = pd.DataFrame(index=index, columns=headers)
	#print df.head()

	# To add:loop through all the days you want

	testDate = "/2017/06/21"

	# urlQuery = baseURL + username + date_format(currentDay)
	urlQuery = baseURL + username + testDate
	print("We will query: " + urlQuery)

	# Paging logarun.com... this is what takes awhile
	page = urllib2.urlopen(urlQuery)
	soup = BeautifulSoup(page, 'html.parser')

	logTitle = soup.find('tr', attrs={'class': 'editTblDayTitle'}).get_text()
	logNote = soup.find('p', attrs={'id': 'ctl00_Content_c_note_c_note'}).get_text()

	print(get_activity(unicode("Bike"), soup))

	# Append today's data to df

"""Utility Functions"""


def date_format(date):
	"""Converts a Date Object to Logarun URL Format"""

	# retURL = "/%s/%s/%s" % (date.year, date.month, date.day) # not clean
	return date.strftime("/%Y/%m/%d")  # much cleaner


def subtract_day(date):
	"""Converts a Date Object to Logarun URL Format"""

	retDate = date - timedelta(days=1)
	return retDate


def get_activity(activityString, soup):
	"""pull an activity from a day.	
	activityString: "Run", "Bike", "Elliptical", etc.
	"""
	if not isinstance(activityString, basestring):
		print("error! Didn't pass a string to get_activity")
		print('you passed:')
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
		indexDate = []
		for item in activityBoxes:  # for each bike that day
			rawHTMLActivityTypes += (item.findAll(attrs={'id': re.compile("ctl01_c_value")}))
			rawHTMLActivityDistances += (item.findAll(attrs={'id': re.compile("ctl00_c_value")}))
			rawHTMLActivityTimes += (item.findAll(attrs={'id': re.compile("ctl02_c_value")}))
			rawHTMLActivityPaces += (item.findAll(attrs={'id': re.compile("ctl03_c_value")}))
		# Seems like a dumb way to grab this all but
		for span in rawHTMLActivityDistances:
			activityDistances.append(float(span.text))
		for i in rawHTMLActivityTypes:
			# cleanedText = i.text.replace("(s)", "s")
			activityTypes.append(unicode(i.text.replace("(s)", "s")))
		for i in rawHTMLActivityTimes:
			activityTimes.append(unicode(i.text))  # Probably change this cast later
		for i in rawHTMLActivityPaces:
			activityPaces.append(unicode(i.text))
		indexDate.append(currentDay)
		df = pd.DataFrame({
			'activity_distance' : activityDistances,
			'activityTypes' : activityTypes,
			'activityTimes' : activityTimes,
			'activityPaces' : activityPaces},index=indexDate)
		print df.head()
		return df

	else:
		return 0

	
if __name__ == "__main__":
	main()


