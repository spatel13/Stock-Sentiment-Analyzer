# Sahil Patel
# spatel13
# sahil.patel2461@gmail.com
# Last Edited: 05/13/2019


import json
import math
from stanfordnlp.server import CoreNLPClient

SENTIMENT = ["Really Negative", "Negative", "Neutral", "Positive", "Really Positive"]

# This function takes in a string and removes anything greater than
# the 128 basic ASCII table i.e removes unique character and emojis
# that would cause CoreNLP to crash and not return a sentiment value
def removeUnicode(text):
    # Initialize empty string
    asciiText = ""
    # For each letter in argument if the letter
    # is in the basic ASCII table add it to the
    # empty string else ignore it
    for char in text:
        if(ord(char)<128):
            asciiText = asciiText + char
    return asciiText

# This function takes in a list of tweets and
# for every tweet, run the text through the the sentiment analyzer
# Finally, add the value to the tweet dictionary
def analyzeSentiment(text):
    address = 'http://localhost:9000'
    annotatorsList = ['sentiment']
    with CoreNLPClient(endpoint=address, annotators=annotatorsList) as sNLP:
        # Remove letters and symbols that the Stanford CoreNLP
        # software won't understand i.e emojis
        text = removeUnicode(text)
        # Send the test to get analyzed by the CoreNLP server
        annotatedText = sNLP.annotate(text).sentence

        # This will total up the sentiment of each individual
        # sentence
        val = 0
        for sentence in annotatedText:
            val += int(sentence.get('sentimentValue'))

        # Average out the sentiment by
        # the number of sentences analyzed
        avgVal = val / len(annotatedText)        

        # This part is purely to get a value
        # so that we can assign a word to the sentiment
        decimal = avgVal - int(avgVal)
        avgValInt = math.floor(avgVal) if (decimal < 0.5) else math.ceil(avgVal)

        return avgVal, SENTIMENT[avgValInt]
