from LanguageModel import LanguageModel
import random


class BigramModel(LanguageModel):

    def __init__(self):
        super().__init__()

        self.unigramcounts = dict()
        self.unigramcounts[self.STOP] = 0

        self.bigramcounts = dict()
        self.N = 0

    # REQUIRED FUNCTIONS from abstract parent LanguageModel
        
    def train(self, sentences): # count num bigrams and num unigrams
        # counting unigrams
        for line in sentences:
            line = line.copy() # don't want to alter the original given sentences
            line.append(self.STOP)
            for word in line:
                if not word in self.unigramcounts: # word is new
                    self.unigramcounts[word] = 1
                else: # word was not found
                    self.unigramcounts[word] += 1
            self.N += len(line)

        # counting bigrams
        for line in sentences:
            line = line.copy() # don't want to alter the original given sentences
            line.insert(0, self.START) # add start token
            line.append(self.STOP)
            for i in range(len(line)):
                if line[i] == self.STOP: # ex: </s> --> stop loop
                    continue ###
                elif not (line[i], line[i+1]) in self.bigramcounts: # word is new
                    self.bigramcounts[(line[i], line[i+1])] = 1
                else: # word was found
                    self.bigramcounts[(line[i], line[i+1])] += 1
        return
        
    def get_word_probability(self, sentence, index):

        # usage: word  prev 
        if index == len(sentence): # end of sentence
            return self.get_bigram_probability(self.STOP, sentence[index-1])
        elif index == 0: # start of sentence
            return self.get_bigram_probability(sentence[0], self.START)
        else:
            return self.get_bigram_probability(sentence[index], sentence[index-1])

    def get_vocabulary(self):
        words = list(self.unigramcounts.keys())
        return words

    def generate_sentence(self):
        words = []
        word = self.generate_word(self.START) # give prev word ( | GIVEN )
        # start sentence token as first  --> prev
        # make old word prev --> loop
        while word != self.STOP:
            words.append(word)
            prev = word
            word = self.generate_word(prev)
        return words
    
    # HELPER FUNCTIONS

    def get_bigram_probability(self, word, prev):

        if not (prev, word) in self.bigramcounts:
            return 0.0
        elif prev == self.START:
            return float(self.bigramcounts[(prev, word)] / self.unigramcounts[self.STOP])
        else:
            return float(self.bigramcounts[(prev, word)] / self.unigramcounts[prev]) 
    
    def generate_word(self, prev):
        threshold = random.uniform(0, 1)
        sum = 0.0
        for word in self.unigramcounts.keys():
            sum += self.get_bigram_probability(word, prev)
            if sum > threshold:
                return word
