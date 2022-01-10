import sentence_transformers
import similarities
import threading
import relevanceFinder
import multiprocessing
from multiprocessing import cpu_count, Lock as mLock,Manager
from nltk.tokenize import word_tokenize
import urlAnalyzer
import getNewArticles
import relevanceFinder
import nltk.data
from sklearn.feature_extraction.text import TfidfVectorizer
import string
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import receivedInfo
from datetime import datetime


def main():
    cpu_count = multiprocessing.cpu_count()

    url = receivedInfo.url
    urlList = receivedInfo.urlList

    articleTextList = list()

    t1 = datetime.now()
    mainArticleText = urlAnalyzer.getArticleText(url)
    for article in urlList:
        articleTextList.append(urlAnalyzer.getArticleText(article))
    
    #tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    mainArticleSentences = mainArticleText.split(".")

    mainArticleSentences = [sentence for sentence in mainArticleSentences if len(sentence) > 40]

    articleSentencesList = list()

    for articleText in articleTextList:
        sentences = articleText.split(".")
        sentences = [sentence for sentence in sentences if len(sentence) > 40]
        articleSentencesList.append(sentences)

    model = SentenceTransformer('bert-base-nli-mean-tokens')
    sentence_embeddingsMain = model.encode(mainArticleSentences)

    t2 = datetime.now()
    print((t2-t1).total_seconds())


    #Call sentenceTuples.extend(similarities.findSimilarities(self.num))
    #with len(urlList) threads
    sentenceTuples = []

    with Manager() as manager:
        procList = []
        sentenceTuples = manager.list()
        for i in range(0,len(urlList)):
            process = multiprocessing.Process(target=similarities.findSimilarities,args=(i,sentenceTuples,model,sentence_embeddingsMain,mainArticleSentences,articleSentencesList))
            procList.append(process)

        for p in procList:
            p.start()

        for p in procList:
            p.join()
        
        sentenceTuples = list(sentenceTuples)

    with open("SimilarityTestingResults.txt","w",encoding="utf8") as outFile:
        for tuple in sentenceTuples:
            outFile.write("Main article: " + tuple[0] + "\n")
            outFile.write("Similar article: " + tuple[1] + "\n")
            outFile.write("\n")


if __name__ == "__main__":
    main()