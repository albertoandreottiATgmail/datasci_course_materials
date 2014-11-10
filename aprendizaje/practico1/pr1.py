

class NaiveBayes(object):
    def estimate(self, train, sample, smooth):
        m = float(len(train))
        count0 = len([1 for v in train if v[2]==0])
        count1 = len([1 for v in train if v[2]==1])
        
        
        pa0 = len([1 for v in train if v[2]==0 and v[0]==sample[0]]) / float(count0)
        pb0 = len([1 for v in train if v[2]==0 and v[1]==sample[1]]) / float(count0)
        pa1 = len([1 for v in train if v[2]==1 and v[0]==sample[0]]) / float(count1)
        pb1 = len([1 for v in train if v[2]==1 and v[1]==sample[1]]) / float(count1)

        if pa0 == 0.0:
            pa0 = smooth
         
        if pb0 == 0.0:
            pb0 = smooth
         
        if pa1 == 0.0:
            pa1 = smooth
         
        if pb1 == 0.0:
            pb1 = smooth
         
        #print str(pa0) + ' ' + str(pb0)+ ' ' + str(pa1) + ' ' +str(pb1) 
    
        if pa0 * pb0 > pa1 * pb1:
            return 0
        else:
            return 1

###           ###
#  Practico 1   #
###           ###
import random
data = [(5, 0, 1), (9, 1, 1), (4, 0, 1), (6, 0, 1), (4, 1, 1), (1,2, 0), (8,2,1), (7, 3, 1), (0,2,0), (2,3,1),
(4,1,1), (7,4,1), (8,1,1), (0,0,0), (9, 0, 1), (2, 3, 1), (4,4, 1), (9, 2, 1), (4, 1, 1), (7, 2, 1)]

datum = (1, 2)

#Bayes
print 'Punto 1' 
print 'Teorema de Bayes'
print 'Que los eventos inexistentes aparezcan 0.5 veces, significa que P((a,b)=(1,3) | c=1)) = P((a,b)=(1,3) | c=0)) = 0.5 '
target = [0, 0]
h = [0, 0]
target[0] = len(filter(lambda x: x[2] == 0, data))/float(len(data))
target[1] = 1 - target[0]
print 'P(h=0) = ' + str(target[0]), '   P(h=1) = ' + str(target[1])
h[0] = 0.5 * target[0]
h[1] = 0.5 * target[1]
print 'Entonces,'
print 'P((a,b)=(1,3) | c=0))*P(c=0) = ' + str(h[0])
print 'P((a,b)=(1,3) | c=1))*P(c=1) = ' + str(h[1])
print 'MAP predice c=1 para el dato en cuestion.'
print 'Para ML, tenemos, '
print 'P((a,b)=(1,3) | c=0)) = 0.5'
print 'P((a,b)=(1,3) | c=1)) = 0.5'
print 'Naive Bayes,'
randindexes = [random.randint(0,1) for x in xrange(0, len(data))]
subset1 = [data[i] for i in xrange(0, len(data)) if randindexes[i]==1]
subset2 = [data[i] for i in xrange(0, len(data)) if randindexes[i]==0]
assert(len(subset1) + len(subset2) == len(data))
print 'Split aleatorio de datos: ' 
print subset1
print subset2

tp = fp = fn = 0.0
smooth = 0.5
print 'con smoothing: ' + str(smooth) 
for datum in subset1:
    tp += NaiveBayes().estimate(subset2, datum, smooth) * datum[2]
    fp += NaiveBayes().estimate(subset2, datum, smooth) == 1 and datum[2] == 0
    fn += NaiveBayes().estimate(subset2, datum, smooth) == 0 and datum[2] == 1

precision = tp/(tp + fp)
recall = tp/(tp + fn)

print 'precision = ' + str(precision)
print 'recall = ' + str(recall)


tp = fp = fn = 0.0
smooth = 0.0001
print 'con smoothing: ' + str(smooth)
for datum in subset1:
    tp += NaiveBayes().estimate(subset2, datum, smooth) * datum[2]
    fp += NaiveBayes().estimate(subset2, datum, smooth) == 1 and datum[2] == 0
    fn += NaiveBayes().estimate(subset2, datum, smooth) == 0 and datum[2] == 1

precision = tp/(tp + fp)
recall = tp/(tp + fn)

print 'precision = ' + str(precision)
print 'recall = ' + str(recall)

