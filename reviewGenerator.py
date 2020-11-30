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
import os.path

# Helper Function to clean up passages
def preprocess_passage(passage):
        # need to preprocess text...
        passage = passage.lower() # might cause issues for names like Will
        #get rid of chapter? might cause issues for some authors who don't use chapters (like Shakespeare)
        #passage = passage.replace("chapter", " ") ###
        #remove garbage punctuation
        # passage = passage.replace('"', ' " ')
        # passage = passage.replace(',', ' , ')
        # passage = passage.replace(';', ' ; ')
        # passage = passage.replace(':', ' : ')
        # passage = passage.replace("'", " ' ")
        # passage = passage.replace("-", ' - ')
        # passage = passage.replace(" -  - ", ' -- ')
        # passage = passage.replace("_", '')
        # passage = passage.replace('\n', '')
        # # passage = passage.replace('#', '')
        # passage = passage.replace('“', '')
        # passage = passage.replace('‘', '')
        # passage = passage.replace('’', '')

        # #handle punctuation
        # # passage = passage.replace("[", " [ ")
        # # passage = passage.replace("]", " ] ")
        # # passage = passage.replace("(", " ( ")
        # # passage = passage.replace(")", " ) ")
        # # passage = passage.replace("/", " / ")
        # passage = passage.replace(".", " . ")
        # passage = passage.replace("?", " ? ") # treat ?,! as uniq tokens
        # passage = passage.replace("!", " ! ") # ^ do that for logreg
        # for i in range (0,4):
        #     passage = passage.replace('  ', ' ')

        return passage

def read_sentences(path):
    print("Loading", path)
    sents = []
    for line in open(path):
        processedline = preprocess_passage(line)
        tokens = processedline.strip().lower().split()
        sents.append(tokens)
    return sents
            
if __name__ == '__main__':
    if not os.path.isfile("data/amberpositive.txt"): # check if you have already downloaded training files
        os.system('python3 Scrape3.py') #scrape reviews if no files
        
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
    # print(args)
    
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

    # Generate sentences.
    # if args.generate:

    print('\nREVIEW:')
    for i in range(7):
        s = model.generate_sentence()
        if len(s) > 100:
            s = s[0:100]
            s.append(' CUTTING OFF TOO LONG...')
        for t in s:
            print(t, end=' ')
        print()
