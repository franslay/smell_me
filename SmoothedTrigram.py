#inherit from trigram class
from TrigramModel import TrigramModel  #inherit from Trigram class
class SmoothedTrigram(TrigramModel):   # inherit all the TrigramModel goodies from Part 1

    def __init__(self):
        super().__init__()           # calls your parent's init function
        
        self.k = 3 # with interpolation USE THIS ONE
        # self.k = 0.00068 # with interpolation USE THIS ONE
        #self.k = 0.000905078 # with interpolation

        #self.k = 0.009050805
        #self.k = 0.0009

        # experimenting 
        #self.k = 0.0007
    
    def get_trigram_probability(self, word, prev, prevtwo):

        if not (prevtwo, prev, word) in self.trigramcounts: # if NOT in trigrams
            if (prevtwo, prev) in self.bigramcounts:
                return (self.k) / (self.bigramcounts[prevtwo, prev] + ((len(self.unigramcounts.keys())+1) * self.k))
            elif prevtwo == self.START and prev == self.START: # <s> <s> I (for example):
                return (self.k) / (self.unigramcounts[self.STOP] + ((len(self.unigramcounts.keys())+1) * self.k)) 
            else:
                return (self.k) / ((len(self.unigramcounts.keys())+1) * self.k)

        else: # if in trigramcounts
            if prevtwo == self.START and prev == self.START: # <s> <s> I (for example):
                return (self.trigramcounts[(prevtwo, prev, word)] + self.k) / (self.unigramcounts[self.STOP] + ((len(self.unigramcounts.keys())+1) * self.k))
            return (self.trigramcounts[(prevtwo, prev, word)] + self.k) / (self.bigramcounts[prevtwo, prev] + ((len(self.unigramcounts.keys())+1) * self.k))

    def get_vocabulary(self):
        words = list(self.unigramcounts.keys())
        #words.append(self.UNK)
        return words
#
# TESTING ONLY
#
if __name__ == '__main__':
    print('hi!')