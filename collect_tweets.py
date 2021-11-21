import json
import demoji
import datetime
import preprocessor
import twitter_interface


poi_ids = []
tweet_ids = []
keywords = []
pois = []


class Node:
    def __init__(self, ins):
        self.item = ins
        self.value = ins['id']
        self.next = None


class LinkedList:
    def __init__(self):
        self.start = None
        self.end = None

    def insert_sorted(self, ins):
        node = Node(ins)

        if self.start:
            if self.start.value < node.value:
                node.next = self.start
                self.start = node
            elif self.end.value > node.value:
                self.end.next = node
                self.end = node
            else:
                n = self.start

                while n.next.value > node.value:
                    n = n.next

                node.next = n.next
                n.next = node
        else:
            self.start = node
            self.end = node

    def traverse(self):
        n = self.start
        trv = []

        while n:
            trv.append(n.item)
            n = n.next

        return trv

class TWPreprocessor:
    @classmethod
    def preprocess(cls, tweet):
        '''
        Do tweet pre-processing before indexing, make sure all the field data types are in the format as asked in the project doc.
        :param tweet:
        :return: dict
        '''
        tw = tweet._json

        return {
            "poi_name": tweet.user.screen_name if tweet.user.screen_name in poi_ids else "",
            "username": tweet.user.screen_name,
            "out_links": "",
            "reply_to": tweet.in_reply_to_status_id_str if hasattr(tweet, 'in_reply_to_status_id_str') else "",
            "poi_id": tweet.user.id if tweet.user.screen_name in poi_ids else "",
            "user_id": tweet.user.id,
            "retweet": tweet.retweeted_status.id_str if hasattr(tweet, 'retweeted_status') else "",
            "quote_tweet": str(tweet.quoted_status_id) if hasattr(tweet, 'quoted_status_id') else "",
            "verified": tweet.user.verified,
            "country": "INDIA" if tweet.lang == "hi" else ("MEXICO" if tweet.lang == "es" else "USA"),
            "id": tweet.id,
            "replied_to_tweet_id": tweet.in_reply_to_status_id,
            "replied_to_user_id": tweet.in_reply_to_user_id,
            "reply_text": tweet.in_reply_to_status_id_str,
            "tweet_text": tweet.full_text,
            "tweet_lang": tweet.lang,
            "text_hi": tweet.full_text if tweet.lang == "hi" else "",
            "text_es": tweet.full_text if tweet.lang == "es" else "",
            "text_en": tweet.full_text if tweet.lang == "en" else "",
            "hashtags": _get_entities(tw, type="hashtags"),
            "mentions": _get_entities(tw, type="mentions"),
            "tweet_urls": _get_entities(tw, type="urls"),
            "tweet_emoticons": _text_cleaner(tweet.full_text)[1],
            "tweet_date": datetime.datetime.strftime(_get_tweet_date(tw["created_at"]), "%a %b %d %H:%M:%S +0000 %Y"),
            "geolocation": tweet._json['geo']['coordinates'] if tweet.geo else ""
        }


def _get_entities(tweet, type=None):
    result = []
    if type == 'hashtags':
        hashtags = tweet['entities']['hashtags']

        for hashtag in hashtags:
            result.append(hashtag['text'])
    elif type == 'mentions':
        mentions = tweet['entities']['user_mentions']

        for mention in mentions:
            result.append(mention['screen_name'])
    elif type == 'urls':
        urls = tweet['entities']['urls']

        for url in urls:
            result.append(url['url'])

    return result


def _text_cleaner(text):
    emoticons_happy = list([
        ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
        ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
        '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
        'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
        '<3'
    ])
    emoticons_sad = list([
        ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
        ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
        ':c', ':{', '>:\\', ';('
    ])
    all_emoticons = emoticons_happy + emoticons_sad

    emojis = list(demoji.findall(text).keys())
    clean_text = demoji.replace(text, '')

    for emo in all_emoticons:
        if emo in clean_text:
            clean_text = clean_text.replace(emo, '')
            emojis.append(emo)

    clean_text = preprocessor.clean(text)
    # preprocessor.set_options(preprocessor.OPT.EMOJI, preprocessor.OPT.SMILEY)
    # emojis= preprocessor.parse(text)

    return clean_text, emojis


