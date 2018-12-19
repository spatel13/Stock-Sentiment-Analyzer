import ast
from datetime import datetime
import json
import logging
import pickle
from stanfordcorenlp import StanfordCoreNLP

MINIFIED_TWEETS = "minified_tweets/"
PICKLE_FOLDER = "pickles/"

class StanfordNLP:
    def __init__(self, host='http://localhost', port=9000):
        self.nlp = StanfordCoreNLP(host, port=port,
                                   timeout=30000)  # , quiet=False, logging_level=logging.DEBUG)
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

def removeUnicode(text):
	asciiText = ""
	for char in text:
		if(ord(char)<128):
			asciiText = asciiText + char
	return asciiText
    
def textToDateTime(date):
    return datetime.strptime(date, "%a %b %d %H:%M:%S %z %Y")
    
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

def analyzeSentiment(tweets):
    sNLP = StanfordNLP(host='http://159.203.87.119')
    for i in range(len(tweets)):
        annotatedText = sNLP.annotate(removeUnicode(tweets[i]['text']))
    
        keys = list(annotatedText.keys())
    
        for sentence in annotatedText.get(keys[0]):
            tweets[i]['sentiment'] = sentence['sentiment']
            tweets[i]['sentimentValue'] = sentence['sentimentValue']

    return tweets

def categorizeTweets(tweets):
    tweetsByDate = {}
    for tweet in tweets:
        created = textToDateTime(tweet['created'])
        if tweetsByDate.get(created.strftime("%Y-%m-%d")) == None:
            tweetsByDate[created.strftime("%Y-%m-%d")] = [tweet]
        else:
            tweetsByDate[created.strftime("%Y-%m-%d")].append(tweet)

    return tweetsByDate

def dailySentiment(tweetsByDate):
    for key in tweetsByDate.keys():
        numOfTweets = len(tweetsByDate.get(key))
        overallSentiment = 0
        for tweet in tweetsByDate.get(key):
            overallSentiment += int(tweet['sentimentValue'])

        print(key + ":: " + " Total Sentiment: " +str(overallSentiment) + " / numOfTweets: " + str(numOfTweets) + " = " + str(overallSentiment/numOfTweets))
    print()

def main():
    print("TESLA:")
    try:
        inFile = open(PICKLE_FOLDER + "tesla", "rb")
        teslaTweets = pickle.load(inFile)
        inFile.close()
    except Exception as e:
        teslaTweets = curateTweets(MINIFIED_TWEETS + "tesla.txt")
        teslaTweets = analyzeSentiment(teslaTweets)
        outFile = open(PICKLE_FOLDER + "tesla", "wb")
        pickle.dump(teslaTweets, outFile)
        outFile.close()

    tweetsByDate = categorizeTweets(teslaTweets)
    dailySentiment(tweetsByDate)

    print("FACEBOOK:")
    try:
        inFile = open(PICKLE_FOLDER + "facebook", "rb")
        facebookTweets = pickle.load(inFile)
        inFile.close()
    except Exception as e:
        facebookTweets = curateTweets(MINIFIED_TWEETS + "facebook.txt")
        facebookTweets = analyzeSentiment(facebookTweets)
        outFile = open(PICKLE_FOLDER + "facebook", "wb")
        pickle.dump(facebookTweets, outFile)
        outFile.close()

    tweetsByDate = categorizeTweets(facebookTweets)
    dailySentiment(tweetsByDate)

    print("APPLE:")
    try:
        inFile = open(PICKLE_FOLDER + "apple", "rb")
        appleTweets = pickle.load(inFile)
        inFile.close()
    except Exception as e:
        appleTweets = curateTweets(MINIFIED_TWEETS + "apple.txt")
        appleTweets = analyzeSentiment(appleTweets)
        outFile = open(PICKLE_FOLDER + "apple", "wb")
        pickle.dump(appleTweets, outFile)
        outFile.close()

    tweetsByDate = categorizeTweets(appleTweets)
    dailySentiment(tweetsByDate)

    print("GOOGLE:")
    try:
        inFile = open(PICKLE_FOLDER + "google", "rb")
        googleTweets = pickle.load(inFile)
        inFile.close()
    except Exception as e:
        googleTweets = curateTweets(MINIFIED_TWEETS + "google.txt")
        googleTweets = analyzeSentiment(googleTweets)
        outFile = open(PICKLE_FOLDER + "google", "wb")
        pickle.dump(googleTweets, outFile)
        outFile.close()

    tweetsByDate = categorizeTweets(googleTweets)
    dailySentiment(tweetsByDate)
    
main()
