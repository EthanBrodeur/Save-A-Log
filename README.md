# Save-A-Log
Backs up running data from logarun.com to an Excel file with BeautifulSoup + Pandas


# Usage
To pull data, run the following in terminal when inside the Save-A-Log directory:
```
$ python logarunPull.py myUsername [-d number of days back]
```

Script will prompt user to input the account's password. If the account is public, just leave blank.

Additional modifiers for date ranges, output formatting forthcoming.

# Notes
Usage requires the following to be installed:
- FireFox
- BeautifulSoup4
- numpy
- pandas
- geckodriver