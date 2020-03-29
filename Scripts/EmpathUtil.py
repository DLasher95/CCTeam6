# this script does nothing right now

# https://github.com/Ejhfast/empath-client
from empath import Empath
lexicon = Empath()

lexicon.create_category("fast", ["fast"], model="fiction", size=1000)
lexicon.create_category("slow", ["slow"], model="fiction", size=1000)
lexicon.create_category("happy", ["happy"], model="fiction", size=1000)
lexicon.create_category("sad", ["sad"], model="fiction", size=1000)
lexicon.create_category("complex", ["complex"], model="fiction", size=1000)
lexicon.create_category("simple", ["simple"], model="fiction", size=1000)

sentence = 'An old man making tea in the morning'
spread = lexicon.analyze(sentence, categories=["fast", "slow", "happy", "sad", "complex", "simple"])