"""Atom"""

class atom:

  def __init__(self, element, coor):
    self.element = element
    self.coor = coor

  # string representation
  def __str__(self):
    return str(self.element) + '@' + str(self.coor)

  def __key(self):
    return (self.element, self.coor)

  def __eq__(self, other):
    return type(self) == type(other) and self.__key() == other.__key()

  def __ne__(self, other):
    return not self.__eq__(other)

  def __repr__(self):
    return str(self)
