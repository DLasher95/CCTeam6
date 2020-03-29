import nltk
import os
import itertools
#nltk.download('wordnet')
from nltk.corpus import wordnet as wn

# Word2Vec?
# https://rare-technologies.com/word2vec-tutorial/
from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec

# https://www.programcreek.com/python/example/91606/nltk.corpus.wordnet.wup_similarity


# this used to work lol
def compare_arrays(one, two):
    score = 0
    count = 0

    for wi in one:
        i = wn.synsets(wi)
        for wj in two:
            j = wn.synsets(wj)
            s = i.wup_similarity(j)
            if s is not None:
                score += s
                count += 1

    return score / count if count > 0 else 0

def score_one_to_one(word1, word2):
    allsyns1 = set(ss for ss in wn.synsets(word1))
    allsyns2 = set(ss for ss in wn.synsets(word2))
    try:
        best = max((wn.wup_similarity(s1, s2) or 0) for s1, s2 in
            itertools.product(allsyns1, allsyns2))
    except:
        best = 0
    return best
def score_many_to_one(arr, cat):
    # average score per word in array
    score = 0
    for w in arr:
        score += score_one_to_one(w, cat)
    return score / len(arr)
def score_many_to_many(arr1, arr2):
    score = 0
    for w in arr1:
        score += score_many_to_one(arr2, w)
    return score / len(arr1)


categories = ['fast', 'slow', 'happy', 'sad', 'complex', 'simple']
ex = ['white', 'sheep', 'standing', 'field', 'happiness']
ex2 = ['man', 'umbrella', 'standing', 'front', 'building', 'fear', 'sadness', 'calmness']

def print_example(example):
    print('Scoring: ' + ', '.join(w for w in ex))
    for cat in categories:
        cat_score = score_many_to_one(ex, cat)
        print(cat + ': ' + str(cat_score))
