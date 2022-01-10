import relevanceFinder


url = "https://www.nytimes.com/2021/10/10/climate/climate-action-congress.html"
urlList = relevanceFinder.getRelevantURLs(url)
urlList = urlList[0:4]