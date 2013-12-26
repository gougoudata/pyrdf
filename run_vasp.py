def get_energy():
  from xml.dom import minidom
  xmldoc = minidom.parse('vasprun.xml')
  #print xmldoc.childNodes[0].nodeValue
  calclist = xmldoc.getElementsByTagName('calculation')
  lastcalc = calclist[-1]
  energylist = lastcalc.getElementsByTagName('energy')
  lastenergy = energylist[-1]
  ilist = lastenergy.getElementsByTagName('i')
  for i in ilist:
    if i.attributes['name'].value == "e_fr_energy":
      return float(i.childNodes[0].nodeValue)

def run(np):
  # Run on pegasus
  if np < 0:
    import os
    os.system('mpirun -machinefile ~/machines -n '\
      + str(abs(np)) + ' ~/bin/pvasp_wannier')
    return get_energy()
  # Else
  if np == 1:
    import os
    os.system('vasp')
    return get_energy()
  else:
    import os
    os.system('aprun -n ' + str(np) + ' vasp5.2')
    return get_energy()
