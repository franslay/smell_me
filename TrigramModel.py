from LanguageModel import LanguageModel
import random


class TrigramModel(LanguageModel):

    def __init__(self):
        super().__init__()

        self.bigramcounts = dict()
        self.trigramcounts = dict()

        self.unigramcounts = dict()
        self.unigramcounts[self.STOP] = 0

        self.N = 0

    # REQUIRED FUNCTIONS from abstract parent LanguageModel
        
    def train(self, sentences):
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
        
        # counting trigrams
        for line in sentences:
            line = line.copy() # don't want to alter the original given sentences
            line.insert(0, self.START) # add start token
            line.insert(0, self.START) # add start token
            line.append(self.STOP)
            #print(line)
            for i in range(len(line)-2):
                if line[i+1] == self.STOP: # i </s> ' ' --> stop loop
                    continue ###
                elif not (line[i], line[i+1], line[i+2]) in self.trigramcounts: # word is new
                    self.trigramcounts[(line[i], line[i+1], line[i+2])] = 1
                else: # word was not found
                    self.trigramcounts[(line[i], line[i+1], line[i+2])] += 1
        return
        
    def get_word_probability(self, sentence, index):
        #print(sentence)
        if index == len(sentence): # end of sentence
            return self.get_trigram_probability(self.STOP, sentence[index-1], sentence[index-2])
        elif index == 0: # start of sentence
            return self.get_trigram_probability(sentence[0], self.START, self.START)
        elif index == 1: # 
            #print("1: " + str(sentence[1]) + " 2: " + str(sentence[0]) + " 3: " + self.START)
            return self.get_trigram_probability(sentence[1], sentence[0], self.START)
        else:
            return self.get_trigram_probability(sentence[index], sentence[index-1], sentence[index-2])

    def get_vocabulary(self):
        words = list(self.unigramcounts.keys())
        return words

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

# HELPER FUNCTIONS

    def get_trigram_probability(self, word, prev, prevtwo):
        if not (prevtwo, prev, word) in self.trigramcounts:
            return 0.0
        elif prevtwo == self.START and prev == self.START: # <s> <s> I 
            return float(self.trigramcounts[(prevtwo, prev, word)] / self.unigramcounts[self.STOP])
        elif prevtwo == self.START and prev != self.START: # <s> I am 
            return float(self.trigramcounts[(prevtwo, prev, word)] / self.bigramcounts[self.START, prev])
        else:
            return float(self.trigramcounts[(prevtwo, prev, word)] / self.bigramcounts[prevtwo, prev]) 
    
    def generate_word(self, prevtwo, prev):
        threshold = random.uniform(0, 1)
        sum = 0.0
        for word in self.unigramcounts.keys():
            sum += self.get_trigram_probability(word, prev, prevtwo)
            if sum > threshold:
                return word

#
# TESTING ONLY
#
if __name__ == '__main__':
    print('hi!')

