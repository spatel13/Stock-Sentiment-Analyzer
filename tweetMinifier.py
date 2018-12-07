# Sahil Patel
# CMSC 473 - NLP
#

from datetime import datetime
import ast
import time
import json

RAW_TWEETS = "raw_tweets/"
MINIFIED_TWEETS = "minified_tweets/"

def curateTweets(filename):
    tweets = []
    with open(filename, "r") as ifp:
        data = ifp.readlines()
        for i in range(len(data)):
            try:
                tweets.append(ast.literal_eval(data[i].strip()))
            except Exception as e:
                pass

    return tweets

def monthToNum(month):
    if month == "Dec":
        return 12
    elif month == "Nov":
        return 11
    elif month == "Oct":
        return 10
    elif month == "Sep":
        return 9
    elif month == "Aug":
        return 8
    elif month == "Jul":
        return 7
    elif month == "Jun":
        return 6
    elif month == "May":
        return 5
    elif month == "Apr":
        return 4
    elif month == "Mar":
        return 3
    elif month == "Feb":
        return 2
    elif month == "Jan":
        return 1

def minify(data):
    tweets = []
    for line in data:
        created = datetime.strptime(line['created_at'], "%a %b %d %H:%M:%S %z %Y")
        tweet = {
            'text': line['text'],
            'favorite_count': line['favorite_count'],
            'retweet_count': line['retweet_count'],
            'created': created,
        }
        tweets.append(tweet)

    return tweets

def writeFile(data, fileName):
    ofp = open(fileName, "w")
    for tweet in data:
        ofp.write(str(tweet) + "\n")

    ofp.close()

def main():
    teslaTweets = curateTweets(RAW_TWEETS + "tesla_tweets.txt")
    minTeslaTweets = minify(teslaTweets)
    writeFile(minTeslaTweets, MINIFIED_TWEETS + "tesla.txt")
        
    facebookTweets = curateTweets(RAW_TWEETS + "facebook_tweets.txt")
    minFacebookTweets = minify(facebookTweets)
    writeFile(minFacebookTweets, MINIFIED_TWEETS + "facebook.txt")


    appleTweets = curateTweets(RAW_TWEETS + "apple_tweets.txt")
    minAppleTweets = minify(appleTweets)
    writeFile(minAppleTweets, MINIFIED_TWEETS + "apple.txt")
    

    googleTweets = curateTweets(RAW_TWEETS + "google_tweets.txt")
    minGoogleTweets = minify(googleTweets)
    writeFile(minGoogleTweets, MINIFIED_TWEETS + "google.txt")

    total = len(teslaTweets) + len(facebookTweets) + len(appleTweets) + len(googleTweets)
    print(total)

main()
