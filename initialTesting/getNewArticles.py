import requests
from bs4 import BeautifulSoup
import re


def returnRelevantURLs(searchTerm): #Return relevant NYT URLs for a given search term
    urlList = list()
    url = "https://www.nytimes.com/search?query=" + searchTerm
    soup = BeautifulSoup(requests.get(url).text,"lxml")
    for link in soup.find_all('a'):
        if link.get('href')[0] == '/' and "sitemap" not in link.get('href') and link.get('href') != '/':
            urlList.append("https://www.nytimes.com" + link.get('href'))
    return urlList
#Probably going to end up using this one more. Can take these urls and pass them through
#urlAnalyzer.py to check keyword matches and analyze political bias
#Cyber operator expedited track
#Computer Network Assessment Battery