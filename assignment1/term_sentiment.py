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
    new_scores = {}
    for line in sent_file:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    for line in tweet_file:
        tweet = json.loads(line)
        tweet_scores = []
        if 'text' in tweet:
            tweet_scores = [scores[x] for x in tweet['text'].split() if x in scores]
            for term in [x for x in tweet['text'].split() if x not in scores]:
                if term not in new_scores:
                    new_scores[term] = 0
                new_scores[term] += reduce(lambda x,y: x+y, [0,0] + tweet_scores)
    for term in new_scores.keys():
        print term , new_scores[term]    


if __name__ == '__main__':
    main()
