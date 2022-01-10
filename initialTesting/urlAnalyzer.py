#https://www.pluralsight.com/guides/extracting-data-html-beautifulsoup
#https://www.analyticsvidhya.com/blog/2020/11/words-that-matter-a-simple-guide-to-keyword-extraction-in-python/
import requests
from bs4 import BeautifulSoup
import nltk
from nltk import tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import RAKE
import operator
from rake_nltk import Rake
from operator import itemgetter
import math
stop_words = set(stopwords.words('english'))
#This program is used to take a url and find keywords in the article content

def getArticleText(url):
    soup = BeautifulSoup(requests.get(url).text,"lxml")
    articleText = ''
    for textContent in soup.find_all('p'):
        articleText += textContent.text
    return articleText

def getTitleKeywords(url):
    try:
        keywords = list()
        soup = BeautifulSoup(requests.get(url).text,"lxml")
        title = soup.find('h1').text.split()
        for word in title:
            if word not in stop_words and len(word) > 3:
                keywords.append(word)
        return keywords[0:4]
    except:
        return list()

def Sort_Tuple(tup):
    tup.sort(key = lambda x: x[1])
    return tup

def getArticleKeywords(url):
    r = Rake()
    articleText = getArticleText(url)
    r.extract_keywords_from_text(articleText)
    phrases = r.get_ranked_phrases()[0:10]
    phrases = filter(lambda x: "advertisement" not in x, phrases)
    return list(phrases)


titleKeywords = getTitleKeywords("https://www.nytimes.com/2021/10/10/climate/climate-action-congress.html")
articleKeywords = getArticleKeywords("https://www.nytimes.com/2021/10/10/climate/climate-action-congress.html")

#MAJ Joseph Littel - Bert Questions
#Add actual unbiased facts (i.e. Actual text of Iranian nuclear agreement)