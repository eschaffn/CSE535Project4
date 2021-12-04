#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

jsonFile = open("tweets_emoSent.json", "r") 
data = json.load(jsonFile) 
jsonFile.close()

# Update emotions (merge anticipation and anticip)
for tweet in data:
    emotions_list = tweet['emotions']
    for e in emotions_list:
        if e == 'anticip':
            emotions_list.remove(e)
            emotions_list.append('anticipation')

# Update json file (merge anticipation and anticip)
def updateJsonFile():
    for tweet in data:
        emotions_list = tweet['emotions']
        for e in emotions_list:
            if e == 'anticip':
                emotions_list.remove(e)
                emotions_list.append('anticipation')
            

    with open("tweets_emoSent2.json", "w+") as jsonFile: 
        jsonFile.write(json.dumps(data))

updateJsonFile()


jsonFile = open("tweets_emoSent2.json", "r") 
data = json.load(jsonFile) 
jsonFile.close()

def getEmotions():
    all_emotions = []
    for tweet in data:
        emotions_list = tweet['emotions']
        for e in emotions_list:
            all_emotions.append(e)
    return all_emotions

def getLabels():
    labels = []
    for tweet in data:
        emotions_list = tweet['emotions']
        for e in emotions_list:
            if e not in labels:
                labels.append(e)
    return labels

def getValues(emotion):
    value = 0
    all_emotions = getEmotions()
    for e in all_emotions:
        if e == emotion:
            value += 1        
    return value

def pieData():
    labels = getLabels()
    values = []
    for emotion in labels:
        val = getValues(emotion)
        values.append(val)
        
    data = [{
        'values': values,
        'labels': labels,
        'type': 'pie'
    }]
    layout = {
        'height': 400,
        'width': 500
    }

    return data, layout

