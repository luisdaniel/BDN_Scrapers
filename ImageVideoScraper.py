#--- This script takes a list of BDN links and searches for image links of different file extensions

from bs4 import BeautifulSoup
import re
import urllib2
import json
import csv

missedLinks = []

baseURL="http://web.archive.org/web/20130419035013/"
csvreader = csv.reader(open('narcoBlogLinks_original.csv', 'rU'), delimiter=",")
csv = list(csvreader)
data = []
with open('imagesNew.json', 'w') as f:
	for i in range(1, len(csv)):
		url = csv[i][2]
		print("Trying: " + url)
		try:
			page = urllib2.urlopen(baseURL + url).read()
		except:
			missedLinks.append(url)
			print("Not Found link: " + url)
			continue
		try:
			soup = BeautifulSoup(page)
			title = soup.find(['h2']).contents[0]
			imageLinks = []
			images = soup.findAll(href=re.compile(".gif"))
			for image in images:
				imageLinks.append(image['href'])
			images = soup.findAll(href=re.compile(".png"))
			for image in images:
				imageLinks.append(image['href'])
			print("Found: " + str(len(imageLinks)) + " images.")
			row = {
				"url": url,
				"title": title,
				"images": imageLinks
			}
			#data.append(row)
			#print(row['url']) #prints with correct encoding.
			#print(type(row['date'])) #<class 'bs4.element.NavigableString'>
			print("Scraped " + str(i))
			s = json.dumps(row, ensure_ascii=False)
			#print(s)
			f.write((s + '\n').encode('utf-8'))
		except Exception, e:
			missedLinks.append(url)
			print("Could not parse link: " + url)
			print("Because " + str(e))
			continue
print(missedLinks) #make note of which links weren't succesfully scraped and display them so I can pass them through this script again.

