#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
from tqdm import tqdm
from nrclex import NRCLex 
import pickle

# Load data
with open ('preprocessed_tweets.pickle', 'rb') as fp:
    tweets = pickle.load(fp)
    
# List of emotions
# fear, anger, anticipation, trust, surprise, positive, negative, sadness, disgust, joy
# Assign emotion
def getEmotions():
    emotions = []
    for tweet in tweets:
        emotion = NRCLex(tweet)
        e = [item[0] for item in emotion.top_emotions] # Get emotions
        emotions.append(e)
    return emotions

def updateJsonFile():
    jsonFile = open("tweet_TR.json", "r") 
    data = json.load(jsonFile) 
    jsonFile.close()
    
    emotions = getEmotions()
    i = 0
    for tweet in tqdm(data): 
        tweet['emotions'] = emotions[i]
        i += 1

    with open("tweets_emotions.json", "w+") as jsonFile: 
        jsonFile.write(json.dumps(data))


updateJsonFile()