def _get_tweet_date(tweet_date):
    return _hour_rounder(datetime.datetime.strptime(tweet_date, '%a %b %d %H:%M:%S +0000 %Y'))


def _hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
            + datetime.timedelta(hours=t.minute // 30))


def finished_poi_replies(in_list):
    out_done = 0
    out_not_done = []

    for i in range(len(in_list)):
        if in_list[i] >= 10:
            out_done += 1
        else:
            out_not_done.append(i)

    return out_done, out_not_done


def rt(tweet):
    return not tweet['retweet'] + tweet['quote_tweet'] == ""


def get_poi_replies(in_tweets):
    sort_list = LinkedList()

    for x in in_tweets:
        sort_list.insert_sorted(x)

    poi_tweets = sort_list.traverse()
    pages = [[]]
    p_i = 0

    for k in range(len(poi_tweets)):
        pages[p_i].append(poi_tweets[k])

        if len(pages[p_i]) == 50:
            pages.append([])
            p_i += 1

    poi_reps = []

    for k in range(7):
        counts = [0 for x in pages[k]]
        last = [x for x in pages[k]]
        not_done = list(range(len(pages[k])))

        while not len(not_done) == 0:
            for n in not_done:
                print("\nCollecting replies for POI tweet: " + str(pages[k][n]['id']) + " (POI: " + str(pages[k][n]['username']) + ")\n")
                reps = twitter.get_replies(pages[k][n], last[n])

                if len(reps) >= 1:
                    last[n] = TWPreprocessor.preprocess(reps[len(reps) - 1])
                else:
                    counts[n] = 10

                out_list = [r for r in reps if r.user.screen_name not in poi_ids]
                poi_reps += [TWPreprocessor.preprocess(o) for o in out_list]
                counts[n] += len(out_list)
                done, not_done = finished_poi_replies(counts)

                print("Total POI tweet replies collected: " + str(len(poi_reps)))
                print("POI tweets with 10 replies: " + str(done + (k * 50)))
                print("--------------------------------------------------------- (Block " + str(k + 1) + ")")

    return poi_reps


def collect_lang(lang):
    lang_name = "Hindi" if lang == 'hi' else ("Spanish" if lang == 'es' else "English")
    last_key_word = [None for k in keywords]
    out = []

    print("\n\nCollecting tweets for language: " + lang_name + "\n")

    while len(out) < 5000:
        for i in range(len(keywords)):
            tws = twitter.get_tweets_by_lang_and_keyword(keywords[i], last_key_word[i])
            out_temp = [t for t in tws if twitter.meet_basic_tweet_requirements(t, lang, keywords) and t.user.screen_name not in poi_ids]
            last_key_word[i] = out_temp[len(out_temp)-1]
            out += [TWPreprocessor.preprocess(o) for o in out_temp]

        print(str(len(out)) + " tweets collected for language: " + lang_name)

    print("\nFinished collecting tweets for language: " + lang_name)

    return out


if __name__ == "__main__":
    twitter = twitter_interface.Twitter()

    with open("config.json") as json_file:
        data = json.load(json_file)
        pois = data['pois']
        keywords = data['keywords']

    poi_ids = [x['screen_name'] for x in pois]
    pois_temp = [x for x in range(len(pois))]
    covid_tw = []
    last_tweet = []
    pois_collected = []
    rt_cnt = 0
    poi_tweets_collected = 0
    poi_rep_10 = 0

    for i in range(len(pois)):
        covid_tw.append([])
        pois_collected.append([])
        last_tweet.append(None)

    while len(pois_temp) > 0:
        to_remove = []

        for i in range(len(pois)):
            if i in pois_temp:
                if pois[i]["finished"] == 0:
                    print(f"---------- collecting tweets for poi: {pois[i]['screen_name']}")

                raw_tweets = twitter.get_tweets_by_poi_screen_name(pois[i], last_tweet[i])  # pass args as needed

                if len(raw_tweets) > 0:
                    last_tweet[i] = raw_tweets[len(raw_tweets)-1]
                    processed_tweets = []

                    for tw in raw_tweets:
                        if twitter.meet_basic_tweet_requirements(tw, "", keywords):
                            covid_tw[i].append(tw)

                        processed_tweets.append(TWPreprocessor.preprocess(tw))

                    j = len(processed_tweets)

                    while (len(processed_tweets) + len(pois_collected[i]) > (len(covid_tw[i]) * 10)) & (len(covid_tw) > 0) & (j >= 0):
                        if not(processed_tweets[j-1] in covid_tw[i]):
                            processed_tweets.remove(processed_tweets[j-1])

                        j = j - 1

                    for item in processed_tweets:
                        item_text = item["tweet_text"]

                        if "rt @".encode("utf-8") in item_text.encode("utf-8").lower():
                            rt_cnt = rt_cnt + 1

                    pois_collected[i] = pois_collected[i] + processed_tweets

                    if len(pois_collected[i]) >= 500:
                        pois[i]["finished"] = 1
                        to_remove.append(i)

                    print("Total tweets: " + str(len(pois_collected[i])))
                    print("Total COVID tweets: " + str(len(covid_tw[i])))
                else:
                    to_remove.append(i)

        for item in to_remove:
            pois_temp.remove(item)

    all_tweets = []

    for i in range(len(pois)):
        all_tweets += pois_collected[i]

    poi_tweets_collected = len(all_tweets)

    print("\n\nSaving tweets to \'tweets.json\'...\n\n")

    with open('tweets.json', 'w') as f:
        json.dump(all_tweets, f)

    tweet_ids = [x['id'] for x in all_tweets]

    print("Collecting POI tweet replies...\n")
    poi_replies = get_poi_replies(all_tweets)
    print("\nFinished collecting POI tweet replies")
    print("\n\nSaving tweets to \'tweets.json\'...\n\n")

    with open('tweets.json', 'w') as f:
        json.dump(all_tweets, f)

    all_tweets += poi_replies
    tweet_ids += [x['id'] for x in poi_replies]

    for lang in ['en', 'es', 'hi']:
        lang_tweets = collect_lang(lang)
        all_tweets += lang_tweets
        tweet_ids += [x['id'] for x in lang_tweets]

        print("\n\nSaving tweets to \'tweets.json\'...\n\n")

        with open('tweets.json', 'w') as f:
            json.dump(all_tweets, f)

    tweet_dict = {}
    replied_to = []

    for t in all_tweets:
        tweet_dict.update({t['id']: t})

    for t in all_tweets:
        if t['reply_to'] in tweet_ids and tweet_dict[t['reply_to']]['poi_name'] == "" and t['reply_to'] not in replied_to:
            replied_to.append(t['reply_to'])

    last_key = [None for k in keywords]
    retweets = [t for t in all_tweets if rt(t)]
    del_rt = True

    while (len(all_tweets) < 50000 and len(replied_to) < 1500) or del_rt:
        for i in range(len(keywords)):
            print("Collecting tweets for keyword: \'" + keywords[i] + "\'...")

            tws = twitter.get_tweets_by_lang_and_keyword(keywords[i], last_key[i])
            out_temp = [t for t in tws if twitter.meet_basic_tweet_requirements(t, "", keywords) and t.user.screen_name not in poi_ids]
            last_key[i] = out_temp[len(out_temp) - 1]
            out = [TWPreprocessor.preprocess(o) for o in out_temp]

            if del_rt:
                out_good = [x for x in out if not rt(x)]
                out = out_good

            tweet_ids += [o['id'] for o in out]
            all_tweets += out

            for o in out:
                tweet_dict.update({o['id']: o})

                if rt(o):
                    retweets.append(o)

            for o in out:
                if o['reply_to'] in tweet_ids and tweet_dict[o['reply_to']]['poi_name'] == "" and o['reply_to'] not in replied_to:
                    replied_to.append(t['reply_to'])

            del_rt = (len(retweets) / len(all_tweets)) > .15

            print("Total tweets collected: " + str(len(all_tweets)))
            print("Total non-POI replies collected: " + str(len(replied_to)) + "\n")
            print("--------------------------------------------------------------------------------------------\n")

        print("\n\nSaving tweets to \'tweets.json\'...\n\n")

        with open('tweets.json', 'w') as f:
            json.dump(all_tweets, f)

    with open('tweets.json', 'w') as f:
        json.dump(all_tweets, f)

    print("\n\nProcess complete! Tweets saved to \'tweets.json\'.")
    print("Total tweets collected: " + str(len(all_tweets)))
    print("Total non-POI replies collected: " + str(len(replied_to)))
    print("Total non-POI tweets collected: " + str(len(all_tweets) - poi_tweets_collected))
