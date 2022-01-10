from nltk.corpus.reader.wordnet import SENSENUM_RE
from sklearn.feature_extraction.text import CountVectorizer
import urlAnalyzer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import itertools

def max_sum_sim(doc_embedding, word_embeddings, words, top_n, nr_candidates):
    # Calculate distances and extract keywords
    distances = cosine_similarity(doc_embedding, candidate_embeddings)
    distances_candidates = cosine_similarity(candidate_embeddings, 
                                            candidate_embeddings)

    # Get top_n words as candidates based on cosine similarity
    words_idx = list(distances.argsort()[0][-nr_candidates:])
    words_vals = [candidates[index] for index in words_idx]
    distances_candidates = distances_candidates[np.ix_(words_idx, words_idx)]

    # Calculate the combination of words that are the least similar to each other
    min_sim = np.inf
    candidate = None
    for combination in itertools.combinations(range(len(words_idx)), top_n):
        sim = sum([distances_candidates[i][j] for i in combination for j in combination if i != j])
        if sim < min_sim:
            candidate = combination
            min_sim = sim

    return [words_vals[idx] for idx in candidate]


def mmr(doc_embedding, word_embeddings, words, top_n, diversity):

    # Extract similarity within words, and between words and the document
    word_doc_similarity = cosine_similarity(word_embeddings, doc_embedding)
    word_similarity = cosine_similarity(word_embeddings)

    # Initialize candidates and already choose best keyword/keyphras
    keywords_idx = [np.argmax(word_doc_similarity)]
    candidates_idx = [i for i in range(len(words)) if i != keywords_idx[0]]

    for _ in range(top_n - 1):
        # Extract similarities within candidates and
        # between candidates and selected keywords/phrases
        candidate_similarities = word_doc_similarity[candidates_idx, :]
        target_similarities = np.max(word_similarity[candidates_idx][:, keywords_idx], axis=1)

        # Calculate MMR
        mmr = (1-diversity) * candidate_similarities - diversity * target_similarities.reshape(-1, 1)
        mmr_idx = candidates_idx[np.argmax(mmr)]

        # Update keywords & candidates
        keywords_idx.append(mmr_idx)
        candidates_idx.remove(mmr_idx)

    return [words[idx] for idx in keywords_idx]

n_gram_range = (6,6)
stop_words = "english"

doc = urlAnalyzer.getArticleText("https://www.nytimes.com/2021/04/05/world/europe/iran-nuclear-talks-explained.html")

count = CountVectorizer(ngram_range=n_gram_range).fit([doc])

candidates = count.get_feature_names_out()


#Pre-trained models
#xlm-r-distilroberta-base-paraphase-v1
#distilbert-base-nli-stsb-mean-tokens

model = SentenceTransformer('xlm-r-distilroberta-base-paraphrase-v1')
doc_embedding = model.encode([doc])
candidate_embeddings = model.encode(candidates)

"""
#Find candidates that are most similar to the document
top_n = 5
distances = cosine_similarity(doc_embedding, candidate_embeddings)
keywords = [candidates[index] for index in distances.argsort()[0][-top_n:]]
"""

print(max_sum_sim(doc_embedding,candidate_embeddings,candidates,top_n=5,nr_candidates=20))
print(mmr(doc_embedding,candidate_embeddings,candidates,top_n=5,diversity=-0.7))