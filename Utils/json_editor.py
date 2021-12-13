import json
from tqdm import tqdm
import datetime


def updateJsonFile():
    jsonFile = open("fucktweets2.json", "r") # Open the JSON file for reading
    data = json.load(jsonFile) # Read the JSON into the buffer variable 'data' 
    jsonFile.close() # Close the JSON file

    ## Working with buffered content
    for line in tqdm(data): #Edit data one line at a time

        line['tweet_date'] = datetime.datetime.strptime(line['tweet_date'], '%a %b %d %H:%M:%S +0000 %Y').__str__()
        
        if line['retweet'] == "":
            line.update({"is_retweet": False})
        else:
            line.update({"is_retweet": True})

    with open("tweets7.json", "w+") as jsonFile: # create a new file and dump the edited data, can be named whatever..
        jsonFile.write(json.dumps(data))


updateJsonFile()