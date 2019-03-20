# Sahil Patel
# CMSC 473 - NLP
# spatel32@umbc.edu

import os
from pymongo import MongoClient
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
tweets_db = client['tweets'].raw_tweets

class StockStreamer(TwythonStreamer):
    def __init__(self, app_key, app_secret, oauth_token, oauth_token_secret, **kwargs):
        super(StockStreamer, self).__init__(app_key, app_secret, oauth_token, oauth_token_secret, **kwargs)
        self.db = client['tweets']
        self.raw_tweets = self.db.raw_tweets

    def _request(self, url, method='GET', params=None):
        self.queries = params['track']
        super()._request(url, method, params)
        
    def on_success(self, data):
        """what do we do when twitter sends us data?
        here data will be a Python object representing a tweet"""

        # only want to collect English-language tweets
        if data.get('lang') == 'en':
            # Find which query caused the tweet to be found
            # and appropriately tag the tweet with it
            for query in self.queries:
                trackers = query.split(",")
                for track in trackers:
                    if track in data.get("text"):
                        data['track'] = trackers[0]
                        tweets_db.insert_one(data)

                        print(trackers[0].upper() + ":  " + data.get("text"))
                        

    def on_error(self, status_code, data):
        print(status_code, data)
        print("BIG ERROR==========================")
        self.disconnect()
        
if __name__ == '__main__':
    queries = ["tesla,#tesla,@tesla,$TSLA", "facebook,#facebook,@facebook,$FB", "apple,#apple,@apple,$aapl", "google,#google,@google,$goog"]

    stream = StockStreamer(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream.statuses.filter(track=queries)

