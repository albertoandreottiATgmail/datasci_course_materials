from treelearner import TreeLearner

#Arbol
print 'Punto 2' 
print 'ID3'
print '''La idea es una funcion que calcule paridad sobre vectores de tres
       features.  
       Los datos son aleatorios y cada valor pertenece al alfabeto [0,1]'''

data = []

#Generate random data
#import random as rnd
#for n in xrange(30):
#    data.append([rnd.randint(0,1), rnd.randint(0,1), rnd.randint(0,1)])

#for sample in data:
#    parity = sample[0]  + sample[1]
#    parity = parity%2
#    sample.append(parity)

#replace random data with hardcoded values from assignment 1
data = [[1, 1, 0, 0], [0, 0, 0, 0], [1, 1, 1, 0], [1, 0, 0, 1], [0, 1, 0, 1], [1, 0, 1, 1], [0, 0, 0, 0],
[0, 1, 1, 1], [0, 1, 0, 1], [1, 1, 0, 0], [0, 0, 0, 0], [1, 0, 0, 1], [0, 1, 1, 1], [1, 1, 1, 0], 
[1, 1, 0, 0], [1, 1, 1, 0], [1, 0, 0, 1], [0, 0, 0, 0], [1, 0, 1, 1], [0, 0, 0, 0], [0, 0, 1, 0],
[0, 1, 1, 1], [0, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 1, 1], [0, 0, 0, 0], [1, 1, 1, 0], 
[0, 1, 0, 1], [0, 1, 0, 1]]

train = [False, False, True, True, False, True, True, False, True, True, False, True, False, True, False, True, False, True, True, False, True, False, False, True, True, False, True, False, True, False]

x_train = [data[i] for i in xrange(len(data)) if train[i]]

x_test = [data[i] for i in xrange(len(data)) if not train[i]]


print 'Los datos son de training son: '
for dato in x_train:
    print(str(dato) + '\n')

print 'Los datos son de test son: '
for dato in x_test:
    print(str(dato) + '\n')


tl = TreeLearner(x_train, 1)
tl.infer(1).plot("  ")
#print 'Prediction for ' + str([1, 0, 0, 1]) + ' is ' + str(tl.predict([1, 0, 0, 1]))

#Compute precision and recall
tp = fp = fn = 0.0

for datum in x_test:
    tp += tl.predict(datum) == 1 and datum[3] == 1
    fp += tl.predict(datum) == 1 and datum[3] == 0
    fn += tl.predict(datum) == 0 and datum[3] == 1

precision = tp/(tp + fp)
recall = tp/(tp + fn)

print 'precision = ' + str(precision)
print 'recall = ' + str(recall)

