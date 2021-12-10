"""
This is the program for calculating the steady-state vector of the transition matrix P
"""
import json
import CheapLinAlg as cla
from datetime import datetime

fp = "C:/Users/mjsul/Desktop/"


if __name__ == "__main__":
    mat = cla.CheapSquareMatrix()

    # loads transition matrix from json file
    print("Loading transition matrix and state vector from files...")
    with open(fp + 'transition_matrix.json') as f:
        mat.from_json(json.load(f))

    # loads state vector, current iteration, and total number of iterations ("epochs") from json file
    with open(fp + 'tr_data.json') as f2:
        tr_data = json.load(f2)
        steady_vec = cla.vec_from_json(tr_data['steady_vector'])
        epochs = tr_data['epochs']
        its = tr_data['iterations']

    # main loop-- repeatedly multiplies state vector by probability matrix
    print("Done!\n\nFinding steady-state vector")
    while its < epochs:
        print("   \"Epoch\" " + str(its + 1) + "/" + str(epochs) + " (" + datetime.now().strftime('%H:%M:%S') + ")")
        # multiply state vector by transition matrix and increase current iteration by 1
        new_vec = mat.as_linear_map(steady_vec, right=False)
        steady_vec = new_vec
        its += 1

        # dump current state vector to json file so we can quit and reload procedure if necessary without losing progress
        print("    Saving state vector to \'tr_data.json\'...")
        with open(fp + 'tr_data.json', 'w') as f3:
            json.dump({
                'epochs': epochs,
                'iterations': its,
                'steady_vector': steady_vec.tolist()
            }, f3)

    sv_list = steady_vec.tolist()

    # load dataset, add TweetRank values, and save dataset
    print("Process complete! Saving TweetRank(TM) values to \'tweets_tr.json\'")
    with open(fp + 'tweets.json') as f4:
        data = json.load(f4)

    for d in data:
        d.update({'tweet_rank': sv_list[mat.elems.index(d['id'])]})

    with open(fp + 'tweets_tr.json', 'w') as f5:
        json.dump(data, f5)
