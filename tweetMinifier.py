# Sahil Patel
# CMSC 473 - NLP
#

from datetime import datetime
import ast
import time
import json
from pymongo import MongoClient

# RAW_TWEETS = "raw_tweets/"
# MINIFIED_TWEETS = "minified_tweets/"

client = MongoClient('localhost', 27017)
db = client.tesla

# This fuction loads the tweets in from the text files
# and evaluates them in to python dictionary objects
# If a evaluation fails then it passes over that tweet
# TODO: evaluate based on JSON potentially
# def curateTweets(filename):
#     tweets = []
#     with open(filename, "r") as ifp:
#         data = ifp.readlines()
#         for i in range(len(data)):
#             try:
#                 tweets.append(ast.literal_eval(data[i].strip()))
#             except Exception as e:
#                 pass

#     return tweets

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

# Writes the minified tweets to a file
# as a json data followed by a \n
# def writeFile(data, fileName):
#     ofp = open(fileName, "w")
#     for tweet in data:
#         json.dump(tweet, ofp)
#         ofp.write("\n")
#     ofp.close()

def main():
    raw_tweets = db.raw_tweets

    tweets = raw_tweets.find()

    mini_tweets = minify(tweets)

    for tweet in mini_tweets:
        print(tweet["text"])

    minified_tweets = db.minified_tweets

    minified_tweets.insert_many(mini_tweets)
    
    # teslaTweets = curateTweets(RAW_TWEETS + "tesla_tweets.txt")
    # minTeslaTweets = minify(teslaTweets)
    # writeFile(minTeslaTweets, MINIFIED_TWEETS + "tesla.txt")
        
    # facebookTweets = curateTweets(RAW_TWEETS + "facebook_tweets.txt")
    # minFacebookTweets = minify(facebookTweets)
    # writeFile(minFacebookTweets, MINIFIED_TWEETS + "facebook.txt")


    # appleTweets = curateTweets(RAW_TWEETS + "apple_tweets.txt")
    # minAppleTweets = minify(appleTweets)
    # writeFile(minAppleTweets, MINIFIED_TWEETS + "apple.txt")
    

    # googleTweets = curateTweets(RAW_TWEETS + "google_tweets.txt")
    # minGoogleTweets = minify(googleTweets)
    # writeFile(minGoogleTweets, MINIFIED_TWEETS + "google.txt")

    # total = len(teslaTweets) + len(facebookTweets) + len(appleTweets) + len(googleTweets)
    # print(total)

main()
