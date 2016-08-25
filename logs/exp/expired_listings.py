import time
import datetime
from crawler import crawler
from parser import parser
from html_generator import gen_html

todays_date = datetime.datetime.now().date()
#~ name = "{}_{}_{}".format(todays_date.month,todays_date.day,todays_date.year)
name = "new"
print "Crawling started:"
crawler(name)
print "Parsing Started:"
parser(name)
print "Generating HTML:"
gen_html(name)
print "Done!"
