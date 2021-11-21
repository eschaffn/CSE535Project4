import copy
import torch
import json


class Node:
    def __init__(self, label):
        self.label = label
        self.btr = 1
        self.tr = 1

    def beta(self, n):
        return self.btr / (self.btr + n.btr)


class Graph:
    def __init__(self, nodes, tweet_dict):
        self.nodes = nodes
        self.tweet_dict = tweet_dict
        self.qts = set()
        self.rts = set()
        self.comments = set()
        self.hashtags = {}
        self.gen_struct()

        self.w_q = 0
        self.w_r = 0
        self.w_c = 0
        self.w_h = 0
        self.teleport = 0

        self.index = {}

        for n in self.nodes:
            self.index.update({n.label: n})

    def gen_struct(self):
        for n in self.nodes:
            n_tw = self.tweet_dict[n]

            for m in [x for x in self.nodes if not x == n]:
                if (n.label, m.label) not in self.hashtags.keys():
                    m_tw = self.tweet_dict[m]

                    if m_tw['quote_tweet'] == n:
                        self.qts.add((m.label, n.label))

                    if m_tw['retweet'] == n:
                        self.rts.add((m.label, n.label))

                    if m_tw['reply_to'] == n:
                        self.comments.add((m.label, n.label))

                    common_hashtags = 0

                    for n_h in n_tw['hashtags']:
                        for m_h in m_tw['hashtags']:
                            if n_h == m_h:
                                common_hashtags += 1

                    self.hashtags.update({(m.label, n.label): common_hashtags})

    def calc_tr(self):
        node_labels = [n.label for n in self.nodes]
        rows = [[0 for x in self.nodes] for x in self.nodes]

        # rows[b][a] != 0 => b quote-tweets a
        for (a, b) in self.qts:
            rows[node_labels.index(b)][node_labels.index(a)] += self.w_q

        # rows[b][a] != 0 => b retweets a
        for (a, b) in self.rts:
            rows[node_labels.index(b)][node_labels.index(a)] += self.w_r

        # rows[b][a] != 0 => b comments on a
        for (a, b) in self.comments:
            rows[node_labels.index(b)][node_labels.index(a)] += self.w_c

        rows_copy = copy.deepcopy(rows)
        btr_vals = self.find_steady_vec(rows)

        for i in range(len(btr_vals)):
            self.index[node_labels[i]].btr = btr_vals[i]

        for n in self.nodes:
            for m in [x for x in self.nodes if not x == n]:
                if (n.label, m.label) in self.hashtags.keys():
                    wgt = self.hashtags[(n.label, m.label)] * self.w_h
                    rows_copy[node_labels.index(n.label)][node_labels.index(m.label)] += wgt * m.beta(n)
                    rows_copy[node_labels.index(n.label)][node_labels.index(m.label)] += wgt * n.beta(m)

        tr_vals = self.find_steady_vec(rows_copy)

        for i in range(len(tr_vals)):
            self.index[node_labels[i]].tr = tr_vals[i]

    def find_steady_vec(self, mat):
        zeros = [0 for x in self.nodes]

        for i in range(len(mat)):
            if mat[i] == zeros:
                mat[i] = [(1 / len(self.nodes)) for x in self.nodes]
            else:
                row_sum = 0

                for elem in mat[i]:
                    row_sum += elem

                for j in range(len(mat[i])):
                    mat[i][j] = mat[i][j] / row_sum

        init_vec = torch.tensor([(1 / len(self.nodes)) for x in self.nodes], dtype=torch.float32)
        weight_matrix = torch.tensor([[(self.teleport / len(self.nodes)) for x in self.nodes] for x in self.nodes], dtype=torch.float32)
        transition_matrix = torch.tensor(mat, dtype=torch.float32)
        transition_matrix = torch.mul(transition_matrix, torch.tensor([1 - self.teleport], dtype=torch.float32))
        transition_matrix = torch.add(transition_matrix, weight_matrix)

        for i in range(50):
            init_vec = torch.mul(transition_matrix, init_vec)

        return init_vec.tolist()


if __name__ == "__main__":
    with open('tweets.json') as f:
        data = json.load(f)

    tweet_dictionary = {}
    tw_ids = []

    for d in data:
        id = d['id']
        tweet_dictionary.update({id: d})
        tw_ids.append(Node(id))

    grp = Graph(tw_ids, tweet_dictionary)
    grp.calc_tr()
