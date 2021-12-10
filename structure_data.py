"""
This is the program for creating the transition probability matrix for TweetRank calculation
"""

import json
import CheapLinAlg as cla


fp = "C:/Users/mjsul/Desktop/"


# "Node" = graph vertex
class Node:
    def __init__(self, label):
        self.label = label  # tweet ID
        self.btr = 1  # Base TweetRank
        self.tr = 0  # TweetRank

    def beta(self, n):
        return n.btr / (self.btr + n.btr)


class Graph:
    # initialize graph structure
    def __init__(self, nodes, tweet_dict):
        self.nodes = nodes
        self.tweet_dict = tweet_dict
        self.comments = set()
        self.hashtags = {}

        self.w_rt = .7  # retweet weight
        self.w_l = .5  # like weight
        self.w_c = 2  # comment weight
        self.w_h = 1  # hashtag weight
        self.teleport = .1  # teleport probability

        self.index = {}
        ht_index = {}

        print("   Creating reply graph edges, calculating \"Base TweetRank\", and structuring hashtag data...")
        for n in self.nodes:
            self.index.update({n.label: n})
            # get tweet object n_tw from tweet id n.label
            n_tw = self.tweet_dict[n.label]
            # calculate Base TweetRank of n
            n.btr += (n_tw['num_likes'] * self.w_l) + (n_tw['num_retweets'] * self.w_rt)

            # if n_tw is a comment on some tweet m_tw, add a graph edge n -> m
            if n_tw['reply_to'] and not n_tw['reply_to'] == "":
                if int(n_tw['reply_to']) in self.tweet_dict.keys():
                    self.comments.add((n.label, int(n_tw['reply_to'])))

            # for each hashtag h in n_tw, append n to the "hashtag index" of h; the list of all tweets (IDs) containing h
            for h in n_tw['hashtags']:
                if h in ht_index.keys():
                    ht_index[h].append(n)
                else:
                    ht_index.update({h: [n]})

        print("   Creating hashtag graph edges...")
        for n in self.nodes:
            # iterate over each hashtag h in the tweet
            for h in self.tweet_dict[n.label]['hashtags']:
                # iterate over all tweets m that use the hashtag h
                for m in ht_index[h]:
                    if not m == n:
                        # add 1 to the weight of the graph edge n -> m
                        # "elif (m.label, n.label) not..." ensures that we only create one edge for each pair of tweets
                        if (n.label, m.label) in self.hashtags.keys():
                            self.hashtags[(n.label, m.label)] += 1
                        elif (m.label, n.label) not in self.hashtags.keys():
                            self.hashtags.update({(n.label, m.label): 1})

        # attempting to get garbage collector to reallocate ht_index
        ht_index = None

    def calc_tm_dict(self):
        # initialize an NxN CheapSquareMatrix, where N = num. of tweets in dataset
        mat = cla.CheapSquareMatrix(elems=[n.label for n in self.nodes])

        print("   Adding reply values...")
        # rows[a][b] != 0 => a comments on b
        for (a, b) in self.comments:
            mat.update_entry(a, b, self.w_c * self.index[a].beta(self.index[b]))

        print("   Adding hashtag values...")
        # for each weighted edge i -> j, add a "graph edge" to the transition matrix at entries P(i,j) and P(j,i),
        # weighted by relative Base TweetRank
        for (a, b) in self.hashtags.keys():
            wgt = self.hashtags[(a, b)] * self.w_h
            beta = self.index[a].beta(self.index[b])
            mat.update_entry(a, b, mat.get_entry(a, b) + (wgt * beta))
            mat.update_entry(b, a, mat.get_entry(b, a) + (wgt * (1 - beta)))

        self.hashtags = None
        self.comments = None
        print("   Normalizing transition matrix into ergodic Markov chain...")
        # adaptation of PageRank transition matrix algorithm described in textbook
        mat.zero_val = 1 / len(mat.elems)  # <== corresponds to performing step 1 of textbook procedure
        cons_zv = self.teleport / len(mat.elems)

        for x in mat.row_index.keys():
            total = 0
            # corresponds to performing steps 2-4 of textbook procedure on all empty entries of the row
            mat.row_index[x].zero_val = cons_zv

            # sum together each non-zero entry of given row
            for y in mat.row_index[x].index.keys():
                total += mat.row_index[x].index[y]

            # corresponds to performing steps 2-4 of textbook procedure on all NON-empty entries of the row
            for y in mat.row_index[x].index.keys():
                mat.update_entry(x, y, ((mat.row_index[x].index[y] / total) * (1 - self.teleport)) + cons_zv)

        # return json-serializable representation of transition matrix
        return mat.to_json()


if __name__ == "__main__":
    # load dataset
    with open(fp + 'tweets.json') as f:
        data = json.load(f)

    tweet_dictionary = {}
    tw_ids = []

    # iterate over dataset and create graph node for each tweet, along with dictionary entry linking the id to the tweet
    for d in data:
        tw_id = d['id']
        tweet_dictionary.update({tw_id: d})
        tw_ids.append(Node(tw_id))

    print("Updating Twitter graph structure:")
    # create Twitter graph structure
    grp = Graph(tw_ids, tweet_dictionary)
    print("Done!\n\nCreating transition matrix:")
    # calculate json-serializable transition matrix
    mat_json = grp.calc_tm_dict()

    # save transition matrix and initial state vector to json files
    print("Done!\n\nSaving to \'transition_matrix.json\'...")
    with open(fp + 'transition_matrix.json', 'w') as f2:
        json.dump(mat_json, f2)

    with open(fp + 'tr_data.json', 'w') as f3:
        json.dump({
            'iterations': 0,
            'epochs': 50,
            'steady_vector': [(1 / len(mat_json['elems'])) for x in mat_json['elems']]
        }, f3)
