"""
   vasp calculator
"""

class vasp:

  # Constructor
  def __init__(self, uc, exc, klength, purpose, **kwargs):
    self.uc = uc
    self.exc = exc
    self.klength = klength
    # purpose: 'relax'
    self.purpose = purpose
    # Additional key passed to incar
    self.kwargs = kwargs

  def prepare(self):
    ps = self.uc.convertToPoscar()
    ps.write('POSCAR')
    from potcar import potcar
    pt = potcar(self.exc)
    pt.write(ps, 'POTCAR')
    from kpoints import kpoints
    k = kpoints('MP', self.klength)
    k.write('KPOINTS')

    from incar import incar
    if self.purpose == 'relax':
      i = incar(incar.initKey['relax'], **self.kwargs)
      i.write('INCAR')

    if self.purpose == 'scf':
      i = incar(incar.initKey['scf'], **self.kwargs)
      i.write('INCAR')
    
  def run(self, np):
    from run_vasp import run
    return run(np)
