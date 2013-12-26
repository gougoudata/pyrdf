"""
  Class implements the KPOINTS file
"""

class kpoints():

  # Constructor
  def __init__(self, mode, klength, poscar = None):
    self.mode = mode
    self.klength = klength
    self.poscar = poscar

  def write(self, fileName):
    if self.mode == 'Auto':
      # Does not need to know poscar
      kpointsFile = open(fileName, 'w')
      kpointsFile.write('KPOINTS Automatic generated by pycell\n')
      kpointsFile.write('0\n')
      kpointsFile.write('Auto\n')
      kpointsFile.write('%d' % (self.klength))

    if self.mode == 'MP':
      kpointsFile=open(fileName, 'w')
      kpointsFile.write('KPOINTS Automatic generated by pycell\n')
      kpointsFile.write('0\n')
      kpointsFile.write('Monkhost-Pack\n')
      kpointsFile.write('%d %d %d' \
        %(self.klength[0], self.klength[1], self.klength[2]))