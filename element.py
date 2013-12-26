"""Element"""

name = \
[ None, 'H', 'He',\
  'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',\
  'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar',\
  'K', 'Ca',\
  'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',\
  'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',\
  'Rb', 'Sr',\
  'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd',\
  'In', 'Sn', 'Sb', 'Te', 'I', 'Xe',\
  'Cs', 'Ba',\
  'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu',\
  'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb',\
  'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',\
  'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn',\
  'Fr', 'Ra',\
  'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am',\
  'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No',\
  'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn',\
  'Uut', 'Fl', 'Uup', 'Lv', 'Uus', 'Uuo',\
]

def findnum(s):
  return name.index(s)

def findname(n):
  return name[n]

# mass per mole in gram
mass = [
1.008, 4.0026,\
]

class element:

  # num should be between 1 to 118
  def __init__(self, name):
    self.num = findnum(name)

  def name(self):
    return findname(self.num)

  def __key(self):
    return (self.num)

  def __eq__(self, other):
    return type(self) == type(other) and self.__key() == other.__key()

  def __ne__(self, other):
    return not self.__eq__(other)

  def __hash__(self):
    return hash(self.__key())

  def __str__(self):
    return name[self.num]

  def __repr__(self):
    return str(self)

  def mass(self):
    return mass[self.num]

