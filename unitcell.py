"""Unit cell"""

# maxrand for mutate_lc
mr = 0.5

def randm1p1():
  from random import random
  return (2*random() - 1.0)

class unitcell:

  def swaplc(self):
    tmp = self.b
    self.b = self.c
    self.c = tmp
    for a in self.alist:
      c = a.coor
      tmp = c[1]
      c[1] = c[2]
      c[2] = tmp

  # alist is a list of atoms
  def __init__(self, a, b, c, alist):
    self.a = a
    self.b = b
    self.c = c
    self.alist = alist
    if self.volume() < 0:
      self.swaplc()
 
  def angles(self):
    xy = self.a.dot(self.b)
    xz = self.a.dot(self.c)
    yz = self.b.dot(self.c)
    xnorm = self.a.norm(); ynorm = self.b.norm(); znorm = self.c.norm()
    cosg = xy/xnorm/ynorm
    cosb = xz/xnorm/znorm
    cosa = yz/ynorm/znorm
    from math import acos, pi
    c = 180/pi
    return (c*acos(cosa), c*acos(cosb), c*acos(cosg))

  def volume(self):
    x = self.a.value
    y = self.b.value
    z = self.c.value
    yz = (y[1]*z[2]-y[2]*z[1], y[2]*z[0]-y[0]*z[2], y[0]*z[1]-y[1]*z[0])
    return x[0]*yz[0] + x[1]*yz[1] + x[2]*yz[2]

  def scale(self, s):
    self.a = self.a * s
    self.b = self.b * s
    self.c = self.c * s

  # convertToPoscar
  def convertToPoscar(self, selectiveDynamics = False):
    from poscar import poscar
    latticeVectors = [list(self.a.value), \
                      list(self.b.value), \
                      list(self.c.value)]
    elementDict = self.elementDict()
    # Converted the list to fit poscar
    reducedCoorList = [list(x.value) for x in self.listOfReducedCoor()]
    elementsLabel = map(str, elementDict.keys())
    elementsNumber = map(len, elementDict.values())
    return poscar.initFromPara(1.0, latticeVectors, elementsLabel,\
                               elementsNumber, selectiveDynamics, "Direct",\
                               reducedCoorList)
  
  # Return element -> list of atom dictionary
  def elementDict(self):
    elementDict = {}
    for atom in self.alist:
      element = atom.element
      if element not in elementDict:
        elementDict[element] = [atom]
      else:
        elementDict[element].append(atom)
    return elementDict

  # Return the list of reduced coordinates
  def listOfReducedCoor(self, element=None):
    elementDict = self.elementDict()
    if element is None:
      return [a.coor\
        for alist in elementDict.values() for a in alist]
    else:
      return [a.coor for a in elementDict[element]]

  # Return the list of cartesian coordinates
  def listOfCartCoor(self, element=None):
    if element is None:
      lrc = self.listOfReducedCoor()
    else:
      self.alist
      lrc = self.listOfReducedCoor(element)
    return [self.a*rc[0] + self.b*rc[1] + self.c*rc[2] for rc in lrc]

  # Return list of coordinates in domain to search
  # domain defined by multiples of a, b, c contains the sphere r
  def listOfCartCoorDomain(self, r, element=None):
    an = abs(self.a); bn = abs(self.b); cn = abs(self.c)
    from math import ceil
    i = int(ceil(r/an)); j = int(ceil(r/bn)); k = int(ceil(r/cn))
    from common import exhaustiveListInRange
    el =  exhaustiveListInRange(((-i, i+1), (-j, j+1), (-k, k+1)))
    # Contain everything if element is None or not specified
    if element is None:
      lc = self.listOfCartCoor()
      return [self.a*e[0] + self.b*e[1] + self.c*e[2] + cc\
        for e in el for cc in lc]
    else:
      lc = self.listOfCartCoor(element)
      return [self.a*e[0] + self.b*e[1] + self.c*e[2] + cc\
        for e in el for cc in lc]

  # Fingerprint
  def fp(self, r, elementpair=None):
    from kdtree import kdtree
    res = 0.01
    if elementpair is None:
      lcs = self.listOfCartCoorDomain(r)
      lc = self.listOfCartCoor()
    else:
      lcs = self.listOfCartCoorDomain(r, elementpair[0])
      lc = self.listOfCartCoor(elementpair[1])
    #from math import log
    #N = len(lcs); q = len(lc)
    #print N, q
    # If the number of query, q, is too small
    # it does not worth to construct the kdtree, 3 dimensional (k = 3)
    # kNlogN > qN -> logN > q/k
    #if 3*log(N) > q:
    #  return self.fp_bf(r)
    kd = kdtree(lcs)
    tmp = []
    for c in lc:
      tmp = tmp + kd.rangeSearch(c, r)[1]
    tmp = map(lambda a: res*int(a/res), tmp)
    return sorted(tmp)

  # Calculating fingerprint using brute force
  def fp_bf(self, r, elementpair=None):
    res = 0.01
    if elementpair is None:
      lcs = self.listOfCartCoorDomain(r)
      lc = self.listOfCartCoor()
    else:
      lcs = self.listOfCartCoorDomain(r, elementpair[0])
      lc = self.listOfCartCoor(elementpair[1])
    near = []
    for c in lc:
      for cs in lcs:
        d = res*int(abs(c-cs)/res)
        if d < r:
          near.append(d)
    return sorted(near)

  # Determine if angle too large
  def angleTooLarge(self):
    if any(a > 130 or a < 50 for a in self.angles()):
      return True
    return False

  # Determine if atoms are too close
  def atomTooClose(self):
    # Since maxR == 2.6
    e = self.elementDict()
    el = e.keys()
    selfep = []
    for e in el:
      selfep.append((e, e))
    from pyrdf.orbitalRadii import mapO
    import itertools
    for ep in list(itertools.combinations(el, 2))+selfep:
      m1 =  max(mapO[ep[0].name()]); m2 = max(mapO[ep[1].name()])
      gauge = 1.2*(m1 + m2)
      l = self.fp_bf(10.0, ep)
      zl = [x for x in l if x == 0]
      nzl = [x for x in l if x != 0]
      if len(zl) > len(self.alist):
        return True
      # If nzl is not empty
      if nzl:
        d = min(nzl)
        if d < gauge:
          return True
    return False

  # Validate unitcell
  def validate(self):
    #print "tooclose:", self.atomTooClose()
    #print "toowide:", self.angleTooLarge()
    if not self.atomTooClose() and not self.angleTooLarge():
      return True
    return False

  # Mutate cell parameters
  def mutate_lc(self):
    from random import random
    # construct symmetric matrix o
    a11 = mr*randm1p1(); a12 = mr*randm1p1(); a13 = mr*randm1p1()
    a22 = mr*randm1p1(); a23 = mr*randm1p1(); a33 = mr*randm1p1()
    from pyrdf.coor import coor
    o_a = coor((1+a11, a12, a13))
    o_b = coor((a12, 1+a22, a23))
    o_c = coor((a13, a23, 1+a33))
    self.a = coor((o_a.dot(self.a), o_b.dot(self.a), o_c.dot(self.a)))
    self.b = coor((o_a.dot(self.b), o_b.dot(self.b), o_c.dot(self.b)))
    self.c = coor((o_a.dot(self.c), o_c.dot(self.c), o_c.dot(self.c)))

  # Mutate swap atom
  def mutate_sa(self):
    natom = len(self.alist) 
    from math import sqrt
    # Swap for sqrt(natom) times
    for i in range(int(sqrt(natom))):
      from random import randrange
      idx1 = randrange(natom); idx2 = randrange(natom)
      # Swapping the atoms
      tmp = self.alist[idx1]
      self.alist[idx1] = self.alist[idx2]
      self.alist[idx2] = tmp

  # Mutate cell
  def mutate(self):
    self.mutate_lc()
    self.mutate_sa()
    return self.__class__(self.a, self.b, self.c, self.alist)

  # Mate unitcell with the other unitcell
  def mate(self, other):

    assert(len(self.alist) == len(other.alist))

    from random import random, randrange
    r = random(); s = (1-r)
    # x child1, linear combination
    x_a = self.a * r + other.a * s
    x_b = self.b * r + other.b * s
    x_c = self.c * r + other.c * s
    # y child2, linear combination
    y_a = self.a * s + other.a * r
    y_b = self.b * s + other.b * r
    y_c = self.c * s + other.c * r

    cut1 = random(); cut2 = random();
    # WLOG, cut1 < cut2; else swap
    if (cut1 > cut2):
      tmp = cut1; cut1 = cut2; cut2 = tmp

    c1a = []; c2a = []

    natom = len(self.alist)

    # Choose a random direction of cut
    d = randrange(3)
    from copy import deepcopy
    
    c1a = c1a + [deepcopy(a) for a in self.alist if a.coor[d] > cut1 and a.coor[d] < cut2]
    c2a = c2a + [deepcopy(a) for a in self.alist if a.coor[d] < cut1 or a.coor[d] > cut2]
    c1a = c1a + [deepcopy(a) for a in other.alist if a.coor[d] < cut1 or a.coor[d] > cut2]
    c2a = c2a + [deepcopy(a) for a in other.alist if a.coor[d] > cut1 and a.coor[d] < cut2]

    c1 = unitcell(x_a, x_b, x_c, c1a)
    c2 = unitcell(y_a, y_b, y_c, c2a)

    return c1, c2

  def __str__(self):
    s = ''
    for a in self.alist:
      s = s+str(a)+'\n'
    return str(self.a) + '\n' + str(self.b) + '\n'\
      + str(self.c) + '\n'+ s

def randcell_novalidate(volume, elementList):
  from pyrdf.atom import atom
  from pyrdf.coor import randcoor
  al = []
  for e in elementList:
    al.append(atom(e, randcoor()))
  uc = unitcell(randcoor(), randcoor(), randcoor(), al)
  s = (volume/uc.volume())**(1/3.)
  uc.scale(s)
  return uc

# Given volume, generate validate random unitcell
def randcell(volume, elementList):
  uc = randcell_novalidate(volume, elementList)
  # Random cell should make sure that cell is validate one
  while not uc.validate():
    uc = randcell_novalidate(volume, elementList)
  return uc
  
