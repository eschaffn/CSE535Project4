import os
import json

# with open ('tweets.json','r', encoding='utf-8') as f1:
#     for line in f1.readlines():
#         print(type(line.strip()))

tweetfile = open('tweets.json','r', encoding='utf-8')
tweets = json.load(tweetfile)
# print(len(tweets))
# print(type(tweets))
# for tweet in tweets:
#     print(tweet)
#     # print(len(tweet))
#     print(type(tweet))

    #print the total length size of the json file
print(f'length of tweets',len(tweets))

    # #getting splits of 6000 tweets
size_of_the_split=800
total = len(tweets)//size_of_the_split
    #
print(f'number of splits',total+1)#printing the number of the splits
    #
for i in range(total+1):
    json.dump(tweets[i*size_of_the_split:(i+1)*size_of_the_split], open('twitter_data_split'+str(i+1)+'.json','w', encoding='utf8'), ensure_ascii=False, indent=True)