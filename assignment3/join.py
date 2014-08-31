import MapReduce
import sys

"""
Join in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    order_id = record[1]
    mr.emit_intermediate(order_id, record)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    lines = filter(lambda x: x[0]=='line_item', list_of_values)
    orders = filter(lambda x: x[0]=='order', list_of_values)

    #Cartesian Product
    for key1 in orders:
        for key2 in lines:
            mr.emit(key1+key2)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
