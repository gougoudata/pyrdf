#from numpy import asscalar, sqrt, dot

#def calcDist(point1, point2):
#  return sqrt(sum([(c1 - c2)**2 for (c1, c2) in zip(point1, point2)]))

# Return the norm2 distance of vector (1xm or mx1 matrix)
#def norm2distance(vector):
#  return sqrt(asscalar(dot(vector, vector.T)))

# Return the normalized vector (1xm or mx1 matrix)
#def normalize(vector):
#  return vector/norm2distance(vector)

# Convert a row matrix of shapw (1xm) to tuple
#def convertRowMatrixToTuple(aRowMatrix):
#  if aRowMatrix.shape[0] == 1:
#    return tuple(aRowMatrix.tolist()[0])

# Function returning tuple filled with zeros
def zeroTuple(dimension):
  if not isinstance(dimension, int):
    ValueError('dimension is not interger')
  if dimension <= 0:
    ValueError('dimension <= 0')
  if dimension == 1:
    return (0,)
  else:
    return zeroTuple(dimension - 1) + (0,)

# Return the list containing the intersection of two lists
def intersectionOfLists(listA, listB):
  return [val for val in listA if val in listB]

# Return list of tuples specified by rangeTuple
# where rangeTuple is of the form ((xStart, xEnd), (yStart, yEnd) ...)
# not including xEnd s.t. (0, 1) just includes 0
def exhaustiveListInRange(rangeTuple):
  # If empty:
  if not rangeTuple:
    return [()]
  # If non empty:
  else:
    tmpList = []
    currentDim = len(rangeTuple) - 1
    for lastTuple in exhaustiveListInRange(rangeTuple[:currentDim]):
      for index in range(rangeTuple[currentDim][0], rangeTuple[currentDim][1]):
        tmpList.append(lastTuple + (index,))
    return tmpList
