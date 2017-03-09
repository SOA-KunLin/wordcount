from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from builtins import (
         bytes, dict, int, list, object, range, str,
         ascii, chr, hex, input, next, oct, open,
         pow, round, super,
         filter, map, zip)

import fileinput
import string
import itertools
import nltk
from collections import Counter

nltk.download('universal_tagset')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

from nltk.corpus import stopwords
stopwords = set(stopwords.words('english'))
punctuation = set(iter(string.punctuation))
stopwords = stopwords.union(punctuation)

def isalnum(s):
    return s.isalnum()

def is_not_stopwords(s):
    return not s in stopwords

# read sentences from stdin
lines = list(fileinput.input())

# split sentences into words (split, or nltk word_tokenize from nltk)
lines_tokens = map(nltk.word_tokenize, lines)
tokens = list(itertools.chain.from_iterable(lines_tokens))

# normalize words ('Word' and 'word' are considered as the same word)
tokens_normalized = map(string.lower, tokens)

# filter out symbols (isalpha, isdigit, isalnum)
tokens_no_symboles = filter(isalnum, tokens_normalized)

# filter out stopwords (stopwords from nltk)
tokens_no_stopwords = list(filter(is_not_stopwords, tokens_no_symboles))

# count the occurance of words (Counter)
wordCounter = Counter()
wordCounter.update(tokens_no_stopwords)

print("First part")
print("--------------------------------------------------------")
print(wordCounter.most_common(20))
print()


posTags = nltk.pos_tag(tokens_no_stopwords)
simplifiedTags = [(word, nltk.map_tag('en-ptb', 'universal', tag)) for word, tag in posTags]

posTagCounter = Counter()
posTagCounter.update(simplifiedTags)

posTags_count = list(map(lambda (pos_tag, count): (pos_tag[1], pos_tag[0], count), posTagCounter.iteritems()))

SimpliedTagsType = set(map(lambda item: item[0], posTags_count))

SimpliedTagsSummary = dict()
for tag_type in SimpliedTagsType:
    posTags = filter(lambda item: item[0] == tag_type, posTags_count)
    posTags = map(lambda item: (item[1], item[2]), posTags)
    SimpliedTagsSummary[tag_type] = \
        sorted(posTags, key=lambda item: item[1], reverse=True)

print("Bonus part")
print("--------------------------------------------------------")
print("VERB:")
print(SimpliedTagsSummary['VERB'][:20])
print("NOUN:")
print(SimpliedTagsSummary['NOUN'][:20])
