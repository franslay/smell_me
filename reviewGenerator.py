# 
# Assumes the following files will exist:
#   BigramModel.py
#   TrigramModel.py
#   SmoothedBigram.py
#   SmoothedTrigram.py
#   LinearInterpolation.py
#
# python3 SentenceGenerator.py -h 
#
# @author Krystal Kim, Franchette Allarey
# Modified from NLP Lab 2 code
#
import math
import argparse
import sys
from UnigramModel import UnigramModel


def read_sentences(path):
    print("Loading", path)
    sents = []
    for line in open(path):
        tokens = line.strip().lower().split()
        sents.append(tokens)
    return sents


def verify_distribution(model):
    contexts = []
    contexts.append( [ ] )
    contexts.append( [ 'united' ] )    
    contexts.append( [ 'to', 'the' ] )
    contexts.append( [ 'the', 'quick', 'brown' ] )
    contexts.append( [ 'lalok', 'nok', 'crrok' ] )        

    for c in contexts:
        print('Testing context', c, end=' ...')
        modelsum = model.check_probability(c)
        if abs(1.0-modelsum) < 1e-6:
            print('GOOD! Probability distribution sums up to one')
        else:
            print('ERROR: probability distribution does not sum up to one, sum =', modelsum)


            
if __name__ == '__main__':

    # User input
    userfrag = input("What is the name of your fragrance?: ")
    # force feed into vocabulary to make it say something about the fragrance
    useraccord = input("\nPick one accord.\n[Choices: amber, animalic, aromatic, citrus, floral, fruity, green, lavender, leather, musky, powdery, rose, spicy, sweet, vanilla, woody]:\n")
    accordlist = ["amber", "animalic", "aromatic", "citrus", "floral", "fruity", "green", "lavender", "leather", "musky", "powdery", "rose", "spicy", "sweet", "vanilla", "woody"]
    while not useraccord in accordlist:
        print()
        useraccord = input("Please pick a valid accord.\n[Choices: amber, animalic, aromatic, citrus, floral, fruity, green, lavender, leather, musky, powdery, rose, spicy, sweet, vanilla, woody]:\n")

    usersentiment = input("\nDo you like your fragrance?\n[Choices: yes, no, idk]:\n")
    while not (usersentiment == "yes" or usersentiment == "no" or usersentiment == "idk"):
        print()
        useraccord = input("Please pick a valid option.\n[Options: yes, no, idk]:\n")
    
    sentiment = ""
    if usersentiment == "yes":
        sentiment = "positive"
    elif usersentiment == "no":
        sentiment = "negative"
    else:
        sentiment = "neutral"

    print()
    # Argument parser
    accordfile = 'data/'+useraccord+sentiment+'.txt' 

    parser = argparse.ArgumentParser(description="reviewGenerator.py")
    parser.add_argument('-model', action="store", dest="model", type=str, choices=['unigram','bigram','trigram','smoothbi','smoothtri','interp'], default='interp', help='Type of LM to load')    
    parser.add_argument('-train', action="store", dest="train", type=str, default=accordfile, help='Path to file with training sentences')
    # parser.add_argument('-test', action="store", dest="test", type=str, default='data/reviews.txt', help='Path to file with test sentences')
    parser.add_argument('-generate', type=eval, choices=[True,False], default=True, help='Generate sentences if True')        

    # Parse the command-line arguments.
    args = parser.parse_args()
    print(args)
    
    # Load the sentences
    if len(args.train) > 2:
        trainset = read_sentences(args.train)

    # Create the model
    if args.model == 'unigram':
        model = UnigramModel()
    elif args.model == 'bigram':
        import BigramModel
        model = BigramModel.BigramModel()
    elif args.model == 'trigram':
        import TrigramModel
        model = TrigramModel.TrigramModel()
    elif args.model == 'smoothbi':
        import SmoothedBigram
        model = SmoothedBigram.SmoothedBigram()
    elif args.model == 'smoothtri':
        import SmoothedTrigram
        model = SmoothedTrigram.SmoothedTrigram()
    elif args.model == 'interp':
        import LinearInterpolation
        model = LinearInterpolation.LinearInterpolation()
    model.train(trainset)

    # Sanity check that the model is implemented:
    if model.get_vocabulary() == None:
        print('ERROR: get_vocabulary() didn''t return a dictionary')
        sys.exit()
    
    # Check for proper probability distributions.
    # print('\nChecking for proper probability distributions:')
    # verify_distribution(model)

    # Generate sentences.
    if args.generate:

        print('\nGenerating sentences (do these look good?):')
        for i in range(6):
            s = model.generate_sentence()
            if len(s) > 100:
                s = s[0:100]
                s.append(' CUTTING OFF TOO LONG...')
            for t in s:
                print(t, end=' ')
            print()
