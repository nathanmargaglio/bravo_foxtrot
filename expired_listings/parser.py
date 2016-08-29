import pandas as pd
import datetime
import requests
import re
import time

def parser(path):
	df = pd.read_csv("data/" +path+"/Expires Info.csv")

	df = df[df['Owner 1 First Name'] != '  '].reset_index()

	url = "http://people.yellowpages.com/whitepages?first={}&last={}&zip={}&state=ny"

	re_address = """<div class="address">\n(.*?)<"""
	re_phone = """<div class="phone">\n(.*?)<"""

	res_df = pd.DataFrame([], columns=['Owner 1 First Name','Owner 1 Last Name','Zip Code','Phone'])
	for n,row in enumerate(df.iterrows()):
		r = None
		print n, n/float(len(df))
		first = row[1]['Owner 1 First Name']
		last = row[1]['Owner 1 Last Name']
		zipcode = row[1]['Zip Code']
		ostreet = str(row[1]['Owner Street Num Street Name']).split(' ')[0]
		pstreet = str(row[1]['Street Number']).split(' ')[0]
		
		if ostreet == '':
			street = pstreet
		else:
			street = ostreet
		#~ print first, last, zipcode, street
		
		time.sleep(2)
		r = requests.get(url.format(first, last, zipcode))
			
		addresses = re.findall(re_address, r.text)
		phones = re.findall(re_phone, r.text)
		results = zip(addresses, phones)
		
		for n in results:
			if street == n[0].lstrip().rstrip().split(' ')[0]:
				phone = n[1].lstrip().rstrip()
				app_res = {
							'Owner 1 First Name':first,
							'Owner 1 Last Name':last,
							'Phone':phone}
				res_df = res_df.append(app_res, ignore_index=True)
				print res_df.iloc[-1]

	final_df = df.merge(res_df,how='outer',on=['Owner 1 First Name','Owner 1 Last Name'])
	final_df.to_csv("data/"+path+"/results.csv")

parser("8_23_2016")
