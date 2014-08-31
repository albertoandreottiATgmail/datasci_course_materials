import MapReduce
import sys

"""
Matrix Multiply in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents

    if record[0] == 'a':
        for k in xrange(5):
            mr.emit_intermediate((record[1], k), record)            
    else:
        for k in xrange(5):
            mr.emit_intermediate((k, record[2]), record)            

 

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    a = filter(lambda x: x[0] == 'a', list_of_values)
    a = sorted(a, key = lambda x: x[2])

    b = filter(lambda x: x[0] == 'b', list_of_values)
    b = sorted(b, key = lambda x: x[1])

    idx1 = 0
    idx2 = 0
    sum = 0
    while idx1 < len(a) and idx2 < len(b):
        if a[idx1][2] == b[idx2][1]:
            sum += a[idx1][3] * b[idx2][3]
            idx2 += 1
            idx1 += 1
        elif a[idx1][2] > b[idx2][1]:
            idx2 += 1    
        else :
            idx1 += 1  

    mr.emit((key[0], key[1], sum))
# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
