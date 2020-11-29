from bs4 import BeautifulSoup
import urllib
import re
import sys
from urllib.request import Request, urlopen

# Opening file 
perfumesfile = open("data/updated_fraglist.txt", 'r')
  
# Using for loop 
for line in perfumesfile: 
    N = len(line)
    l = line.split(" ")
    url = l[0]
    accordlist = l[1:N]

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "html.parser")

    original_stdout = sys.stdout # Save a reference to the original standard output

    with open('data/reviews.txt', 'a') as f:
        sys.stdout = f

        # print("***POSITIVE REVIEWS***")
        # print("----------")
        for review in soup.findAll('div', attrs={'class':'reviewmain review3'}): # positive = review3
            comment = review.find('div', attrs={'class':'reviewblurb'}) # review comment 
            print("positive", comment.text, accordlist) # ".text" grabs just the text inside HTML tag
            # print("----------")

        print()
        # print("***NEGATIVE REVIEWS***")
        # print("----------")
        for review in soup.findAll('div', attrs={'class':'reviewmain review1'}): # negative = review1 
            comment = review.find('div', attrs={'class':'reviewblurb'}) # review comment
            print("negative", comment.text, accordlist) # ".text" grabs just the text inside HTML tag
            # print("----------")

        print()
        # print("***NEUTRAL REVIEWS***")
        # print("----------")
        for review in soup.findAll('div', attrs={'class':'reviewmain review2'}): # negative = review1 
            comment = review.find('div', attrs={'class':'reviewblurb'}) # review comment
            print("neutral", comment.text, accordlist) # ".text" grabs just the text inside HTML tag
            # print("----------")
        
        sys.stdout = original_stdout # Reset the standard output to its original value




