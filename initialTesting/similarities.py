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

#https://stackoverflow.com/questions/4576077/how-can-i-split-a-text-into-sentences
#Showed me how to split text into sentences using nltk

#https://towardsdatascience.com/bert-for-measuring-text-similarity-eec91c6bf9e1.
#Using BERT to find similarities between text.

#https://www.tutorialspoint.com/python3/python_multithreading.htm
#Threading tutorial.

def findSimilarities(threadNum,sentenceTuples,model,sentence_embeddingsMain,mainArticleSentences,articleSentencesList):
    returnList = list()
    sentence_embeddings1 = model.encode(articleSentencesList[threadNum])

    #Generate a list of lists, containing cosine values for each sentence in the article
    similarityList = list()
    for sentence in sentence_embeddingsMain:
        similarity = cosine_similarity([sentence],sentence_embeddings1)
        similarityList.append(similarity)

    for mainArticleSentenceNum in range(0,len(similarityList)):
        for otherArticleNum in range(0,len(similarityList[mainArticleSentenceNum][0])):
            if similarityList[mainArticleSentenceNum][0][otherArticleNum] > .83:
                sentenceTuple = (mainArticleSentences[mainArticleSentenceNum].strip(),articleSentencesList[threadNum][otherArticleNum].strip())
                returnList.append(sentenceTuple)
    
    sentenceTuples.extend(returnList)