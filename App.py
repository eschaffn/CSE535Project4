import json
import urllib.request, urllib.parse

aws_ip = '3.144.135.150'
corename = 'Prod_bm25'

def fetchResults(query):
    response = []
    query = query['query']
    print(query)
    q = {'q': f"{query}"}
    inurl = f'http://{aws_ip}:8983/solr/{corename}/select?defType=edismax&{urllib.parse.urlencode(q)}&qf=text_en+text_de+text_ru+tag&wt=json&indent=true&rows=10'
    data = urllib.request.urlopen(inurl)
    docs = json.load(data)['response']['docs']
    for doc in docs:
        if doc['lang'] == ['ru']:
            response.append({'Response' : doc['text_ru'].strip()})
        elif doc['lang'] == ['de']:
            response.append({'Response' : doc['text_de'].strip()})
        elif doc['lang'] == ['en']:
            response.append({'Response' : doc['text_en'].strip()})
    return(response)
