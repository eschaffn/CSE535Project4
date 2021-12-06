#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json



jsonFile = open("words_per_topic.json", "r") 
words_per_topic = json.load(jsonFile)
jsonFile.close()

# Sort lists in descending order
g = []
for k in words_per_topic.keys(): 
    l = words_per_topic[k]
    sorted_list = sorted(l, key=lambda x: x[1],reverse=True)
    g.append(sorted_list)

# Get 5 most frequent words per topic
new_g = []
for item in g:
    new_g.append(item[:5])

# Update dictionary with topics names
new_dic = {}
i = 0
for k in words_per_topic.keys():
    new_dic.update({k:new_g[i]})
    i += 1
    

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
        values, labels = getValuesLabels(new_dic[k])
        
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

