import json
import math
from stanfordcorenlp import StanfordCoreNLP

SENTIMENT = ["Really Negative", "Negative", "Neutral", "Positive", "Really Positive"]

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

sNLP = StanfordNLP()

# This function takes in a string and removes anything greater than
# the 128 basic ASCII table i.e removes unique character and emojis
# that would cause CoreNLP to crash and not return a sentiment value
def removeUnicode(text):
	asciiText = ""
	for char in text:
		if(ord(char)<128):
			asciiText = asciiText + char
	return asciiText

# This function takes in a list of tweets and
# for every tweet, run the text through the the sentiment analyzer
# Finally, add the value to the tweet dictionary
def analyzeSentiment(text):
    text = removeUnicode(text)
    annotatedText = sNLP.annotate(text).get('sentences')

    val = 0
    for sentence in annotatedText:
        val += int(sentence.get('sentimentValue'))

    avgVal = val / len(annotatedText)        

    decimal = avgVal - int(avgVal)
    avgValInt = math.floor(avgVal) if (decimal < 0.5) else math.ceil(avgVal)

    return avgVal, SENTIMENT[avgValInt]

# def main():
#     analyzeSentiment(removeUnicode("$APPL would you guys have \"beat\" without the billions of dollars in buybacks to manipulate your EPS @tim_cook? Maybe that cash you're hoarding oversees should go to hiring, R&D, and new product creation instead of as a way to reduce your float. Then there may be actual innovation"))

#     analyzeSentiment(removeUnicode("$aapl on the other side of #Antitrust law. I agree that 30% is quite a high cut to take, but undecided on not allowing 3rd party selling of apps is fully anti competitive? It indeed provides some security & quality control for users.."))
    
# main()
