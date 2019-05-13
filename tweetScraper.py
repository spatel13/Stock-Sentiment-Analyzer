# Sahil Patel
# CMSC 473 - NLP
# spatel32@umbc.edu

import os
from pymongo import MongoClient
from sentimentAnalyzer import analyzeSentiment
import time
from twython import TwythonStreamer

# Tries to get the required API keys from the environment
# and if it fails, prints an error and exits
try:
    CONSUMER_KEY = os.environ.get("TWIT_API_KEY")
    CONSUMER_SECRET = os.environ.get("TWIT_API_SECRET")
    OAUTH_TOKEN = os.environ.get("TWIT_ACCESS_TOKEN")
    OAUTH_TOKEN_SECRET = os.environ.get("TWIT_ACCESS_SECRET")
except Exception as e:
    print("No_TwitterKeys", e)
    sys.exit(1)

client = MongoClient('localhost', 27017)
tweets_db = client['tweets'].tweets

tweets = []

class StockStreamer(TwythonStreamer):
    def __init__(self, app_key, app_secret, oauth_token, oauth_token_secret, **kwargs):
        super(StockStreamer, self).__init__(app_key, app_secret, oauth_token, oauth_token_secret, **kwargs)
        self.db = client['tweets']
        self.raw_tweets = self.db.raw_tweets

    def _request(self, url, method='GET', params=None):
        self.company = params['track'].split(',')[0]
        self.tweetCounter = 0
        super()._request(url, method, params)
        
    def on_success(self, data):
        """what do we do when twitter sends us data?
        here data will be a Python object representing a tweet"""

        minified_tweet = {}
        
        # only want to collect English-language tweets
        if data.get('lang') == 'en':

            sentimentValue, sentiment = analyzeSentiment(data.get('text'))
            
            minified_tweet['text'] = data.get('text')
            minified_tweet['favorite_count'] = data.get('favorie_count')
            minified_tweet['retweet_count'] = data.get('retweet_count')
            minified_tweet['created'] = data.get('created_at')
            minified_tweet['track'] = self.company
            minified_tweet['sentimentValue'] = sentimentValue
            minified_tweet['sentiment'] = sentiment

            tweets_db.insert_one(minified_tweet)

            print(self.company.upper() + ":  " + data.get("text"))
            self.tweetCounter += 1
            
            if self.tweetCounter >= 10:
                self.disconnect()
                        

    def on_error(self, status_code, data):
        print(status_code, data)
        print("BIG ERROR==========================")
        self.disconnect()

if __name__ == '__main__':
    queries = ["tesla,#tesla,@tesla,$TSLA", "facebook,#facebook,@facebook,$FB", "apple,#apple,@apple,$aapl", "google,#google,@google,$goog"]

    stream = StockStreamer(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    while True:
        for query in queries:
            stream.statuses.filter(track=query)
            time.sleep(30)
