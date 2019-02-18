# Sahil Patel
# CMSC 473 - NLP
# spatel32@umbc.edu

from datetime import datetime
import os
import requests
import time
from twython import TwythonStreamer

TWEET_PATH = "raw_tweets/"

# Try to get the require API keys from the environment
# and if it fails, printe error and exit
try:
    CONSUMER_KEY = os.environ.get("TWIT_API_KEY")
    CONSUMER_SECRET = os.environ.get("TWIT_API_SECRET")
    OAUTH_TOKEN = os.environ.get("TWIT_ACCESS_TOKEN")
    OAUTH_TOKEN_SECRET = os.environ.get("TWIT_ACCESS_SECRET")
except Exception as e:
    print("No_TwitterKeys", e)
    sys.exit(1)

tweets = []
    
# StockStreamer code provided graciously by Dr. George Ray of UMBC
class StockStreamer(TwythonStreamer):

    def on_success(self, data):
        """what do we do when twitter sends us data?
        here data will be a Python object representing a tweet"""

        # only want to collect English-language tweets
        if data.get('lang') == 'en':
            # Add data to overall tweet list
            tweets.append(data)
            
        # write to file when we've collected 50
        if len(tweets) >= 5:
            self.disconnect()


    def on_error(self, status_code, data):
        print(status_code, data)
        print("BIG ERROR==========================")
        self.disconnect()


# The collectTweets function take in a file object and a query and starts the
# twitter API's stream to collect realtime tweets about the specified query
def collectTweets(ifp, query):
    #here is order for keys - you need to put your tokens here
    stream = StockStreamer(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    # Keep filtering tweets based on the query parameter. After 5 are found,
    # write each tweet to file with \n. Notify user of written status
    # sleep for 90 seconds and restart
    while True:
        global tweets
        tweets = []
        gmrStart = str(datetime.now().minute) + ":" + str(datetime.now().second)
        stream.statuses.filter(track=query)
        print("RETURN---RETURN---RETURN------")
        gmrEnd = str(datetime.now().minute) + ":" + str(datetime.now().second)
        
        for gmrText in tweets:
            # Print text out to console for confimation
            print(gmrText.get('text'))

            # Writing to the given text file
            ifp.write(str(gmrText) + "\n")

        time.sleep(90)

# This function get a valid integer choice between 1-5 for the
# 5 possible tweet streaming options
def getValidInt():
    userInput = int(input("Please enter a number from 1-5: "))
    while userInput < 1 or userInput > 5:
        print("Sorry, that is not a valid input.")
        userInput = int(input("Please enter a number from 1-5: "))

    return userInput

def main():
    # Provide user list of tweets to stream and collect
    print("1 - Tesla\n2 - Facebook\n3 - Apple\n4 - Google\n5 - Other")
    stock = getValidInt()

    # Decided which tweets the user wants and build the tracking query
    # and open the respective file of that company
    if stock == 1:
        query = "tesla,#tesla,@tesla,$TSLA"
        ifp = myFile = open(TWEET_PATH + "tesla_tweets.txt", "a+")
    elif stock == 2:
        query = "facebook,#facebook,@facebook,$FB"
        ifp = myFile = open(TWEET_PATH + "facebook_tweets.txt", "a+")
    elif stock == 3:
        query = "apple,#apple,@apple,$aapl"
        ifp = myFile = open(TWEET_PATH + "apple_tweets.txt", "a+")
    elif stock == 4:
        query = "google,#google,@google,$goog"
        ifp = myFile = open(TWEET_PATH + "google_tweets.txt", "a+")
    else:
        query = input("Please enter the query you would like to make (comma-seperated list): ")
        ifp = myFile = open(TWEET_PATH + "other_tweets.txt", "a+")

    # Start collecting tweets for the previously chosen query
    collectTweets(ifp, query)

main()
