from goose import Goose
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
from nltk.classify import *
from nltk.probability import DictionaryProbDist
from nltk.corpus import wordnet
#from sklearn.svm.sparse import LinearSVC
from sklearn.naive_bayes import BernoulliNB
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import sys
import urllib2
from nltk.corpus import brown
import random
import numpy as np
from sklearn.multiclass import OneVsRestClassifier
#from sklearn.feature_extraction.text import CountVectorizer
import cPickle
def extract_content(url):
    print "here in gooose"
    g = Goose()
    article = g.extract(url = url)
    title = article.title
    img_src = article.top_image.src
    content = article.cleaned_text[:500]
    if article.title and img_src:
        return title,content,img_src
    else:
       return "","",""
def extract_words(text):

    '''
   here we are extracting features to use in our classifier. We want to pull all the words in our input
   porterstem them and grab the most significant bigrams to add to the mix as well.
   '''

    stemmer = PorterStemmer()

    tokenizer = WordPunctTokenizer()
    tokens = tokenizer.tokenize(text)
    bigram_finder = BigramCollocationFinder.from_words(tokens)
    bigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 500)

    for bigram_tuple in bigrams:
        x = "%s %s" % bigram_tuple
        tokens.append(x)

    result =  [stemmer.stem(x.lower()) for x in tokens if x not in stopwords.words('english') and len(x) > 1]
    print result
    return result

def get_feature(word):
    return dict([(word, True)])


def bag_of_words(words):
    return dict([(word, True) for word in words])


def create_training_dict(text, sense):
    ''' returns a dict ready for a classifier's test method '''
    tokens = extract_words(text)
    return [(bag_of_words(tokens), sense)]



def classify(content):
 if(len(content)>200):
  tokens = bag_of_words(extract_words(line))
  f1= open('my_dataset.pkl')
  classifier=cPickle.load(f1)
  f1.close()
 #print tokens
  decision = classifier.classify(tokens)
  labels  = classifier.prob_classify(tokens)
  #batch = classifier.batch_classify(tokens)
  #for b in batch:
   # print b
  return decision