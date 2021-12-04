#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
from tqdm import tqdm
import nltk
import pickle

# Load data
with open ('preprocessed_tweets.pickle', 'rb') as fp:
    tweets = pickle.load(fp)
    
from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')

'''
Before running the sentiment annotator:
Download the Stanford Core NLP model (https://stanfordnlp.github.io/CoreNLP/#download)
Unizip the folder
cd into the folder
cd stanford-corenlp-4.3.2/
Start the server using this command:
java -mx5g -cp "./*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000 
'''

# Assign sentiment
def getSentiments():
    sentiments = []
    for tweet in tweets:
        res = nlp.annotate(tweet,
                       properties={'annotators': 'sentiment',
                                   'outputFormat': 'json',
                                   'timeout': 1000
                       })
    
    
        try:
            s = res['sentences'][0]['sentiment']
        except:
            s = ''
        sentiments.append(s)
    return sentiments

def updateJsonFile():
    jsonFile = open("tweets_emotions.json", "r") 
    data = json.load(jsonFile) 
    jsonFile.close()
    
    sentiments = getSentiments()
    i = 0
    for tweet in tqdm(data): 
        tweet['sentiment'] = sentiments[i]
        i += 1

    with open("tweets_emoSent.json", "w+") as jsonFile: 
        jsonFile.write(json.dumps(data))


updateJsonFile()


# # Check json file 
# jsonFile = open("tweets_emoSent.json", "r") 
# check = json.load(jsonFile) 
# jsonFile.close()

# # Check how many tweets don't have a sentiment
# count = 0
# for tweet in check:
#     if tweet['sentiment'] == '':
#         count += 1
# count # 462

