import csv
import bs4
import requests
#import argparse
import pandas as pd


# enter multiple phrases separated by '',
sampleterm = ['matebook e']
df = pd.DataFrame(columns=['date_sold','name','link','price','bids'])

# Resort Index by A-Z
def resort(dataframe, value):
	dataframe = dataframe.sort_values(value)
	dataframe = dataframe.reset_index(drop=True)
	return dataframe

# Search ebay for terms, return as soupp
def search(terms):
	for term in terms:
		site = 'http://www.ebay.com/sch/i.html?_from=R40&_nkw='+term+'&_in_kw=1&_ex_kw=&_sacat=0&LH_Sold=1&_udlo=&_udhi=&LH_Auction=1&_samilow=&_samihi=&_sadis=15&_stpos=90278-4805&_sargn=-1%26saslc%3D1&_salic=1&_sop=13&_dmd=1&_ipg=200&LH_Complete=1'
		res = requests.get(site)
		res.raise_for_status()
		soup = bs4.BeautifulSoup(res.text, "lxml")
	return soup


soup = search(sampleterm)

df.date_sold = [e.span.contents[0].split(' ')[0] for e in soup.find_all(class_="tme")] 	# Date/Time Stamp
df.name = [e.contents[0] for e in soup.find_all(class_="vip")] 							# Name of item
df.link = [e['href'] for e in soup.find_all(class_="vip")]								# Store links
df.bids = [e.span.contents[0].split(' ')[0] for e in soup.find_all("li", "lvformat")]	# Bid Spans
df.price = [e.contents[0] for e in soup.find_all("span", "bold bidsold")]				# Prices

#df = resort(df, 'date_sold')
print(soup.prettify())
print(df)

	# l = [e for e in zip(dte, titles, links, prices, bids)]
	# print(l)
	
	# write each entry of the rowlist `l` to the csv output file
	# with open('%s.csv' % phrase, 'wb') as csvfile:
	#     w = csv.writer(csvfile)
	#     for e in l:
	#         w.writerow(e)

	# with open('{}.csv'.format(phrases), 'w') as csvfile:
	# 	wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
	# 	wr.writerow(l)

	# writer = pd.ExcelWriter('{}.xls'.format(phrases))
	# for e in l:
	# 	e.to_excel(writer, 'Unique', index = False)
	# writer.save()	






