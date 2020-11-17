from LanguageModel import LanguageModel
from UnigramModel import UnigramModel
from SmoothedBigram import SmoothedBigram
from SmoothedTrigram import SmoothedTrigram
import random

class LinearInterpolation(LanguageModel):

    def __init__(self):
        super().__init__()

        self.unigrammodel = UnigramModel()
        self.bigrammodel = SmoothedBigram()
        self.trigrammodel = SmoothedTrigram()

        self.l1 = 0.1   # --> unigram
        self.l2 = 0.6  # --> bigram k: 0.0088
        self.l3 = 0.3  # --> trigram k: 0.0009
        # self.l1 = 0.02   # --> unigram
        # self.l2 = 0.69  # --> bigram k: 0.0088
        # self.l3 = 0.29  # --> trigram k: 0.0009

        # experimenting
        """
        self.l1 = 0.03
        self.l2 = 0.69
        self.l3 = 0.28"""
    
    def train(self, sentences):
        self.unigrammodel.train(sentences)
        self.bigrammodel.train(sentences)
        self.trigrammodel.train(sentences)
    
    def get_word_probability(self, sentence, index):
        """print("printing the weights")
        print("uni vocab: " + str(len(self.unigrammodel.get_vocabulary())))
        print("bi vocab: " + str(len(self.bigrammodel.get_vocabulary())))
        print("tri vocab: " + str(len(self.trigrammodel.get_vocabulary())))"""

        prob = 0.0
        prob += (self.l1 * self.unigrammodel.get_word_probability(sentence, index))
        prob += (self.l2 * self.bigrammodel.get_word_probability(sentence, index))
        prob += (self.l3 * self.trigrammodel.get_word_probability(sentence, index))
        return prob
    
    def get_vocabulary(self):
        return self.bigrammodel.get_vocabulary()
    
    def generate_sentence(self):
        words = []
        prev = self.START
        prevtwo = self.START
        word = self.generate_word(prevtwo, prev)
        while word != self.STOP:
            words.append(word)
            prevtwo = prev
            prev = word
            word = self.generate_word(prevtwo, prev)
        return words
    
    def generate_word(self, prevtwo, prev):
        threshold = random.uniform(0, 1)
        sum = 0.0
        for word in self.bigrammodel.unigramcounts.keys():
            sum += (self.l1 * self.unigrammodel.get_unigram_probability(word)) # interpolate probs of each 
            sum += (self.l2 * self.bigrammodel.get_bigram_probability(word, prev))
            sum += (self.l3 * self.trigrammodel.get_trigram_probability(word, prev, prevtwo))
            if sum > threshold:
                return word