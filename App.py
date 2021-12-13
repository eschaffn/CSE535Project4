import json
import urllib.request, urllib.parse
import random 
import TopicsBarStatic
import topicsBarDynamic
import POITopicsSunburst3
import emotionsPie
import bubblechart

aws_ip = 'ec2-18-188-22-27.us-east-2.compute.amazonaws.com'
corename = 'LEMMA'

TOPIC_NAMES = {
'1_Corona_Masks_Government': "rgb(21, 247, 21)",
'2_Immunity_Positive_South_Africa': "rgb(21, 247, 240)",
'3_Hospital_Health': "rgb(247, 21, 51)",
'4_Coronavirus': "rgb(247, 179, 21)",
'5_India_Covid_Cases': "rgb(247, 21, 134)",
'6_Omicron_Variant': "rgb(247, 142, 21)",
'7_Symptoms_Lockdown': "rgb(21, 247, 81)",
'8_Travel_Quarantine': "#db3236",
'9_Social_Distance': "rgb(0, 0, 0)",
'10_Covid_Vaccination': "rgb(0,0,0)",
'Non_Covid': "rgb(56, 56, 56)"
}


class Node:
    def __init__(self, label):
        self.label = label
        self.val = label['tweet_rank'] * label['score']
        self.next = None


class LinkedList:
    def __init__(self):
        self.start = None
        self.end = None

    def insert_sorted(self, n):
        if self.start:
            if n.val >= self.start.val:
                n.next = self.start
                self.start = n
            elif n.val <= self.end.val:
                self.end.next = n
                self.end = n
            else:
                m = self.start

                while m.next.val > n.val:
                    m = m.next

                n.next = m.next
                m.next = n
        else:
            self.start = n
            self.end = n

    def traverse(self):
        n = self.start
        out = []

        while n:
            out.append(n.label)
            n = n.next

        return out

def format_text(user, body, topic):
    out = "@" + user + ": <br><br>\'\'\'"
    start = 0
    end = 120
    stop = False

    while not stop:
        while end < len(body) and not body[end].isspace():
            end += 1

        stop = end >= len(body)
        out += body[start:end].strip()

        if stop:
            out += "\'\'\'"
        else:
            start = end
            end += 120

        out += "<br>"

    return out + "<br>TOPIC: " + topic


