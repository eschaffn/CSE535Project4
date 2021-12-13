import numpy as np
import pandas as pd
import csv
import demoji
import re
import json
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
nltk.download('stopwords')
nltk.download('punkt')

def clean_text(df,input_list=False):
    all_reviews = list()
    if input_list:
        lines = df
    else:
        lines = df["text_en"].values.tolist()
    for text in lines:
        text = text.lower()
        pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        text = pattern.sub('', text)
        text = re.sub(r"[,.\"!@#$%^&*(){}?/;`~:<>+=-]", "", text)
        text = re.sub('^rt ', ' ', text)  # remove 'rt'
        text = re.sub('\n', ' ', text)  # remove '\n'
        text = re.sub('[0-9]+', ' ', text)  # remove numbers
        text = re.sub('\s+', ' ', text)  # remove extra whitespaces
        text = re.sub('^\s+', '', text)  # remove space(s) at start
        text = re.sub('\s+$', '', text)  # remove space(s) at end
        tokens = word_tokenize(text)
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in tokens]
        words = [word for word in stripped if word.isalpha()]
        stop_words = set(stopwords.words("english"))
        stop_words.discard("not")
        PS = PorterStemmer()
        words = [PS.stem(w) for w in words if not w in stop_words]
        words = ' '.join(words)
        all_reviews.append(words)
    return all_reviews

a1 = open('/Users/alisalehi/PycharmProjects/MT/TFIDFCOSINE/all_TR_50638_Topics.json')
all_tweets = json.load(a1)

sc = open('/Users/alisalehi/PycharmProjects/MT/TFIDFCOSINE/FinalJJ_scored_2664.json')
manuscored = json.load(sc)


#extracting tweets related to the list below
vaxrel = ['vaccine','vaccination','vaxx','vaxxer','pfizer', 'moderna', 'johnson', 'j&j', 'astrazeneca', 'sputnik', 'booster', 'dose', 'vaccinated', 'unvaccinated','vaccinehesitancy']
kw_tweets = []
for tweet in all_tweets:
    for item in vaxrel:
        if item in tweet['text_en']:
            kw_tweets.append(tweet)
            break
print('len of keyword related',len(kw_tweets)) #6906
print(kw_tweets[0])

ids = []
filtered =[]
for dic1 in kw_tweets:
    dic2 = {}
    dic2['id'] = dic1['id']
    dic2['text_en'] = dic1['text_en']
    dic2['Stance'] = ''
    filtered.append(dic2)
    # ids.append(dic1['id'])
print('len of columns filtered',len(filtered))


#extracting the scored ones and add all to a list
all_scored = []
for tw in manuscored:
    if tw['Stance'] == '1':
        all_scored.append(tw)
for tw in manuscored:
    if tw['Stance'] == '0':
        all_scored.append(tw)
for tw in manuscored:
    if tw['Stance'] == '-1':
        all_scored.append(tw)

print('len of allscored' ,len(all_scored)) #737

# print([t2['id'] for t2 in all_scored])

noscores_kw_tweets = []
for t1 in filtered:
    if int(t1['id']) not in [int(t2['id']) for t2 in all_scored]:
    # if t1['text_en'] == [t2['text_en'] for t2 in all_scored]:
        noscores_kw_tweets.append(t1)
        ids.append(t1['id'])
print('len of noscores_kw_tweets',len(noscores_kw_tweets))
total = all_scored+noscores_kw_tweets
print('len of total', len(total))
print('this', all_scored[238] ,total[238])
#1--237 0--479  -1--21   ''--6485
# test = []
# for i in total:
#     if i['Stance'] == '':
#         test.append(i)
# print(len(test))


# #extracting tex_en
all_txten = []
for twt in total:
    all_txten.append(twt['text_en'])
print('alltxten',len(all_txten))
print(all_txten[0])
clean = clean_text(all_txten, input_list=True)
print(clean[0])
#
print(len(clean))
# #
from sklearn.feature_extraction.text import TfidfVectorizer
TV1 = TfidfVectorizer(min_df=5)
allvec = TV1.fit_transform(clean).toarray()
# print(type(allvec))
print(allvec.shape) #(7195, 4054)
# # #
from sklearn.metrics.pairwise import cosine_similarity,cosine_distances
#
cs_sim = cosine_similarity(allvec)
print(cs_sim.shape)
pro_sim = cs_sim[0:237, 737:].max(axis =0)
print(pro_sim.shape)
print(pro_sim)
# # # #
neut_sim = cs_sim[237:479, 737:].max(axis = 0)
print(neut_sim)
# # # #
against_sim = cs_sim[479:737, 737:].max(axis=0)
print(against_sim)

for i in range(0,len(ids)):
    max = np.argmax([pro_sim[i],neut_sim[i],against_sim[i]])
    if max == 0:
        st = 'pro'
    elif max == 1:
        st = 'neutral'
    else:
        st = 'against'
    for tweet in total[737:]:
        if int(tweet['id']) == int(ids[i]):
            tweet['Stance'] = st
            break
        # elif tweet['Stance'] == '1':
        #     tweet['Stance'] = 'pro'
        # elif tweet['Stance'] == '0':
        #     tweet['Stance'] = 'neutral'
        # elif tweet['Stance'] == '-1':
        #     tweet['Stance'] = 'against'
for tweet in total[:737]:
    if tweet['Stance'] == '1':
        tweet['Stance'] = 'pro'
    elif tweet['Stance'] == '0':
        tweet['Stance'] = 'neutral'
    elif tweet['Stance'] == '-1':
        tweet['Stance'] = 'against'

n = json.dumps(total)
stadded = open('/Users/alisalehi/PycharmProjects/MT/TFIDFCOSINE/stance5_added_7195_mean.json', 'w')
stadded.write(n)
