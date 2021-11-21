'''
@author: Souvik Das
Institute: University at Buffalo
'''

import tweepy
import collect_tweets
from collect_tweets import TWPreprocessor
import time


class Twitter:
    def __init__(self):
        self.auth = tweepy.OAuthHandler("RKrvceYrnetnnt5PwL58Z11kY", "91RrDqUdFDIRoaBudGORMOpxIOmL50ZCikjmVvr1XFKu5xiHE4")  # (api, api secret)
        self.auth.set_access_token("1432453295205933056-Okv9mWvgbQqHFDXLL0hBfdg7iORZpa", "Zu0GKD33ilc2RSRF3x8XEddT0c9E2FDsflDsJDfn6EkG5")  # (access, access secret)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    @staticmethod
    def meet_basic_tweet_requirements(tw, ln, key):
        '''
        Add basic tweet requirements logic, like language, country, covid type etc.
        :return: boolean
        '''
        meets_req = 0
        hashtags = []

        pp_tw = TWPreprocessor.preprocess(tw)

        if pp_tw['id'] in collect_tweets.tweet_ids:
            return False

        for h in pp_tw['hashtags']:
            hashtags.append(h.encode("utf-8").lower())

        text_obj = tw.full_text
        text = text_obj.encode("utf-8").lower().split()

        for i in range(len(key)):
            k_text = key[i]["name"]

            if k_text.encode("utf-8") in hashtags + text:
                meets_req = 1
                break

        if not(ln == "") & meets_req == 1:
            if not(tw.lang == ln):
                meets_req = 0

        return meets_req == 1

    def get_tweets_by_poi_screen_name(self, poi, multi):
        '''
        Use user_timeline api to fetch POI related tweets, some postprocessing may be required.
        :return: List
        '''
        tweets = None
        rate = 2
        collecting = True

        while collecting:
            collecting = False

            try:
                if multi:
                    tweets = self.api.user_timeline(poi["screen_name"], count=poi["count"], tweet_mode='extended', max_id=multi.id)
                else:
                    tweets = self.api.user_timeline(poi["screen_name"], count=poi["count"], tweet_mode='extended')
            except Exception:
                print("\nTweet collection error. Trying again...")
                time.sleep(rate)
                rate *= 2
                collecting = True

        return tweets

    def get_tweets_by_lang_and_keyword(self, key, multi):
        '''
        Use search api to fetch keywords and language related tweets, use tweepy Cursor.
        :return: List
        '''
        tweets = None
        rate = 2
        collecting = True

        while collecting:
            collecting = False

            try:
                if multi:
                    tweets = self.api.search(key, tweet_mode='extended', max_id=multi.id)
                else:
                    tweets = self.api.search(key, tweet_mode='extended')
            except Exception:
                print("\nTweet collection error. Trying again...")
                time.sleep(rate)
                rate *= 2
                collecting = True

        return tweets

    def get_replies(self, tw, last_rep):
        '''
        Get replies for a particular tweet_id, use max_id and since_id.
        For more info: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/guides/working-with-timelines
        :return: List
        '''
        name = tw['username']
        replies = []
        m_id = tw['id']

        if not last_rep['id'] == tw['id']:
            m_id = last_rep['id']

        rate = 2
        collecting = True

        while collecting:
            collecting = False

            try:
                for page in tweepy.Cursor(self.api.search, q='to:' + name, tweet_mode='extended', result_type='recent', since_id=m_id, timeout=999999).pages(10):
                    for tweet in page:
                        if hasattr(tweet, 'in_reply_to_status_id_str'):
                            if tweet.in_reply_to_status_id_str == str(tw['id']) and not tweet.user.id == tw['user_id']:
                                replies.append(tweet)
            except Exception:
                print("\nTweet collection error. Trying again...")
                time.sleep(rate)
                rate *= 2
                collecting = True

        return replies
