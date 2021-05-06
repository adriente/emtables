from emtables.tables import EDXSTable
import numpy as np

def test_EDXSTable () :
    be = 3
    er = [1,2]
    elts = [79]
    cst = 1e-24
    
    t = EDXSTable(elements = elts,beam_energy = be, energy_range = er, cs_threshold = cst) 
    t.generate_table()
    
    energies = np.array(t.table["79"]["energies"])
    cs = np.array(t.table["79"]["cs"])
    
    np.testing.assert_array_less(cst,cs)
    np.testing.assert_array_less(energies,be)
    np.testing.assert_array_less(er[0],energies)
    np.testing.assert_array_less(energies,er[1])