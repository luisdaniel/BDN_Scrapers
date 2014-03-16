
#-------- This script opens up a file with a list of links and the uses Beautiful Soup to scrape the content of each link. 


from bs4 import BeautifulSoup
import re
import urllib2
import json
import csv

missedLinks = []


csvreader = csv.reader(open('blanks.csv', 'rU'), delimiter=",")
csv = list(csvreader)
data = []
#------ Link structure for BDN has changed and this script is no longer useful on BDN. Was still able to retrieve older blog entries from the Internet Archive
baseURL="http://web.archive.org/web/20130419035013/"


with open('blanks.json', 'w') as f:
	for i in range(1, len(csv)):
		url = baseURL+csv[i][1]
		print("Trying: " + url)
		page = urllib2.urlopen(url).read()
		try:
			soup = BeautifulSoup(page)
			title = soup.find(['h2']).contents[0]
			date = soup.find(attrs={"class": "date"}).contents[0]
			text = ''
			for node in soup.findAll(attrs={"class":"content"}):
				text += ''.join(node.findAll(text=True))
			row = {
				"url": url,
				"title": title,
				"date": date,
				"text": text
			}
			#data.append(row)
			print(row['text']) #prints with correct encoding.
			#print(type(row['date'])) #<class 'bs4.element.NavigableString'>
			print("Scraped " + str(i) + " articles")
			s = json.dumps(row, ensure_ascii=False)
			#print(s)
			f.write((s + '\n').encode('utf-8'))
		except:
			missedLinks.append(url)
			continue
print(missedLinks)
#------ For anything that went wrong during the scraping, write down which link wasn't able to be scraped and run the script again with those links
