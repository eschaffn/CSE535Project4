import json
import copy
import CheapLinAlg as cla


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
        og_mat = cla.CheapSquareMatrix(node_labels)

        # rows[a][b] != 0 => a quote-tweets b
        for (a, b) in self.qts:
            og_mat.update_entry(a, b, og_mat.get_entry(a, b) + self.w_q)

        # rows[a][b] != 0 => a retweets b
        for (a, b) in self.rts:
            og_mat.update_entry(a, b, og_mat.get_entry(a, b) + self.w_r)

        # rows[a][b] != 0 => a comments on b
        for (a, b) in self.comments:
            og_mat.update_entry(a, b, og_mat.get_entry(a, b) + self.w_c)

        og_mat_copy = copy.deepcopy(og_mat)
        btr_vals = self.find_steady_vec(og_mat)

        for i in range(len(btr_vals)):
            self.index[node_labels[i]].btr = btr_vals[i]

        for n in self.nodes:
            for m in [x for x in self.nodes if not x == n]:
                if (n.label, m.label) in self.hashtags.keys():
                    wgt = self.hashtags[(n.label, m.label)] * self.w_h
                    og_mat_copy.update_entry(n.label, m.label, og_mat.get_entry(n.label, m.label) + (wgt * m.beta(n)))
                    og_mat_copy.update_entry(m.label, n.label, og_mat.get_entry(m.label, n.label) + (wgt * n.beta(m)))

        tr_vals = self.find_steady_vec(og_mat_copy)

        for i in range(len(tr_vals)):
            self.index[node_labels[i]].tr = tr_vals[i]

    def find_steady_vec(self, mat):
        for x in mat.row_index.keys():
            total = 0

            for y in mat.row_index[x].keys():
                total += mat.row_index[x][y]

            for y in mat.row_index[x].keys():
                mat.row_index[x][y] = mat.row_index[x][y] / total

        mat.scalar_mul(1 - self.teleport)
        mat.add_matrix_of_ns(self.teleport / len(self.nodes))
        init_vec = cla.CheapVector(mat.elems)
        init_vec.add_uniform_vec(1 / len(self.nodes))

        for i in range(50):
            init_vec = mat.as_linear_map(init_vec, right=False)

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
