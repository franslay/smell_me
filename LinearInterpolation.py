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

        # self.l1 = 0.1   # --> unigram
        # self.l2 = 0.6  # --> bigram k: 0.0088
        # self.l3 = 0.3  # --> trigram k: 0.0009

        # experimenting
        
        self.l1 = 0.06
        self.l2 = 0.62
        self.l3 = 0.32
        # self.l1 = 0.8
        # self.l2 = 0.6
        # self.l3 = 0.32
    
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
        diceroll = random.uniform(0, 1) # dice roll
        cutoff = 0.00015
        sum = 0.0
        for word in self.bigrammodel.unigramcounts.keys(): # while p(word) < cutoff -> then continue
            prob1 = self.unigrammodel.get_unigram_probability(word)
            prob2 = self.bigrammodel.get_bigram_probability(word, prev)
            prob3 = self.trigrammodel.get_trigram_probability(word, prev, prevtwo)
            wordprob = prob1 + prob2 + prob3

            sum += (self.l1 * prob1) # interpolate probs of each 
            sum += (self.l2 * prob2)
            sum += (self.l3 * prob3)
            if sum > diceroll:
                if wordprob < cutoff: # new cut off fr really improbable words
                    continue
                else:
                    return word

#Come up with two scores for a couple models (smoothbi, smoothtri, lin interp, lin interp v2) & COMPARE
# Readability 
# How representative is this of the accord?