# coding: utf-8
"""
Benchmarks for the Avito fraud detection competition
"""
import csv
import re
import nltk.corpus
from collections import defaultdict
import scipy.sparse as sp
import numpy as np
import os
from sklearn.linear_model import SGDClassifier
from nltk import SnowballStemmer
import random as rnd 
import logging
from sklearn.externals import joblib
from sklearn.metrics import roc_auc_score

dataFolder = "/home/guest/Downloads/dataset"

stopwords= frozenset(word.decode('utf-8') for word in nltk.corpus.stopwords.words("russian") if word!="не")    
stemmer = SnowballStemmer('russian')
engChars = [ord(char) for char in u"cCyoOBaAKpPeE"]
rusChars = [ord(char) for char in u"сСуоОВаАКрРеЕ"]
eng_rusTranslateTable = dict(zip(engChars, rusChars))
rus_engTranslateTable = dict(zip(rusChars, engChars))

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)
        
def correctWord (w):
    """ Corrects word by replacing characters with written similarly depending on which language the word. 
        Fraudsters use this technique to avoid detection by anti-fraud algorithms."""

    if len(re.findall(ur"[а-я]",w))>len(re.findall(ur"[a-z]",w)):
        return w.translate(eng_rusTranslateTable)
    else:
        return w.translate(rus_engTranslateTable)

def getItems(fileName, itemsLimit=None):
    """ Reads data file. """
    
    with open(os.path.join(dataFolder, fileName)) as items_fd:
        logging.info("Sampling...")
        if itemsLimit:
            countReader = csv.DictReader(items_fd, delimiter='\t', quotechar='"')
            numItems = 0
            for row in countReader:
                numItems += 1
            items_fd.seek(0)        
            rnd.seed(0)
            sampleIndexes = set(rnd.sample(range(numItems),itemsLimit))
            
        logging.info("Sampling done. Reading data...")
        itemReader=csv.DictReader(items_fd, delimiter='\t', quotechar = '"')
        itemNum = 0
        for i, item in enumerate(itemReader):
            item = {featureName:featureValue.decode('utf-8') for featureName,featureValue in item.iteritems()}
            if not itemsLimit or i in sampleIndexes:
                itemNum += 1
                yield itemNum, item
                
    
def getWords(text, stemmRequired = False, correctWordRequired = False):
    """ Splits the text into words, discards stop words and applies stemmer. 
    Parameters
    ----------
    text : str - initial string
    stemmRequired : bool - flag whether stemming required
    correctWordRequired : bool - flag whether correction of words required     
    """

    cleanText = re.sub(u'[^a-zа-я0-9]', ' ', text.lower())
    if correctWordRequired:
        words = [correctWord(w) if not stemmRequired or re.search("[0-9a-z]", w) else stemmer.stem(correctWord(w)) for w in cleanText.split() if len(w)>1 and w not in stopwords]
    else:
        words = [w if not stemmRequired or re.search("[0-9a-z]", w) else stemmer.stem(w) for w in cleanText.split() if len(w)>1 and w not in stopwords]
    
    return words

def processData(fileName, featureIndexes={}, itemsLimit=None, useIt=[]):
    """ Processing data. """
    processMessage = ("Generate features for " if featureIndexes else "Generate features dict from ")+os.path.basename(fileName)
    logging.info(processMessage+"...")

    wordCounts = defaultdict(lambda: 0)
    targets = []
    item_ids = []
    row = []
    col = []
    cur_row = 0
    for processedCnt, item in getItems(fileName, itemsLimit):
        if useIt and not useIt[processedCnt]:
            continue
        #col = []
        for word in getWords(item["title"]+" "+item["description"], stemmRequired = False, correctWordRequired = False):
            if not featureIndexes:
                wordCounts[word] += 1
            else:
                if word in featureIndexes:
                    col.append(featureIndexes[word])
                    row.append(cur_row)
        
        cur_row += 1
        if featureIndexes:
            if "is_blocked" in item:
                targets.append(int(item["is_blocked"]))
            item_ids.append(int(item["itemid"]))
                    
        if cur_row%500 == 0:                 
            logging.debug(processMessage+": "+str(cur_row)+" items done")
                
    if not featureIndexes:
        index = 0
        for word, count in wordCounts.iteritems():
            if count>=3:
                featureIndexes[word]=index
                index += 1
                
        return featureIndexes
    else:
        features = sp.csr_matrix((np.ones(len(row)),(row,col)), shape=(cur_row, len(featureIndexes)), dtype=np.float64)
        if targets:
            return features, targets, item_ids
        else:
            return features, item_ids


def treshold(value, limit = 0.5):
    if value > limit:
        return 1
    else:
        return 0

def main():
    """ Generates features and fits classifier. """
    iLimit=310000

    #randomly separate a third of the training set for testing
    useIt = [False] * (iLimit + 1)
    for idx in xrange(iLimit):
        useIt[idx] = rnd.randint(0,9) > 2

    featureIndexes = processData(os.path.join(dataFolder, "avito_train.tsv"), itemsLimit = iLimit)
    trainFeatures,trainTargets, trainItemIds = processData(os.path.join(dataFolder,"avito_train.tsv"), featureIndexes, itemsLimit=iLimit, useIt = useIt)
    testFeatures, testTargets, testItemIds = processData(os.path.join(dataFolder,"avito_train.tsv"), featureIndexes, itemsLimit=iLimit, useIt = [not x for x in useIt])
    
    #Dump everything to disk
    joblib.dump((trainFeatures, trainTargets, trainItemIds, testFeatures, testTargets, testItemIds), os.path.join(dataFolder,"train_data.pkl"))
    #trainFeatures, trainTargets, trainItemIds, testFeatures, testTargets, testItemIds = joblib.load(os.path.join(dataFolder,"train_data.pkl"))
    
    #randomly separate a third of the training set for testing

    logging.info("Feature preparation done, fitting model...")
    clf = SGDClassifier(    loss="log", 
                            penalty="l2", 
                            alpha=1e-4, 
                            class_weight="auto")
    clf.fit(trainFeatures,trainTargets)

    logging.info("Predicting...")
    
    predicted_scores = clf.predict_proba(testFeatures).T[1]
    predicted_scores = map(treshold, predicted_scores)
    correct = 0.0
    for tuple in zip(predicted_scores, testTargets):
        if tuple[0]==tuple[1]:
            correct += 1

    print correct / len(testTargets)
       
    logging.info("Write results...")
    output_file = "avito_starter_solution.csv"
    logging.info("Writing submission to %s" % output_file)
    f = open(os.path.join(dataFolder,output_file), "w")
    f.write("id\n")
    
    for pred_score, item_id in sorted(zip(predicted_scores, testItemIds), reverse = True):
        f.write("%d\n" % (item_id))
    f.close()
    logging.info("Done.")
                               
if __name__=="__main__":            
    main()            
    
    
    
