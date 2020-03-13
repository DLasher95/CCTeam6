import nltk
#nltk.download()
from nltk.corpus import wordnet as wn

#one = wn.synset('dog')
one = wn.synset('.n.01')
#two = wn.synset('cat')
two = wn.synset('guitar.n.01')
print(str(one.path_similarity(two)))