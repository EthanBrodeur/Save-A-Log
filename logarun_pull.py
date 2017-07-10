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


def main():
	# Import username from command line
	if len(sys.argv) == 1:
		print("Terminating. You need to supply a username.")
		sys.exit()
	username = sys.argv[1]
	print("username = " + username)
	current_day = datetime.today()


	# BUILD URL
	# A Logarun URl looks like:
	# http://www.logarun.com/calendars/<username>/<year>/<month>/<day>
	# For example: http://www.logarun.com/calendars/edbrodeur/2017/06/18
	base_URL = "http://www.logarun.com/calendars/"

	#TODO: Request number of days back to go from user, set that up as a date range in pandas, set that date range as the dataframe index
	num_days_back = 50
	index = pd.date_range(current_day - timedelta(days=num_days_back), periods=num_days_back, freq='D')
	
	headers =["Date", "Log Title", "Log Note", "Activity", "Atcivity Distance", "Activity Type", "Activity Time", "Activity Pace"]
	df = pd.DataFrame(columns=headers)

	while num_days_back >= 0:

		url_query = base_URL + username + date_format(current_day)
		print("We will query: " + url_query)

		# Paging logarun.com... this is what takes awhile
		page = urllib2.urlopen(url_query)
		soup = BeautifulSoup(page, 'html.parser')

		try:
			df.append(get_activity(unicode("Bike"), soup, current_day))
		except TypeError:
			print("bike didn't happen that day")

		try:
			df.append(get_activity(unicode("Run"), soup, current_day))
		except TypeError:
			print("run didn't happen that day")

		try:
			df.append(get_activity(unicode("Swim"), soup, current_day))
		except TypeError:
			print("swim didn't happen that day")

		try:
			df.append(get_activity(unicode("Elliptical"), soup, current_day))
		except TypeError:
			print("elliptical didn't happen that day")

		num_days_back -= 1
		current_day = subtract_day(current_day)

	print(df.describe())
	print(df.head())
	print(df)
	df.to_csv("myLog")

"""Utility Functions"""
def date_format(date):
	"""Converts a Date Object to Logarun URL Format"""

	# retURL = "/%s/%s/%s" % (date.year, date.month, date.day) # not clean
	return date.strftime("/%Y/%m/%d")  # much cleaner


def subtract_day(date):
	"""Converts a Date Object to Logarun URL Format"""

	retDate = date - timedelta(days=1)
	return retDate


def get_activity(activity_string, soup, date):
	"""pull an activity from a day.	
	activity_string: "Run", "Bike", "Elliptical", etc.
	"""
	if not isinstance(activity_string, basestring):
		print("error! Didn't pass a string to get_activity")
		print('you passed:')
		print(type(activity_string))
		sys.exit()

	log_title = soup.find('tr', attrs={'class': 'editTblDayTitle'}).get_text()
	log_note = soup.find('p', attrs={'id': 'ctl00_Content_c_note_c_note'}).get_text()
	
	regExString = "app %s.*" % activity_string
	activity_boxes = soup.findAll(attrs={'class': re.compile(regExString)})
	if activity_boxes:
		activity_distances = []
		activity_types = []
		activity_paces = []
		activity_times = []
		raw_HTML_activity_distances = []
		raw_HTML_activity_types = []
		raw_HTML_activity_paces = []
		raw_HTML_activity_times = []
		index_date = []
		for item in activity_boxes:  # for each bike that day
			raw_HTML_activity_types += (item.findAll(attrs={'id': re.compile("ctl01_c_value")}))
			raw_HTML_activity_distances += (item.findAll(attrs={'id': re.compile("ctl00_c_value")}))
			raw_HTML_activity_times += (item.findAll(attrs={'id': re.compile("ctl02_c_value")}))
			raw_HTML_activity_paces += (item.findAll(attrs={'id': re.compile("ctl03_c_value")}))
		# Seems like a dumb way to grab this all but
		for span in raw_HTML_activity_distances:
			activity_distances.append(float(span.text))
		for i in raw_HTML_activity_types:
			# cleanedText = i.text.replace("(s)", "s")
			activity_types.append(unicode(i.text.replace("(s)", "s")))
		for i in raw_HTML_activity_times:
			activity_times.append(unicode(i.text))  # Probably change this cast later
		for i in raw_HTML_activity_paces:
			activity_paces.append(unicode(i.text))
		index_date.append(date)
		df = pd.DataFrame({
			'Log Title' : log_title,
			'Log Note' : log_note,
			'Acivity': activity_string,
			'Activity Distance' : activity_distances,
			'Activity Type' : activity_types,
			'Activitiy Time' : activity_times,
			'Activity Pace' : activity_paces}, index=index_date) #ValueError: could not broadcast input array from shape (2) into shape (1)

		return df

	else:
		return 0

	
if __name__ == "__main__":
	main()


