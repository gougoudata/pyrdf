"""
  Implements incar
"""

KnownKeySet = \
set([
'NWRITE',     'ISTART',     'ICHARG',     'INIWAV',     'ISPIN',\
'PREC',       'ENCUT',      'EDIFF',      'NELMIN',     'LREAL',\
'ALGO',       'NSW',        'IBRION',     'EDIFFG',     'ISIF',\
'ISYM',       'ISMEAR',     'SIGMA',      'LWAVE' ,     'NELM',\
'LPLANE',     'NPAR',       'LCHARG',
])

class incar():

  initKey = {}

  initKey['relax'] = {\
    'NWRITE': 0,\
    'ISTART': 0,\
    'ICHARG': 2,\
    'PREC'  : 'Normal',\
    'EDIFF' : 1E-6,\
    'NELMIN': 6,\
    'NELM'  : 999,\
    'ALGO'  : 'Normal',\
    'IBRION': 2,\
    'EDIFFG': 1E-2,\
    'ISIF'  : 3,\
    'ISMEAR': 0,\
    'SIGMA' : 0.02,\
    'LWAVE' : '.FALSE.',\
    'LCHARG': '.FALSE.',\
    'LPLANE': '.TRUE.',\
    'ISYM'  : 0,\
  }

  initKey['scf'] = {\
    'ISTART': 0,\
    'ICHARG': 2,\
    'PREC'  : 'Normal',\
    'EDIFF' : 1E-6,\
    'NELMIN': 6,\
    'NELM'  : 999,\
    'ALGO'  : 'Normal',\
    'ISMEAR': 0,\
    'SIGMA' : 0.02,\
    'LWAVE' : '.FALSE.',\
    'LCHARG': '.FALSE.',\
    'LPLANE': '.TRUE.',\
    'ISYM'  : 0,\
  }

  # Constructor
  # paraDict is convenient for predefined set of keys
  # kwargs for any additional keys: for any task independent
  def __init__(self, paraDict={}, **kwargs):
    self.paraDict = {}
    for key in paraDict:
      if key in KnownKeySet:
        self.paraDict[key] = paraDict[key]
      else:
        raise ValueError("Constructor paraDict: INCAR key not known")
    # With this ordering kwargs provided overwrite paraDict
    for key in kwargs:
      if key in KnownKeySet:
        self.paraDict[key] = kwargs[key]
      else:
        raise ValueError("Constructor kwargs: INCAR key not known")

  # Write the class to file
  def write(self, fileName):
    incarFile = open(fileName, 'w')
    for key in self.paraDict:
      incarFile.write(str(key) + ' = ' + str(self.paraDict[key]) + '\n')
