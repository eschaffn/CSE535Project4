#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

jsonFile = open("tweets9_10.json", "r") 
data = json.load(jsonFile) 
jsonFile.close()


COLORS = {
1: '#4885ed',
2: "#db3236",
3: "f4c20d",
4: "4885ed",
5: "3cba54",
6: '#4885ed',
7: "#db3236",
8: "f4c20d"
}
# Docs is the list of results from the search
# I'm assuming it's a list of dictionaries just like data

def getTopics(docs):
    all_topics = []
    for tweet in docs:
        all_topics.append(tweet['topic'])
    return all_topics

def getLabels(docs):
    labels = []
    for tweet in docs:
        t = tweet['topic']
        if t not in labels:
            labels.append(t)
    return labels

def getValues(topic, docs):
    value = 0
    all_topics = getTopics(docs)
    for t in all_topics:
        if t == topic:
            value += 1        
    return value

def barData(docs):
    labels = getLabels(docs)
    values = []
    colors = []
    n = 1
    for l in labels:
        val = getValues(l, docs)
        values.append(val)
        colors.append(COLORS[n])
        n+=1
    data = [{
        'x': labels,
        'y': values,
        'type': 'bar',
        'marker': {
            'color': colors
        }
    }]

    return data