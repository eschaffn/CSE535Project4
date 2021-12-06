#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json



jsonFile = open("words_per_topic.json", "r") 
words_per_topic = json.load(jsonFile)
jsonFile.close()


def getValuesLabels(k):
    labels = []
    values = []
    for pair in k:
        labels.append(pair[0])
        values.append(pair[1])
    
        
    return values, labels



def wordsTopicData():
    data = {}
    
    for k in words_per_topic.keys():
        values, labels = getValuesLabels(words_per_topic[k])
        
        d = {
        'type': 'bar',
        'x': values,
        'y': labels,
        'orientation': 'h'
        }
        
        d_name = 'data_words_per_topics_' + k
        
        data.update({d_name:d})
    
    return data


wordsTopicData()