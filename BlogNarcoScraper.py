#----Scrapes links from BDN. link structure on BDN has since changed. 
#----Posts used to be listed with simple URL structure: www.blogdelnarco.com/month/page#

from BeautifulSoup import BeautifulSoup
import re
import urllib2
import json
import csv

csvwriter = csv.writer(open("narcoBlogLinks.csv", "w"))
csvwriter.writerow(["year", "month", "url"])
blogLinks = []

baseURL  = "http://www.blogdelnarco.com/"

for i in range(2010, 2014):
	if i == 2010:
		startMonth = 3
	else:
		startMonth = 1
	for j in range(startMonth, 13):
		if j < 10:
			url = baseURL + str(i) + "/0" + str(j) + "/"
		else:
			url = baseURL + str(i) + "/" + str(j) +"/"
		print url
		page = urllib2.urlopen(url).read()
		soup = BeautifulSoup(page)
		lastLink = soup.findAll(attrs = {"class":"last"})
		lastPage = int(str(lastLink)[str(lastLink).find("page/")+5:str(lastLink).find('/" class')])
		for k in range(1, lastPage+1):
			kURL = url + "page/" + str(k) + "/"
			print "Scraping: " + kURL
			page = urllib2.urlopen(kURL).read()
			soup = BeautifulSoup(page)
			links = soup.findAll(attrs={'class':'title'})
			for link in links:
				pageURL = str(link)[str(link).find('ref="')+5:str(link).find('" rel')]
				month = str(j)
				year = str(i)
				print "Adding: " + pageURL
				newRow = [year, month, pageURL]
				csvwriter.writerow(newRow)
				

