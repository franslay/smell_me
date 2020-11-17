from BigramModel import BigramModel  #inherit from bigram class

class SmoothedBigram(BigramModel):   # inherit all the BigramModel goodies from Part 1

    def __init__(self):
        super().__init__()           # calls your parent's init function
        
        #self.vocablen = len(self.get_vocabulary())

        self.k = .0001
        #self.k = 0.0088 # just for bigram
        # self.k = 0.0005 # USE THIS ONE

        # experimenting
        #self.k = 0.00005
    
    def get_bigram_probability(self, word, prev):

        if not (prev, word) in self.bigramcounts: # word pair NOT in bigramcounts
            if prev in self.unigramcounts:
                return (self.k) / (self.unigramcounts[prev] + ((len(self.unigramcounts.keys())+1) * self.k))
            elif prev == self.START: # self.START is NOT in unigramcounts --> count self.STOP
                return (self.k) / (self.unigramcounts[self.STOP] + ((len(self.unigramcounts.keys())+1) * self.k)) 
            else:
                #return (self.k) / (len(self.vocablen) * self.k)
                return (self.k) / ((len(self.unigramcounts.keys())+1) * self.k)
        else: # (prev, word) in bigramcounts
            if prev == self.START: # self.START is NOT in unigramcounts --> count self.STOP
                return (self.bigramcounts[(prev, word)] + self.k) / (self.unigramcounts[self.STOP] + ((len(self.unigramcounts.keys())+1) * self.k))
            return (self.bigramcounts[(prev, word)] + self.k) / (self.unigramcounts[prev] + ((len(self.unigramcounts.keys())+1) * self.k)) 

    def get_vocabulary(self):

        words = list(self.unigramcounts.keys())
        words.append(self.UNK)
        return words
    
    #def return_vocablen(self):
    #   return vocablen

#
# TESTING ONLY
#
if __name__ == '__main__':
    print('hi!')