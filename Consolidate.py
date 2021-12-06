import json

#PUT NEW FILEPATH HERE
fp = 'C:/Users/mjsul/Desktop/'


if __name__ == "__main__":
    #put the original tweets.json here
    with open(fp + 'tweets.json') as f:
        data_tr = json.load(f)

    #put tweets with stance detection here
    with open(fp + 'tweets_VaxxTopics.json') as f2:
        data_ling = json.load(f2)

    index_tr = {}
    index_ling = {}
    out = []

    for d in data_tr:
        index_tr.update({d['id']: d})

    for d in data_ling:
        index_ling.update({d['id']: d})

    for k in index_tr.keys():
        if k in index_ling.keys():
            index_tr[k].update({
                'stance': index_ling[k]['stance'],
            })

            out.append(index_tr[k])

    with open(fp + 'tweets.json', 'w') as f3:
        json.dump(out, f3)
