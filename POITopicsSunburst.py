#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

jsonFile = open("tweets_emoSentTopics2.json", "r") 
docs = json.load(jsonFile)
jsonFile.close()

'''
# Dic1 = {“Country”:[list_of_pois],“Country”:[list_of_pois],“Country”:[list_of_pois]}

Dic1 = {"USA": ["POTUS", "SpeakerPelosi", "SenTedCruz", "CDCgov", "GavinNewsom"], 
"Mexico": ["SSalud_mx", "VicenteFoxQue", "lopezobrador_", "Claudiashein", "caroviggiano"], 
"India": ["MoHFW_INDIA","narendramodi", "AmitShah", "ArvindKejriwal", "smritiirani"]}
'''
'''
# Dic2 = {“POI”:[list_of_topics],…,“POI”:[list_of_topics]}

Dic2 = {
"POTUS": ["Topic1", "Topic2", "Topic3"],
"”SpeakerPelosi": [], 
"SenTedCruz": [], 
"CDCgov": [],
"SSalud_mx": [], 
"VicenteFoxQue": [], 
"“lopezobrador_": [], 
"Claudiashein": [], 
"“caroviggiano": [],
"MoHFW_INDIA": [],
"narendramodi": [], 
"AmitShah": [], 
"ArvindKejriwal": [], 
"smritiirani": []}
'''

def getDic1(docs):
    
    usa_pois = []
    mex_pois = []
    ind_pois = []
    
    for tweet in docs:
        if tweet['poi_name'] != '':
            if tweet['country'] == 'USA' and tweet['poi_name'] not in usa_pois:
                usa_pois.append(tweet['poi_name'])
            elif tweet['country'] == 'Mexico' and tweet['poi_name'] not in mex_pois:
                mex_pois.append(tweet['poi_name'])
            elif tweet['country'] == 'India' and tweet['poi_name'] not in ind_pois:
                ind_pois.append(tweet['poi_name'])
    
    Dic1 = {"USA": usa_pois,
            "Mexico": mex_pois,
            "India": ind_pois,
            }
        
    return Dic1

def getDic2(docs, Dic1):
    Dic2 = {}
    for k in Dic1.keys():
        # for each poi
        for v in Dic1[k]:
            topics = []
            # get topics for v
            # check each tweet
            for tweet in docs:
                # if tweet is from poi
                if tweet['poi_name'] == v:
                    # get topics
                    if tweet['topic'] not in topics:
                        topics.append(tweet['topic'])
                    
            Dic2[v] = topics
        
    return Dic2

def getIds(Dic1,Dic2):
    list_of_ids = []
    #For each key in Dic1, append key
    for k in Dic1.keys():
        list_of_ids.append(k)
        
    #For each key in dic1, for each value in key, append key - value
    for k in Dic1.keys():
        for v in Dic1[k]:
            list_of_ids.append(k + ' - ' + v)
            
    #For each key in dic2, for each value in key, append key - value
    for k in Dic2.keys():
        for v in Dic2[k]:
            list_of_ids.append(k + ' - ' + v)
            
    return list_of_ids


def getLabels(Dic1,Dic2):
    list_of_labels = []
    
    # inner_labels: for each key in Dic1, append key
    for k in Dic1.keys():
        list_of_labels.append(k) 
    
    # middle_labels: for each key in Dic1, append values
    for k in Dic1.keys():
        for v in Dic1[k]:
            list_of_labels.append(v)
            
    # outer_labels: for each key in Dic2, append values
    for k in Dic2.keys():
        for v in Dic2[k]:
            list_of_labels.append(v)

    return list_of_labels

def getParents(Dic1,Dic2):
    
    list_of_parents = []
    
    # Append “” x len(dic1) (num of countries)
    numCountries = len(Dic1)
    i = 0
    while i < numCountries:
        list_of_parents.append('')
        i += 1
    
    #For each key in dic1, Append key x len(dic1[‘key’]) 
    #(for each country, append country x number of pois per country)
    for k in Dic1.keys():
        numPOIS = len(Dic1[k])
        i = 0
        while i < numPOIS:
            list_of_parents.append(k)
            i += 1

    #For each key in dic1, (for each country) 
    for k in Dic1.keys():
        #for each poi in each country
        for v in Dic1[k]:
            # append poi x number of topics of that poi
            for t in Dic2.keys():
                if t == v:
                    numTopics = len(Dic2[t])
            i = 0
            while i < numTopics:
                list_of_parents.append(k + ' - ' + v)
                i += 1
  
    return list_of_parents

def sunburstData():
    Dic1 = getDic1(docs)
    Dic2 = getDic2(docs,Dic1)

    list_of_ids = getIds(Dic1,Dic2)
    list_of_labels = getLabels(Dic1,Dic2)
    list_of_parents = getParents(Dic1,Dic2)
    
    data = [{
        'type': 'sunburst',
        'ids': list_of_ids,
        'labels': list_of_labels,
        'parents': list_of_parents,
        'outsidetextfont': {'size': 20, 'color': "#377eb8"},
        'leaf': {'opacity': 0.4},
        'marker': {'line': {'width': 2}} 
        }]    


    return data