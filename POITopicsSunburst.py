#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def getDocs():
    jsonFile = open("tweets9_10.json", "r") 
    docs = json.load(jsonFile)
    jsonFile.close()
    return docs

def getDic1(docs):
    
    usa_pois = []
    mex_pois = []
    ind_pois = []
    
    for tweet in docs:
        if tweet['poi_name'] != '':
            if tweet['country'] == 'USA' and tweet['poi_name'] not in usa_pois:
                usa_pois.append(tweet['poi_name'])
            elif tweet['country'] == 'MEIXCO' and tweet['poi_name'] not in mex_pois:
                mex_pois.append(tweet['poi_name'])
            elif tweet['country'] == 'INDIA' and tweet['poi_name'] not in ind_pois:
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
            list_of_ids.append(k + '-' + v)
            
    #For each key in dic2, for each value in key, append key - value
    for k in Dic2.keys():
        for v in Dic2[k]:
            list_of_ids.append(k + '-' + v)
            
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
    docs = getDocs()
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
    '''
    return [{'type': 'sunburst',
  'ids': ['USA',
   'Mexico',
   'India',
   'USA - POTUS',
   'USA - SpeakerPelosi',
   'USA - SenTedCruz',
   'USA - CDCgov',
   'USA - GavinNewsom',
   'Mexico - VicenteFoxQue',
   'Mexico - Claudiashein',
   'India - MoHFW_INDIA',
   'India - narendramodi',
   'India - AmitShah',
   'India - ArvindKejriwal',
   'India - smritiirani',
   'POTUS - Non Covid Related',
   'POTUS - Covid tests',
   'POTUS - Vaccination',
   'POTUS - Coronavirus and variants',
   'POTUS - Covid cases',
   'SpeakerPelosi - Non Covid Related',
   'SpeakerPelosi - Vaccination',
   'SpeakerPelosi - Coronavirus and variants',
   'SpeakerPelosi - Covid cases',
   'SpeakerPelosi - Covid tests',
   'SenTedCruz - Non Covid Related',
   'SenTedCruz - Covid tests',
   'SenTedCruz - Vaccination',
   'SenTedCruz - Coronavirus and variants',
   'SenTedCruz - Covid cases',
   'CDCgov - Non Covid Related',
   'CDCgov - Covid cases',
   'CDCgov - Vaccination',
   'CDCgov - Covid tests',
   'CDCgov - Coronavirus and variants',
   'GavinNewsom - Non Covid Related',
   'GavinNewsom - Vaccination',
   'GavinNewsom - Covid cases',
   'GavinNewsom - Coronavirus and variants',
   'GavinNewsom - Covid tests',
   'VicenteFoxQue - Non Covid Related',
   'VicenteFoxQue - Covid tests',
   'VicenteFoxQue - Vaccination',
   'VicenteFoxQue - Coronavirus and variants',
   'Claudiashein - Non Covid Related',
   'Claudiashein - Vaccination',
   'Claudiashein - Covid tests',
   'Claudiashein - Social distance',
   'Claudiashein - Coronavirus and variants',
   'MoHFW_INDIA - Non Covid Related',
   'MoHFW_INDIA - Vaccination',
   'MoHFW_INDIA - Coronavirus and variants',
   'MoHFW_INDIA - Covid tests',
   'MoHFW_INDIA - Covid cases',
   'narendramodi - Non Covid Related',
   'narendramodi - Vaccination',
   'narendramodi - Coronavirus and variants',
   'narendramodi - Covid tests',
   'narendramodi - Covid cases',
   'AmitShah - Non Covid Related',
   'AmitShah - Covid tests',
   'AmitShah - Vaccination',
   'AmitShah - Coronavirus and variants',
   'AmitShah - Covid cases',
   'ArvindKejriwal - Non Covid Related',
   'ArvindKejriwal - Vaccination',
   'ArvindKejriwal - Covid cases',
   'ArvindKejriwal - Coronavirus and variants',
   'ArvindKejriwal - Covid tests',
   'smritiirani - Non Covid Related',
   'smritiirani - Vaccination',
   'smritiirani - Coronavirus and variants',
   'smritiirani - Covid tests'],
  'labels': ['USA',
   'Mexico',
   'India',
   'POTUS',
   'SpeakerPelosi',
   'SenTedCruz',
   'CDCgov',
   'GavinNewsom',
   'VicenteFoxQue',
   'Claudiashein',
   'MoHFW_INDIA',
   'narendramodi',
   'AmitShah',
   'ArvindKejriwal',
   'smritiirani',
   'Non Covid Related',
   'Covid tests',
   'Vaccination',
   'Coronavirus and variants',
   'Covid cases',
   'Non Covid Related',
   'Vaccination',
   'Coronavirus and variants',
   'Covid cases',
   'Covid tests',
   'Non Covid Related',
   'Covid tests',
   'Vaccination',
   'Coronavirus and variants',
   'Covid cases',
   'Non Covid Related',
   'Covid cases',
   'Vaccination',
   'Covid tests',
   'Coronavirus and variants',
   'Non Covid Related',
   'Vaccination',
   'Covid cases',
   'Coronavirus and variants',
   'Covid tests',
   'Non Covid Related',
   'Covid tests',
   'Vaccination',
   'Coronavirus and variants',
   'Non Covid Related',
   'Vaccination',
   'Covid tests',
   'Social distance',
   'Coronavirus and variants',
   'Non Covid Related',
   'Vaccination',
   'Coronavirus and variants',
   'Covid tests',
   'Covid cases',
   'Non Covid Related',
   'Vaccination',
   'Coronavirus and variants',
   'Covid tests',
   'Covid cases',
   'Non Covid Related',
   'Covid tests',
   'Vaccination',
   'Coronavirus and variants',
   'Covid cases',
   'Non Covid Related',
   'Vaccination',
   'Covid cases',
   'Coronavirus and variants',
   'Covid tests',
   'Non Covid Related',
   'Vaccination',
   'Coronavirus and variants',
   'Covid tests'],
  'parents': ['',
   '',
   '',
   'USA',
   'USA',
   'USA',
   'USA',
   'Mexico',
   'Mexico',
   'Mexico',
   'India',
   'India',
   'India',
   'India',
   'India',
   'USA - POTUS',
   'USA - POTUS',
   'USA - POTUS',
   'USA - POTUS',
   'USA - POTUS',
   'USA - SpeakerPelosi',
   'USA - SpeakerPelosi',
   'USA - SpeakerPelosi',
   'USA - SpeakerPelosi',
   'USA - SpeakerPelosi',
   'USA - SenTedCruz',
   'USA - SenTedCruz',
   'USA - SenTedCruz',
   'USA - SenTedCruz',
   'USA - SenTedCruz',
   'USA - CDCgov',
   'USA - CDCgov',
   'USA - CDCgov',
   'USA - CDCgov',
   'USA - CDCgov',
   'USA - GavinNewsom',
   'USA - GavinNewsom',
   'USA - GavinNewsom',
   'USA - GavinNewsom',
   'USA - GavinNewsom',
   'Mexico - VicenteFoxQue',
   'Mexico - VicenteFoxQue',
   'Mexico - VicenteFoxQue',
   'Mexico - VicenteFoxQue',
   'Mexico - Claudiashein',
   'Mexico - Claudiashein',
   'Mexico - Claudiashein',
   'Mexico - Claudiashein',
   'Mexico - Claudiashein',
   'India - MoHFW_INDIA',
   'India - MoHFW_INDIA',
   'India - MoHFW_INDIA',
   'India - MoHFW_INDIA',
   'India - MoHFW_INDIA',
   'India - narendramodi',
   'India - narendramodi',
   'India - narendramodi',
   'India - narendramodi',
   'India - narendramodi',
   'India - AmitShah',
   'India - AmitShah',
   'India - AmitShah',
   'India - AmitShah',
   'India - AmitShah',
   'India - ArvindKejriwal',
   'India - ArvindKejriwal',
   'India - ArvindKejriwal',
   'India - ArvindKejriwal',
   'India - ArvindKejriwal',
   'India - smritiirani',
   'India - smritiirani',
   'India - smritiirani',
   'India - smritiirani'],
  'outsidetextfont': {'size': 20, 'color': '#377eb8'},
  'leaf': {'opacity': 0.4},
  'marker': {'line': {'width': 2}}}]
  '''
