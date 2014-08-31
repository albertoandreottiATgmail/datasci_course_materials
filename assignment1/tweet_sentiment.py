import sys
import json

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    
    scores = {} # initialize an empty dictionary
    for line in sent_file:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    for line in tweet_file:
        tweet = json.loads(line)
        tweet_scores = []
        if 'text' in tweet:
            tweet_scores = [scores[x] for x in tweet['text'].split() if x in scores]
        print str(reduce(lambda x,y: x+y, [0,0] + tweet_scores))
        
           
        

    #print scores.items() # Print every (term, score) pair in the dictionary

if __name__ == '__main__':
    main()
