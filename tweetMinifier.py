# Sahil Patel
# CMSC 473 - NLP
#

import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

# Pulls the required data from each tweet into
# a minified version dictionary and appends
# that to a list that will be written to a file
def minify(data):
    tweets = []
    for line in data:
        tweet = {
            'text': line['text'],
            'favorite_count': line['favorite_count'],
            'retweet_count': line['retweet_count'],
            'created': line['created_at'],
        }
        tweets.append(tweet)

    return tweets


def dataHandler(db):
    raw_tweets = db.raw_tweets
    tweets = raw_tweets.find()
    mini_tweets = minify(tweets)

    for tweet in mini_tweets:
        print(tweet["text"])

    minified_tweets = db.minified_tweets
    minified_tweets.insert_many(mini_tweets)

def main():
    db = client.tesla
    dataHandler(db)

    db = client.facebook
    dataHandler(db)

    db = client.apple
    dataHandler(db)

    db = client.google
    dataHandler(db)

main()
