from goose import Goose
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
from nltk.classify import *
from sklearn.naive_bayes import BernoulliNB
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import sys
import re
from math import sqrt
import numpy as np
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.feature_extraction.text import CountVectorizer
import cPickle
from main.models import *
def extract_content(url):
    print "here in gooose"
    g = Goose()
    article = g.extract(url = url)
    title = article.title
    img_src = article.top_image.src
    content = article.cleaned_text
    print "befire if"
    print title
    if article.title and img_src:
        print "here in if"
        return title,content.encode('utf-8'),img_src
    else:
       return "","",""
def cosine_metric(content1,content2):
    train_set = [content1,content2]
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix_train = tfidf_vectorizer.fit_transform(train_set)
    val = cosine_similarity(tfidf_matrix_train[0], tfidf_matrix_train[1])
    return val.item(0,0)

def aggregate(wc,apcount):
   for word ,count in wc.items():
        apcount.setdefault(word,0)
        if count > 1:
            apcount[word]+=1
   return apcount
def getwordcount(content):
    word_count=0
    wc = {}
    tokens = re.compile(r'[^A-Z^a-z]+').split(content)
    for word in tokens:
            if word.lower() not in stopwords.words('english'):
               if len(word) > 1:
                  w = word.lower()
                  wc.setdefault(w,0)
                  wc[w]+=1
                  word_count+=1
    return wc
def pearson(v1,v2):
  # Simple sums
  sum1=sum(v1)
  sum2=sum(v2)

  # Sums of the squares
  sum1Sq=sum([pow(v,2) for v in v1])
  sum2Sq=sum([pow(v,2) for v in v2])

  # Sum of the products
  pSum=sum([v1[i]*v2[i] for i in range(len(v1))])

  # Calculate r (Pearson score)
  num=pSum-(sum1*sum2/len(v1))
  den=sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))
  if den==0: return 0

  return 1.0-num/den
def find_similar(content1,content2):
         dist = 0.0
         similar = cosine_metric(content1,content2)
         if similar > 0.85:
           dist = calculate_distance(content1,content2)
           print dist
           return dist

def calculate_distance(content1,content2):
  apcount = {}
  wordscount = {}
  data = []
  wc = getwordcount(content1)
  apcount = aggregate(wc,apcount)
  wordscount["content1"] = wc
  wc = getwordcount(content2)
  apcount = aggregate(wc,apcount)
  wordscount["content2"] = wc
  wordlist = []

  for w,bc in apcount.items():
          wordlist.append(w)
  for blog,wc in wordscount.items():
    temp = []
    for word in wordlist:
        if word in wc:
         temp.append(float(wc[word]))
        else:
         temp.append(float(0))

    data.append(temp)
  dist = pearson(data[0],data[1])
  return dist

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
    return result

def get_feature(word):
    return dict([(word, True)])


def bag_of_words(words):
    return dict([(word, True) for word in words])


def create_training_dict(text, sense):
    ''' returns a dict ready for a classifier's test method '''
    tokens = extract_words(text)
    return [(bag_of_words(tokens), sense)]



def classify_link(content):

 if(len(content)>200):
  tokens = bag_of_words(extract_words(content))
  import os
  f1= open('/home/nivedita/linker/linker/media/nltk/my_dataset.pkl')
  classifier=cPickle.load(f1)
  f1.close()
 #print tokens
  decision = classifier.classify(tokens)
  labels  = classifier.prob_classify(tokens)
  #batch = classifier.batch_classify(tokens)
  #for b in batch:
   # print b
  return decision
