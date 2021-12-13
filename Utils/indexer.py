import os
import pysolr
import json
import requests
# import tagger
from tqdm import tqdm



CORE_NAME = "LEMMA"
AWS_IP = 'ec2-3-144-132-249.us-east-2.compute.amazonaws.com'


# [CAUTION] :: Run this script once, i.e. during core creation

def delete_core(core=CORE_NAME):
    print(os.system('sudo su - solr -c "/opt/solr/bin/solr delete -c {core}"'.format(core=core)))

def create_core(core=CORE_NAME):
    print(os.system(
        'sudo su - solr -c "/opt/solr/bin/solr create -c {core} -n data_driven_schema_configs"'.format(
            core=core)))

def docSplitter(doc):
    q = f"{doc[4:]}".strip()
    return doc[0:3], q

class Indexer:
    def __init__(self):
        self.solr_url = f'http://{AWS_IP}:8983/solr/'
        self.connection = pysolr.Solr(self.solr_url + CORE_NAME, always_commit=True, timeout=5000000)

    def create_documents(self, docs):
        # tags = tagger.tagger(docs)
        # docs.update({'tag': tags})
        self.connection.add(docs)

    def clear_index(self):
        print(self.connection.delete(q='*:*'))
    
    def add_fields(self):
        '''
        Define all the fields that are to be indexed in the core. Refer to the project doc for more details
        :return:
        '''
        data = {
            "add-field": [
                # {
                #     "name": "id",
                #     "type": "string",
                #     "multiValued": False
                # },
                # {
                #     "name": "is_retweet",
                #     "type": "boolean",
                #     "multiValued": False
                # },
                # {
                #     "name": "num_retweets",
                #     "type": "plong",
                #     "multiValued": False,
                #     "docValues": True
                # },
                # {
                #     "name": "num_likes",
                #     "type": "plong",
                #     "multiValued": False,
                #     "docValues": True
                # },
                # {
                #     "name": "emotions",
                #     "type": "string",
                #     "multiValued": True
                # },
                # {
                #     "name": "topic",
                #     "type": "string",
                #     "multiValued": False
                # },
                # {
                #     "name": "sentiment",
                #     "type": "string",
                #     "multiValued": False
                # },
                {
                    "name": "tweet_rank",
                    "type": "plong",
                    "multiValued": False
                }



                # {
                #     "name": "country",
                #     "type": "string",
                #     "multiValued": False
                # },
                # {
                #     "name": "tweet_lang",
                #     "type": "string",
                #     "multiValued": False
                # },
                # {
                #     "name": "tweet_text",
                #     "type": "text_general",
                #     "multiValued": False
                # },
                # {
                #     "name": "text_en",
                #     "type": "text_en",
                #     "multiValued": False
                # },
                # {
                #     "name": "text_es",
                #     "type": "text_es",
                #     "multiValued": False
                # },
                # {
                #     "name": "text_hi",
                #     "type": "text_hi",
                #     "multiValued": False
                # },
                # {
                #     "name": "tweet_date",
                #     "type": "pdate",
                #     "docValues": "true",
                #     "multiValued": False
                # },
                # {
                #     "name": "verified",
                #     "type": "boolean",
                #     "multiValued": False
                # },
                # {
                #     "name": "poi_id",
                #     "type": "plong",
                #     "docValues": "true",
                #     "multiValued": False
                # },
                # {
                #     "name": "poi_name",
                #     "type": "string",
                #     "multiValued": False
                # },
                # {
                #     "name": "replied_to_tweet_id",
                #     "type": "plong",
                #     "docValues": "true",
                #     "multiValued": False
                # },
                # {
                #     "name": "replied_to_user_id",
                #     "type": "plong",
                #     "docValues": "true",
                #     "multiValued": False
                # },
                # {
                #     "name": "reply_text",
                #     "type": "text_general",
                #     "multiValued": False
                # },
                # {
                #     "name": "hashtags",
                #     "type": "string",
                #     "multiValued": True
                # },
                # {
                #     "name": "mentions",
                #     "type": "string",
                #     "multiValued": True
                # },
                # {
                #     "name": "tweet_urls",
                #     "type": "string",
                #     "multiValued": True
                # },
                # {
                #     "name": "tweet_emoticons",
                #     "type": "string",
                #     "multiValued": True
                # },
                # {
                #     "name": "geolocation",
                #     "type": "string",
                #     "multiValued": True
                # },
                # {
                #     "name": "username",
                #     "type": "string",
                #     "multiValued": False
                # }
                
            ]

        }
        print(requests.post(self.solr_url + CORE_NAME + "/schema", json=data).json())


docs = 'tweets6.json'
# delete_core()
# create_core()
indexer = Indexer()
indexer.clear_index()
indexer.add_fields()
# tagger.add_tags()
# indexer.replace_fields()
# indexer.set_VSM()
with open(docs, 'r') as f:
    data = json.load(f)
    print('Indexing Documents...')
    for line in tqdm(data):
        indexer.create_documents(line)


