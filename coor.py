"""Coordinate"""

class coor:

  # constructor
  def __init__(self, value):
    self.value = value

  # string representation
  def __str__(self):
    return str(self.value)

  def __key(self):
    return (self.value)

  def __hash__(self):
    return hash(self.__key())

  def __eq__(self, other):
    return type(self) == type(other) and self.__key() == other.__key()

  def __ne__(self, other):
    return not self.__eq__(other)

  def __add__(self, other):
    v = tuple([x1+x2 for x1, x2 in zip(self.value, other.value)])
    return self.__class__(v)

  def __sub__(self, other):
    v = tuple([x1-x2 for x1, x2 in zip(self.value, other.value)])
    return self.__class__(v)

  def __mul__(self, num):
    v = tuple([num * x for x in self.value])
    return self.__class__(v)
    
  def dot(self, other):
    return sum([x1*x2 for x1, x2 in zip(self.value, other.value)])

  def norm(self):
    from math import sqrt
    return sqrt(sum([x*x for x in self.value]))

  def __abs__(self):
    return self.norm()

  def __repr__(self):
    return str(self)

  def __getitem__(self, i):
    return self.value.__getitem__(i)

  def __setitem__(self, i, v):
    l = list(self.value)
    l[i] = v
    self.value = tuple(l)

  def __len__(self):
    return len(self.value)

def randcoor():
  from random import random
  return coor((random(), random(), random()))
