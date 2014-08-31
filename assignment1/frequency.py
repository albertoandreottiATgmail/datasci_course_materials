import sys
import json


def main():

    tweet_file = open(sys.argv[1])
    count = {} # initialize an empty dictionary
    total = 0


    for line in tweet_file:
        tweet = json.loads(line)
        if 'text' in tweet:
            for term in tweet['text'].split():
                total += 1
                if term not in count:
                    count[term] = 0.0
                count[term] += 1
    freqs = {k:count[k]/total for k in count.keys()}
    
    for term in freqs.keys():
        print term , freqs[term]  

if __name__ == '__main__':
    main()
