#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 07:18:20 2021

@author: maga
"""

import json
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import demoji
import pickle


# Load data
infile = open('tweet_TR.json','rb')
tweets = json.load(infile)
infile.close()

# Function to remove stopwords
def remove_stopwords(text): 
    text_wo_stopwords = []  
    stop_words = set(stopwords.words('english'))
    text = re.split('\s',text)
    for t in text:
        if t not in stop_words:
            text_wo_stopwords.append(t)
    text_wo_stopwords = ' '.join(text_wo_stopwords)
    return text_wo_stopwords

# Function to preprocess tweets
def preprocess(raw_tweet):
    text = raw_tweet.lower() # convert to lowercase
    text = re.sub('\n',' ',text) # remove '\n'
    text = re.sub(r"http\S+", "",text) # remove urls
    text = re.sub('#',' ',text) # remove '#' but leave text from hashtag
    text = re.sub('@[a-zA-Z]+',' ', text) # remove mentions
    text = re.sub('^rt ',' ', text) # remove 'rt'
    text = re.sub('[,\.\:\!¡\?\¿\–\_\-\’\$%|@\'—\...=/)/(]',' ',text) # remove punctuation
    text = re.sub('[0-9]+', ' ',text) # remove numbers
    text = demoji.replace(text, '') # remove emojis
    text = re.sub('\s+',' ',text) # remove extra whitespaces
    text = re.sub('^\s+','',text) # remove space(s) at start
    text = re.sub('\s+$','',text) # remove space(s) at end
    text = remove_stopwords(text)
    return text

# Extract all tweets in English
def get_tweets_en(tweets_dic):
    data = []    
    for tweet in tweets:
        raw_text = tweet['text_en']
        text = preprocess(raw_text)
        data.append(text)             
    return data

data = get_tweets_en(tweets)


with open('preprocessed_tweets.pickle', 'wb') as fp:
    pickle.dump(data, fp)