def fetchResults(data):

    response = []

    query = data['query']
    RTfilterparams = data['RTfilterparams']
    langfilterparams = data['langfilterparams']

    q = {'q': f"{query}"}

    if RTfilterparams == 'True':
        q = q 
    else:
        q['q'] +=  "-is_retweet:true"

    inurl = f'http://{aws_ip}:8983/solr/{corename}/select?defType=edismax&{urllib.parse.urlencode(q)}&fl=*%2Cscore&qf=text_en+text_hi+text_es&wt=json&indent=true&rows=20'
    print(inurl)

    data = urllib.request.urlopen(inurl)
    docs = json.load(data)['response']['docs']
    sort_list = LinkedList()

    for d in docs:
        sort_list.insert_sorted(Node(d))

    docs = sort_list.traverse()

    for doc in docs:
        if langfilterparams == 'es':
            response.append(
                {'Response' : 
                    {'text': doc['text_es'].strip(),
                    'original_text': doc['tweet_text'],
                    'map_text': format_text(doc['username'], doc['text_es'], doc['topic']),
                    'username': doc['username'], 
                    'tweet_url': f'https://twitter.com/{doc["username"]}/status/{doc["id"]}',
                    # 'lon': random.randint(1, 150),
                    # 'lat': random.randint(1, 150),
                    'lon': float(doc['geolocation'][0]) if doc['geolocation'] != [""] else 10000,
                    'lat': float(doc['geolocation'][1]) if doc['geolocation'] != [""] else 10000,
                    'topics': doc['topic'] if 'topic' in doc else '',
                    'colors': TOPIC_NAMES[doc['topic']] if 'topic' in doc else '',
                    'emotion': doc['emotions'] if 'emotions' in doc else '',
                    'num_likes': doc['num_likes'],
                    'num_retweets': doc['num_retweets'],
                    'solr_score': doc['score'],
                    'tweet_rank': doc['tweet_rank'],
                    # 'topic_bar_data': topicsBarDynamic.barData(docs),
                    'sentiment': doc['sentiment']
                }})        
        elif langfilterparams == 'hi':
            response.append(
                {'Response' : 
                    {'text': doc['text_hi'].strip(), 
                    'original_text': doc['tweet_text'],
                    'map_text': format_text(doc['username'], doc['text_hi'], doc['topic']),
                    'username': doc['username'], 
                    'tweet_url': f'https://twitter.com/{doc["username"]}/status/{doc["id"]}',
                    # 'lon': random.randint(1, 150),
                    # 'lat': random.randint(1, 150),
                    'lon': float(doc['geolocation'][0]) if doc['geolocation'] != [""] else 10000,
                    'lat': float(doc['geolocation'][1]) if doc['geolocation'] != [""] else 10000,
                    'topics': doc['topic'] if 'topic' in doc else '',
                    'colors': TOPIC_NAMES[doc['topic']] if 'topic' in doc else '',
                    'emotion': doc['emotions'] if 'emotions' in doc else '',
                    'num_likes': doc['num_likes'],
                    'num_retweets': doc['num_retweets'],
                    'solr_score': doc['score'],
                    'tweet_rank': doc['tweet_rank'],
                    # 'topic_bar_data': topicsBarDynamic.barData(docs),
                    'sentiment': doc['sentiment']
                }})        
        elif langfilterparams == 'en':
            response.append(
                {'Response' : 
                    {'text': doc['text_en'].strip(),
                    'original_text': doc['tweet_text'],
                    'map_text': format_text(doc['username'], doc['text_en'], doc['topic']),
                    'username': doc['username'], 
                    'tweet_url': f'https://twitter.com/{doc["username"]}/status/{doc["id"]}',
                    # 'lon': random.randint(1, 150),
                    # 'lat': random.randint(1, 150),
                    'lon': float(doc['geolocation'][0]) if doc['geolocation'] != [""] else 10000,
                    'lat': float(doc['geolocation'][1]) if doc['geolocation'] != [""] else 10000,
                    'topics': doc['topic'] if 'topic' in doc else '',
                    'colors': TOPIC_NAMES[doc['topic']] if 'topic' in doc else '',
                    'emotion': doc['emotions'] if 'emotions' in doc else '',
                    'num_likes': doc['num_likes'],
                    'num_retweets': doc['num_retweets'],
                    'solr_score': doc['score'],
                    'tweet_rank': doc['tweet_rank'],
                    # 'topic_bar_data': topicsBarDynamic.barData(docs),
                    'sentiment': doc['sentiment']
                }})
        else:
            response.append(
                {'Response' : 
                    {'text': doc['tweet_text'].strip(), 
                    'original_text': doc['tweet_text'],
                    'map_text': format_text(doc['username'], doc['tweet_text'], doc['topic']),
                    'username': doc['username'], 
                    'tweet_url': f'https://twitter.com/{doc["username"]}/status/{doc["id"]}',
                    # 'lon': random.randint(1, 150),
                    # 'lat': random.randint(1, 150),
                    'lon': float(doc['geolocation'][0]) if doc['geolocation'] != [""] else 10000,
                    'lat': float(doc['geolocation'][1]) if doc['geolocation'] != [""] else 10000,
                    'topics': doc['topic'] if 'topic' in doc else '',
                    'colors': TOPIC_NAMES[doc['topic']] if 'topic' in doc else '',
                    'emotion': doc['emotions'] if 'emotions' in doc else '',
                    'num_likes': doc['num_likes'],
                    'num_retweets': doc['num_retweets'],
                    'solr_score': doc['score'],
                    'tweet_rank': doc['tweet_rank'],
                    # 'topic_bar_data': topicsBarDynamic.barData(docs),
                    'sentiment': doc['sentiment']
                    }})
    response.append({'topic_bar_data': topicsBarDynamic.barData(docs)})

    print('-'*20)
    print(f'A user searched for: {query}')
    print(f'Search Returning {len(response)-1} Results')
    print('-' *20)

    return(response)

def run_plots():
    response = {}
    sunburst_data = POITopicsSunburst3.sunburstData()
    piechart_data = emotionsPie.pieData()
    words_per_topic_data = TopicsBarStatic.wordsTopicData()
    bubblechart_data = bubblechart.bubblechartData()

    response.update({'words_per_topic_data': words_per_topic_data})
    response.update({'sunburst_data': sunburst_data})
    response.update({'piechart_data': piechart_data})
    response.update({'bubblechart_data': bubblechart_data})

    return response
