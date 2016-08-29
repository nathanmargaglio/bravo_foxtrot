import time
import datetime
from crawler import crawler
from parser import parser

todays_date = datetime.datetime.now().date()
name = "{}_{}_{}".format(todays_date.month,todays_date.day,todays_date.year)
print "Crawling started:"
crawler(name)
print "Parsing Started:"
parser(name)
print "Done!"
