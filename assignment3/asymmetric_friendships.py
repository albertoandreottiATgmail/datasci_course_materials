import MapReduce
import sys

"""
Friends in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents

    if record[0] > record[1]:
        key = record[0]+record[1]
    else:
        key = record[1]+record[0]
 
    mr.emit_intermediate(key, record)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    if len(list_of_values)==1:
        mr.emit((list_of_values[0][0], list_of_values[0][1]))
        mr.emit((list_of_values[0][1], list_of_values[0][0]))

    
# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
