
"""
    TreeLearner
"""

from math import log
import random


class TreeLearner():
    
    def __init__(self, samples, target):  # pylint: disable=E1002
        
        self._targetVal = target
        self._samples = samples
    
    # 'parameters' would be used to tell which features we can use
    def infer(self, target):        
        
        #target attribute is always the last one, its value is param 'target'
        self._targetAtt = target
        
        #mark the target as used
        used = [False] * (len(self._samples[0]) - 1) + [True] 

        #compute the tree, store it
        self._trainedTree = self._growTree(self._samples, used)        

        return self._trainedTree
        
    def _growTree(self, dataset, used):
        
        if(len(dataset) == 0):
            return Leaf(0, '','')
        #all positive
        if(len(filter(lambda x: x[-1] != self._targetVal, dataset))==0):
            return Leaf(1, self._targetVal)    
        #all negative
        if(len(filter(lambda x: x[-1] == self._targetVal, dataset))==0):
            return Leaf(1, 'other')
        
        #we run out of parameters and still classification is not good.
        if(reduce(lambda x, y: x and y, used)):
            return Leaf(0, '')
        
        # idx: location of the attribute in _samples, 
        idx = self._chooseBestAttribute(dataset, used)
        node = Node()
        used[idx] = True
        print used
        
        #split the data in as many subsets as values has the attribute.
        for value in [0, 1]:
            chunk = [it for it in dataset if it[idx] == value] 
            child = self._growTree(chunk, list(used))
            child.addAttVal(idx, value)
            node.addChild(child)
       
        return node
     
    def _chooseBestAttribute(self, dataset, used):
        assert(used[-1] == True)
        
        minfo = [0] * len(self._samples[0])

        
        #compute mutual information between the class and each attribute
        for idx in xrange(0, len(self._samples[0]) - 1):
            if not used[idx]:
                for value in [0, 1]:
                    subset = filter(lambda x: x[idx]==value, dataset)
                    val_prob = float(len(subset))/len(dataset)
                    if val_prob == 0:
                        continue
                    
                    #compute entropy
                    entropy = 0
                    for target in [0, 1]:
                        prob = float(len(filter(lambda x: x[-1] == target, subset)))/len(subset)
                        if prob > 0:
                            entropy += prob * log(prob) 
                    
                    #-P(B=b).H(A|B=b)
                    minfo[idx] += -val_prob * entropy
            else:
                #attributes already used must lose.
                minfo[idx] = float("inf")

        #do the actual choice according to minfo
        print minfo
        return min(enumerate(minfo[0: -1]), key=lambda x: x[1])[0]

    #predict the outcome for X
    def predict(self, X):
        return self._trainedTree.predict(X)
        
    
            
class Node(object):
    
    def __init__(self):
        self._children = []
        self._att = self._val = ''
        
    def addChild(self, child):
        self._children.append(child)
        
    def addAttVal(self, att, val):
        self._att = att
        self._val = val

    def toString(self):
        return 'Attribute: '+ str(self._att) + '   Value: ' + str(self._val)

    #Depth first search to plot
    def plot(self, tab):
        
        print tab + self.toString()
        for child in self._children:
            child.plot(tab + tab)        

    def predict(self, X):
        attribute = self._children[0]._att
        
        if X[attribute] == self._children[0]._val:
            return self._children[0].predict(X)
        else:
            return self._children[1].predict(X)

    
class Leaf(Node):

    def __init__(self, pos, targetVal):
        self._outcome = pos
        self._targetVal = targetVal

    def plot(self, tab):
        print tab + self.toString()
    
    def predict(self, X):
        return self._outcome
        

