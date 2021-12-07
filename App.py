import json
import urllib.request, urllib.parse
import random 
import TopicsBarStatic
import topicsBarDynamic
import POITopicsSunburst
import emotionsPie

aws_ip = 'ec2-18-117-90-175.us-east-2.compute.amazonaws.com'
corename = 'LEMMA'

TOPIC_NAMES = {
'Covid': "rgb(21, 247, 21)",
'Covid cases and omicron': "rgb(21, 247, 240)",
'India fight corona': "rgb(247, 21, 51)",
'Hospital and medications': "rgb(247, 179, 21)",
'Tests and travel': "rgb(247, 21, 134)",
'Social distancing and masks': "rgb(247, 142, 21)",
'Covid and economy': "rgb(21, 247, 81)",
'Vaccination': "#db3236",
'Non Covid Related': "rgb(0, 0, 0)"
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
    print(response)
    return(response)

def run_plots():
    
    response = {}
    sunburst_data = POITopicsSunburst.sunburstData()
    piechart_data = emotionsPie.pieData()
    words_per_topic_data = TopicsBarStatic.wordsTopicData()

    response.update({'words_per_topic_data': words_per_topic_data})
    response.update({'sunburst_data': sunburst_data})
    response.update({'piechart_data': piechart_data})

    print(response)
    return response
