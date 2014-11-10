from sklearn.ensemble import RandomForestClassifier
import random as rnd

X = [[1, 1, 0], [0, 0, 0], [1, 1, 1], [1, 0, 0], [0, 1, 0], [1, 0, 1], [0, 0, 0], [0, 1, 1],
     [0, 1, 0], [1, 1, 0], [0, 0, 0], [1, 0, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0], [1, 1, 1],
     [1, 0, 0], [0, 0, 0], [1, 0, 1], [0, 0, 0], [0, 0, 1], [0, 1, 1], [0, 1, 1], [0, 0, 0],
     [0, 0, 0], [1, 0, 1], [0, 0, 0], [1, 1, 1], [0, 1, 0], [0, 1, 0]]

Y = [0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1]

train = [rnd.random()>0.5 for x in xrange(len(Y))]
train = [False, False, True, True, False, True, True, False, True, True, False, True, False, True, False, True, False, True, True, False, True, False, False, True, True, False, True, False, True, False]

x_train = [X[i] for i in xrange(len(Y)) if train[i]]
y_train = [Y[i] for i in xrange(len(Y)) if train[i]]
x_test = [X[i] for i in xrange(len(Y)) if not train[i]]
y_test = [Y[i] for i in xrange(len(Y)) if not train[i]]


clf = RandomForestClassifier(n_estimators = 3, criterion='entropy', max_features = 2)
clf = clf.fit(x_train, y_train)
outcome = clf.predict(x_test)

#Compute precision and recall
x_test = [X[i] + [Y[i]] for i in xrange(len(Y)) if not train[i]]
tp = fp = fn = 0.0
for idx in xrange(len(outcome)):
    tp += outcome[idx] == 1 and y_test[idx] == 1
    fp += outcome[idx] == 1 and y_test[idx] == 0
    fn += outcome[idx] == 0 and y_test[idx] == 1

precision = tp/(tp + fp)
recall = tp/(tp + fn)

print 'precision = ' + str(precision)
print 'recall = ' + str(recall)

