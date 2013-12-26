# switch of xc functional
# value holds the standard folder name of pp
def switchEXC(x):
  return {'LDA':'potpaw', 'PBE':'potpaw_PBE'}[x]

"""
class implementing the potcar file
"""

class potcar():
  # Constructor
  # The default pseudopotential path is from environment variable
  # VASP_PP_PATH
  # LDA exchange correlation potential is used by default
  import os
  def __init__(self, exc, ppPath = os.environ['VASP_PP_PATH']):
    self.ppPath = ppPath
    self.exc = exc

  # Write a corresponding potcar for a poscar object
  def write(self, poscar, fileName):
    sl = poscar.paraDict['speciesLabel']
    ppFolder = switchEXC(self.exc)
    POTCARTextList = []
    for label in sl:
      # TODO Don't care about the other lousy PPs
      if self.ppPath[-1] != '/':
        f = open(self.ppPath + '/' + ppFolder + '/' + label + '/POTCAR', 'r')
      else:
        f = open(self.ppPath + ppFolder + '/' + label + '/POTCAR', 'r')
      POTCARTextList.append(f.read())
    outputFile = open(fileName, 'w')
    for POTCARText in POTCARTextList:
      outputFile.writelines(POTCARText)

  
