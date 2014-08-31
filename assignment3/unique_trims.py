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

 
    mr.emit_intermediate(record[1][0:len(record[1])-10], record[1][0:len(record[1])-10])

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    mr.emit(list_of_values[0])
    
    
# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
