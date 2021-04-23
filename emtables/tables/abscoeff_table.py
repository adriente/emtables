from emtables.tables import EMTable
from emtables.ics_EDXS.EDXS_sdicts import create_transition_dict, create_shell_dict, create_line_dict
from emtables.conf import WERNISCH_H
from emtables.tables.abscoeff_functions import wernisch_dK, wernisch_dL, wernisch_dM, wernisch_dN
import xraylib as xr

class AbsCoeffTable (EMTable) :
    def __init__ (self,**kwargs) :
        super().__init__(**kwargs)
        self.mdata["type"] =  "Wernisch_abs_coeff"
        self.list_L = ["L1", "L2", "L3"]
        self.list_M = ["M1", "M2", "M3", "M4", "M5"]
        self.xr_dict = xr.__dict__
        
    def generate_table(self) :
        L, M = False, False
        element_dict = {}
        for elt in self.elements:
            shells_dict = {}
            try:
                xr.EdgeEnergy(elt, self.xr_dict["L1_SHELL"])
                L = True
                for shell in self.list_L:
                    shells_dict[shell] = [
                        xr.EdgeEnergy(elt, self.xr_dict[shell + "_SHELL"]),
                        WERNISCH_H[shell],
                    ]
            except ValueError:
                pass
            try:
                xr.EdgeEnergy(elt, self.xr_dict["M1_SHELL"])
                M = True
                for shell in self.list_M:
                    shells_dict[shell] = [
                        xr.EdgeEnergy(elt, self.xr_dict[shell + "_SHELL"]),
                        WERNISCH_H[shell],
                    ]
            except ValueError:
                pass
            if M and L:
                d = [
                    wernisch_dK(elt),
                    wernisch_dL(elt),
                    wernisch_dM(elt),
                    wernisch_dN(elt),
                ]
                k = [-2.685, -2.669, -2.514, -2.451]
            elif L and not (M):
                d = [
                    wernisch_dK(elt),
                    wernisch_dL(elt),
                    wernisch_dM(elt),
                ]
                k = [-2.685, -2.669, -2.514]
            else:
                d = [wernisch_dK(elt), wernisch_dL(elt)]
                k = [-2.685, -2.669]
            try : 
                shells_dict["K"] = [xr.EdgeEnergy(elt, self.xr_dict["K_SHELL"]), 1.0]
                shells_dict["d"] = d
                shells_dict["exp"] = k
                element_dict[str(elt)] = shells_dict
            except ValueError :
                pass
            L, M = False, False
            
        self.table = element_dict
        
if __name__ == "__main__" :
    t = AbsCoeffTable(elements = [79],beam_energy = 3, energy_range = 20)
    t.generate_table()
    print(t.table)
    ask = input("Generate the default table (This will take a while) ? [y|n]")
    if ask == "y" : 
        t = AbsCoeffTable()
        t.generate_table()
        t.save_table("default_abscoeff.json")
        