import nltk
#nltk.download('wordnet')
from nltk.corpus import wordnet as wn


# compare every word in s1 to every word in s2
# get the average at the end
def compare(i1, i2, debug=False):
    # https://mkyong.com/python/python-how-to-split-a-string/
    s1 = i1.split()
    s2 = i2.split()

    score = 0
    count = 0

    for w1 in s1:
        for w2 in s2:
            try:
                # research this more
                a = w1 + '.n.01'
                b = w2 + '.n.01'
                one = wn.synset(a)
                two = wn.synset(b)
                score += one.path_similarity(two)
                count += 1
                if debug:
                    print('[' + w1 + ', ' + w2 + '] = ' + str('% .2f' % round(one.path_similarity(two), 2)))
            except Exception as e:
                if debug:
                    print('Could not determine similarity of ' + w1 + ' and ' + w2)
                    print(e)

    return score / count if count > 0 else 0
