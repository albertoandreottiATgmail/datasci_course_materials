import sys
import json
import operator

def main():

    tweet_file = open(sys.argv[1])
    count = {} # initialize an empty dictionary
    total = 0

    for line in tweet_file:
        tweet = json.loads(line)
        if 'entities' in tweet and 'hashtags' in tweet['entities']:
            for tag in tweet['entities']['hashtags']:
                total += 1
                if tag['text'] not in count:
                    count[tag['text']] = 0.0
                count[tag['text']] += 1

    freqs = {k:count[k] for k in count.keys()}

    top_ten = sorted(freqs.iteritems(), key=operator.itemgetter(1))
    top_ten.reverse()
    for term in top_ten[0:10]:
        print term[0] , term[1]  

if __name__ == '__main__':
    main()
