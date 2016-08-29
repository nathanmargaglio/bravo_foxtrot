import time
import datetime
from crawler import crawler
from parser import parser

#~ todays_date = datetime.datetime.now().date()
#~ name = "{}_{}_{}".format(todays_date.month,todays_date.day,todays_date.year)
#~ print "Crawling started:"
#~ crawler(name)
#~ print "Parsing Started:"
#~ parser(name)
#~ print "Done!"

if __name__ == "__main__":
	for i in range(19,30):
		name = "8_{}_2016".format(str(i))
		date = "08/{}/2016".format(str(i))
		crawler(name,date)
		parser(name)
