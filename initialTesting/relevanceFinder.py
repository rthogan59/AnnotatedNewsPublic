import os
import getNewArticles
import urlAnalyzer

#Process:
#1. Get URL from user
#2. Get keywords from that URL (urlAnalyzer)
#3. Use keywords to get relevant urls from that URL
    #Need to refine the process for getting keywords

def getRelevantURLs(url):
    titleKeywords = urlAnalyzer.getTitleKeywords(url)
    searchTerm = ""
    for word in titleKeywords:
        searchTerm += word + " "
    searchTerm = searchTerm[:-1]

    relevantURLs = getNewArticles.returnRelevantURLs(searchTerm)
    for newURL in relevantURLs:
        if url in newURL:
            relevantURLs.remove(newURL)

    return relevantURLs
    
#Test URL:
#"https://www.nytimes.com/2021/10/10/climate/climate-action-congress.html"

"""
for url in getRelevantURLs("https://www.nytimes.com/2021/10/10/climate/climate-action-congress.html"):
    print(url)
    print(urlAnalyzer.getTitleKeywords(url))
    print(urlAnalyzer.getArticleKeywords(url))
    print("\n")
"""

def returnSearchKeywords(searchTerm):
    returnList = list()
    relevantUrls = getNewArticles.returnRelevantURLs(searchTerm)
    for url in relevantUrls:
        titleKeywords = urlAnalyzer.getTitleKeywords(url)
        returnList.append(titleKeywords)
    return returnList
