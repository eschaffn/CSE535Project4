#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

jsonFile = open("tweets_emoSentTopics.json", "r") 
data = json.load(jsonFile) 
jsonFile.close()

# Docs is the list of results from the search
# I'm assuming it's a list of dictionaries just like data

def getTopics(docs):
    all_topics = []
    for tweet in docs:
        topics_list = tweet['topic']
        for t in topics_list:
            all_topics.append(t)
    return all_topics

def getLabels():
    labels = []
    for tweet in data:
        topics_list = tweet['topic']
        for t in topics_list:
            if t not in labels:
                labels.append(t)
    return labels

def getValues(topic):
    value = 0
    all_topics = getTopics()
    for t in all_topics:
        if t == topic:
            value += 1        
    return value

def barData():
    labels = getLabels()
    values = []
    for l in labels:
        val = getValues(l)
        values.append(val)
        
    data = [{
        'x': lables,
        'y': values,
        'type': 'bar'
    }]

    return data