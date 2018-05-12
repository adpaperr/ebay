import bs4
import requests
import configs
import pandas as pd


# enter multiple phrases separated by '',
searchterm = 'matebook e'

# Creates the structure of a dataframe
def dfbuild():
	dataframe = pd.DataFrame(columns=['date_sold','name','link','price','bids'])
	return dataframe

# Resort Index by A-Z
def resort(dataframe, value):
	dataframe = dataframe.sort_values(by=value, ascending=False)
	dataframe = dataframe.reset_index(drop=True)
	return dataframe

# Search ebay for terms, return as soup
def search(term):
	site = 'http://www.ebay.com/sch/i.html?_from=R40&_nkw='+term+'&_in_kw=1&_ex_kw=&_sacat=0&LH_Sold=1&_udlo=&_udhi=&LH_Auction=1&_samilow=&_samihi=&_sadis=15&_stpos=90278-4805&_sargn=-1%26saslc%3D1&_salic=1&_sop=13&_dmd=1&_ipg=200&LH_Complete=1'
	res = requests.get(site)
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text, "lxml")
	return soup

# Grab the actual data from soup, fix dtypes
def pulldata(dataframe, soup):
	from datetime import datetime
	now = datetime.now()
	dataframe.date_sold = [e.span.contents[0].split(' ')[0] for e in soup.find_all(class_="tme")]
	dataframe.date_sold = dataframe.date_sold.apply(lambda x: datetime.strptime(x + str(now.year), '%b-%d' + '%Y'))
	dataframe.name = [e.contents[0] for e in soup.find_all(class_="vip")]
	dataframe.link = [e['href'] for e in soup.find_all(class_="vip")]
	dataframe.bids = [int(e.span.contents[0].split(' ')[0]) for e in soup.find_all("li", "lvformat")]
	dataframe.price = [e.contents[0] for e in soup.find_all("span", "bold bidsold")]
	dataframe.price = dataframe.price.replace('[\$,)]','', regex=True).astype(float)
	return dataframe

# Write out the file to CSV with the first sentence as file name
def writetocsv(dataframe):
	import csv
	filename = searchterm.split(' ', 1)[0]
	writer = pd.ExcelWriter('searches/{}.xls'.format(filename))
	dataframe.to_excel(writer, 'ebay_search', index = False)
	writer.save()

def main():
	df = dfbuild()
	soup = search(searchterm)
	df = pulldata(df, soup)
	df = resort(df, 'date_sold')

	start = df.date_sold.iloc[-1]
	end = df.date_sold.iloc[0]
	idx = pd.date_range(start, end)
	df.index = pd.DatetimeIndex(df.index)
	df = df.reindex(idx, fill_value='')

	print(df)
	writetocsv(df)

if __name__ == '__main__':
	main()


	# print(configs.pushuser)





