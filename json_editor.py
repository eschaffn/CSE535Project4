import json
from tqdm import tqdm


def updateJsonFile():
    jsonFile = open("tweets.json", "r") # Open the JSON file for reading
    data = json.load(jsonFile) # Read the JSON into the buffer variable 'data' 
    jsonFile.close() # Close the JSON file

    ## Working with buffered content
    for line in tqdm(data): #Edit data one line at a time

        #manipulate data here (MT, sentiment, etc..)

    with open("tweets2.json", "w+") as jsonFile: # create a new file and dump the edited data, can be named whatever..
        jsonFile.write(json.dumps(data))


updateJsonFile()