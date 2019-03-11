import ast
from datetime import datetime
import json
from pymongo import MongoClient
from stanfordcorenlp import StanfordCoreNLP

client = MongoClient('localhost', 27017)

# This was gotten from the Stanford CoreNLP
# wiki pages and I am only vaguely sure what it does.
# Will update on more as I figure it out
class StanfordNLP:
    def __init__(self, host='http://localhost', port=9000):
        self.nlp = StanfordCoreNLP(host, port=port,
                                   timeout=30000)
        self.props = {
            'annotators': 'sentiment',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        }

    def word_tokenize(self, sentence):
        return self.nlp.word_tokenize(sentence)

    def pos(self, sentence):
        return self.nlp.pos_tag(sentence)

    def ner(self, sentence):
        return self.nlp.ner(sentence)

    def parse(self, sentence):
        return self.nlp.parse(sentence)

    def dependency_parse(self, sentence):
        return self.nlp.dependency_parse(sentence)

    def annotate(self, sentence):
        return json.loads(self.nlp.annotate(sentence, properties=self.props))

    @staticmethod
    def tokens_to_dict(_tokens):
        tokens = defaultdict(dict)
        for token in _tokens:
            tokens[int(token['index'])] = {
                'word': token['word'],
                'lemma': token['lemma'],
                'pos': token['pos'],
                'ner': token['ner']
            }
        return tokens

# This function takes in a string and removes anything greater than
# the 128 basic ASCII table i.e removes unique character and emojis
# that would cause CoreNLP to crash and not return a sentiment value
def removeUnicode(text):
	asciiText = ""
	for char in text:
		if(ord(char)<128):
			asciiText = asciiText + char
	return asciiText

# this function takes in a date string and
# converts it into a datetime object based on
# a specific parsing breakdown
def textToDateTime(date):
    return datetime.strptime(date, "%a %b %d %H:%M:%S %z %Y")

# This fuction loads the tweets in from the text files
# and evaluates them in to python dictionary objects
# If a evaluation fails then it passes over that tweet
# TODO: evaluate based on JSON potentially
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

# This function takes in a list of tweets and
# for every tweet, run the text through the the sentiment analyzer
# Finally, add the value to the tweet dictionary
def analyzeSentiment(tweets):
    sNLP = StanfordNLP(host='http://159.203.87.119')
    for i in range(len(tweets)):
        annotatedText = sNLP.annotate(removeUnicode(tweets[i]['text']))
    
        keys = list(annotatedText.keys())
    
        for sentence in annotatedText.get(keys[0]):
            tweets[i]['sentiment'] = sentence['sentiment']
            tweets[i]['sentimentValue'] = sentence['sentimentValue']

    return tweets

# This function takes in a list of tweets and
# categorizes them by the date on which they were tweeted
def categorizeTweets(tweets):
    tweetsByDate = {}
    for tweet in tweets:
        created = textToDateTime(tweet['created'])
        if tweetsByDate.get(created.strftime("%Y-%m-%d")) == None:
            tweetsByDate[created.strftime("%Y-%m-%d")] = [tweet]
        else:
            tweetsByDate[created.strftime("%Y-%m-%d")].append(tweet)

    return tweetsByDate

# This function takes in the dictionary of tweets and
# for each date calculates the average sentiment over
# the entire days worth of collected tweets
def dailySentiment(tweetsByDate):
    for key in tweetsByDate.keys():
        numOfTweets = len(tweetsByDate.get(key))
        overallSentiment = 0
        for tweet in tweetsByDate.get(key):
            overallSentiment += int(tweet['sentimentValue'])

        print(key + ":: " + " Total Sentiment: " +str(overallSentiment) + " / numOfTweets: " + str(numOfTweets) + " = " + str(overallSentiment/numOfTweets))
    print()

def main():
    db = client.tesla
    tweets = db.minified_tweets
    tweets = analyzeSentiment(tweets)
    tweetsByDate = categorizeTweets(tweets)
    dailySentiment(tweetsByDate)


    db = client.facebook
    tweets = db.minified_tweets
    tweets = analyzeSentiment(tweets)
    tweetsByDate = categorizeTweets(tweets)
    dailySentiment(tweetsByDate)

    db = client.apple
    tweets = db.minified_tweets
    tweets = analyzeSentiment(tweets)
    tweetsByDate = categorizeTweets(tweets)
    dailySentiment(tweetsByDate)

    db = client.google
    tweets = db.minified_tweets
    tweets = analyzeSentiment(tweets)
    tweetsByDate = categorizeTweets(tweets)
    dailySentiment(tweetsByDate)
    
main()
