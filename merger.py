import json

all_translated_tweets = []

for i in range(1,60):
    tweetfile = open('/Users/alisalehi/PycharmProjects/MT/Translated_tweets/TR_split_'+str(i)+'.json')
    tweets = json.load(tweetfile)
    for dic in tweets:
        all_translated_tweets.append(dic)
print('final len is', len(all_translated_tweets))

j = json.dumps(all_translated_tweets)
  # for n in range(1,60):
with open('/Users/alisalehi/PycharmProjects/MT/Translated_tweets/all_translated_tweets', 'w') as f:
    f.write(j)