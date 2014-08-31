import sys
import json
import operator


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    
    state_val = {}
    scores = {} # initialize an empty dictionary
    for line in sent_file:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    for line in tweet_file:
        tweet = json.loads(line)
        tweet_scores = []
        if 'text' in tweet:
            tweet_scores = [scores[x] for x in tweet['text'].split() if x in scores]
        
        val = reduce(lambda x,y: x+y, [0,0] + tweet_scores)
        state = findState(tweet)
        if state not in state_val:
            state_val[state] = 0.0

        state_val[state] += val
    state_val['ZZ'] = 0.0    
    print max(state_val.iteritems(), key=operator.itemgetter(1))[0]
           
def findState(tweet):

    if 'user' in tweet and 'location' in tweet['user']:
        for state in states.keys():
            if tweet['user']['location'].lower().find(states[state].lower()) >= 0:
                return state
            
        for state in states.keys():
            if tweet['user']['location'].find(state)  >= 0:
                return state
    return 'ZZ'    

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}






#print scores.items() # Print every (term, score) pair in the dictionary

if __name__ == '__main__':
    main()
